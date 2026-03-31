#!/usr/bin/env python
"""Upload a local file to MinerU API, wait for extraction, and download results.

Usage:
    python scripts/mineru_api_extract.py --input /path/to/file.pdf --output-dir /path/to/out

Auth:
    Set MINERU_API_KEY in the environment, or pass --api-key directly.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import zipfile
from pathlib import Path

import requests


API_BASE = "https://mineru.net/api/v4"
RETRY_STATUS_CODES = {408, 429, 500, 502, 503, 504}
DEFAULT_SECRET_FILE = Path(".secrets/mineru.env")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract a local file with MinerU API")
    parser.add_argument("--input", required=True, help="Local file path")
    parser.add_argument("--output-dir", required=True, help="Directory to store outputs")
    parser.add_argument("--api-key", help="MinerU API key; defaults to MINERU_API_KEY")
    parser.add_argument("--data-id", help="Optional custom data_id")
    parser.add_argument("--model-version", default="vlm", help="MinerU model version")
    parser.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds")
    parser.add_argument("--max-polls", type=int, default=120, help="Maximum polling attempts")
    return parser.parse_args()


def build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }


def require_ok(resp: requests.Response) -> dict:
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"MinerU API error: {json.dumps(data, ensure_ascii=False)}")
    return data


def request_with_retries(method: str, url: str, *, max_attempts: int = 3, retry_delay: int = 2, **kwargs) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.request(method, url, **kwargs)
            if resp.status_code in RETRY_STATUS_CODES and attempt < max_attempts:
                time.sleep(retry_delay * attempt)
                continue
            return resp
        except requests.RequestException as exc:
            last_error = exc
            if attempt >= max_attempts:
                break
            time.sleep(retry_delay * attempt)
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"Request failed without response: {method} {url}")


def load_api_key_from_file(secret_file: Path) -> str | None:
    if not secret_file.exists():
        return None

    for raw_line in secret_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() != "MINERU_API_KEY":
            continue
        return value.strip().strip("'").strip('"')
    return None


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    secret_file = (Path.cwd() / DEFAULT_SECRET_FILE).resolve()
    api_key = args.api_key or os.environ.get("MINERU_API_KEY") or load_api_key_from_file(secret_file)
    if not api_key:
        raise RuntimeError(
            "Missing API key. Set MINERU_API_KEY, pass --api-key, "
            f"or put MINERU_API_KEY=... in {secret_file}"
        )

    headers = build_headers(api_key)
    data_id = args.data_id or f"{input_path.stem}_{int(time.time())}"

    apply_payload = {
        "files": [{"name": input_path.name, "data_id": data_id}],
        "model_version": args.model_version,
    }
    apply_resp = request_with_retries(
        "POST",
        f"{API_BASE}/file-urls/batch",
        headers={**headers, "Content-Type": "application/json"},
        json=apply_payload,
        timeout=60,
    )
    apply_data = require_ok(apply_resp)
    batch_id = apply_data["data"]["batch_id"]
    upload_url = apply_data["data"]["file_urls"][0]

    with input_path.open("rb") as fh:
        upload_resp = request_with_retries("PUT", upload_url, data=fh, timeout=300)
    upload_resp.raise_for_status()

    result = None
    for _ in range(args.max_polls):
        time.sleep(args.poll_interval)
        poll_resp = request_with_retries(
            "GET",
            f"{API_BASE}/extract-results/batch/{batch_id}",
            headers=headers,
            timeout=60,
        )
        poll_data = require_ok(poll_resp)
        items = poll_data.get("data", {}).get("extract_result", [])
        if not items:
            continue
        item = items[0]
        state = item.get("state")
        if state == "failed":
            raise RuntimeError(f"Extraction failed: {item.get('err_msg')}")
        if state == "done":
            result = item
            break

    if result is None:
        raise TimeoutError(f"Timed out waiting for extraction result for batch {batch_id}")

    zip_url = result["full_zip_url"]
    zip_path = output_dir / f"{batch_id}.zip"
    meta_path = output_dir / f"{batch_id}.result.json"
    md_path = output_dir / f"{batch_id}.full.md"
    extract_dir = output_dir / batch_id

    zip_resp = request_with_retries("GET", zip_url, timeout=300)
    zip_resp.raise_for_status()
    zip_path.write_bytes(zip_resp.content)
    meta_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    with zipfile.ZipFile(zip_path, "r") as zf:
        extract_dir.mkdir(parents=True, exist_ok=True)
        zf.extractall(extract_dir)
        md_name = next((name for name in zf.namelist() if name.endswith("full.md")), None)
        if md_name:
            md_path.write_text(zf.read(md_name).decode("utf-8"), encoding="utf-8")

    print(json.dumps(
        {
            "batch_id": batch_id,
            "zip_path": str(zip_path),
            "meta_path": str(meta_path),
            "markdown_path": str(md_path) if md_path.exists() else None,
            "extract_dir": str(extract_dir),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
