// WebSocket connection test script
const token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImxvZ2luX3VzZXJfa2V5IjoiYTQ0NDkzZjQtODA1My00N2Y5LTgwMzQtNDY2MWJiZGM3N2QwIn0.1pV34Pk9xzjONWHnG_7UDIJz6U-SUDvEpp3WvNy0C2owVEzraZS8X57y1QoPA9q5eI2m0hnbJX_K8jyf_-jvCw';
const conversationId = 'test-123';
const wsUrl = `ws://localhost:8080/ws/chat/${conversationId}?token=${token}`;

console.log('Connecting to:', wsUrl);

const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  console.log('WebSocket connected successfully!');
  console.log('Protocol:', ws.protocol);
  console.log('ReadyState:', ws.readyState);
  ws.close();
  process.exit(0);
};

ws.onerror = (error) => {
  console.log('WebSocket error:', error.message || error);
  process.exit(1);
};

ws.onclose = (event) => {
  console.log('WebSocket closed:', event.code, event.reason);
  if (event.code !== 1000) {
    process.exit(1);
  }
};

// Timeout after 10 seconds
setTimeout(() => {
  console.log('Connection timeout');
  ws.close();
  process.exit(1);
}, 10000);
