export const connectToWebSocket = (documentId, token, onMessage) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${documentId}?token=${token}`);
  
    ws.onopen = () => {
      console.log('WebSocket connected');
    };
  
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      onMessage(message);
    };
  
    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };
  
    return ws;
  };
  