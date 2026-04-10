#!/bin/bash
pkill -f "uvicorn" || true
sleep 2
echo "uvicorn processes:"
ps aux | grep uvicorn | grep -v grep || echo "none"
