import websocket
import ssl
import json

token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImxvZ2luX3VzZXJfa2V5IjoiYTQ0NDkzZjQtODA1My00N2Y5LTgwMzQtNDY2MWJiZGM3N2QwIn0.1pV34Pk9xzjONWHnG_7UDIJz6U-SUDvEpp3WvNy0C2owVEzraZS8X57y1QoPA9q5eI2m0hnbJX_K8jyf_-jvCw'
conversation_id = 'test-123'
ws_url = f'ws://localhost:8080/ws/chat/{conversation_id}?token={token}'

print(f'Connecting to: {ws_url}')

try:
    ws = websocket.create_connection(
        ws_url,
        timeout=10,
        header=[
            f"Cookie: Admin-Token={token}"
        ]
    )
    print('WebSocket connected successfully!')
    print(f'Protocol: {ws.getstatus()}')
    ws.close()
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
