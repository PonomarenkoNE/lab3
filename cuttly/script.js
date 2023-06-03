const socket = new WebSocket('ws://localhost:8000/ws/monitor/');

// Set custom headers before opening the connection
socket.onbeforeopen = function(event) {
  socket.setRequestHeader('authorization', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1ODg0NDk4LCJqdGkiOiI5ODJjOTQyMTE3OGQ0NzU4YjJiYTYwZGI1ODdjODlkMSIsInVzZXJfaWQiOjF9.kQ66F0qKDwRU86sqEitxIDBabKs1V86hQTmq_j9aV2M');
};

socket.onopen = function() {
  console.log('WebSocket connection established.');
};

socket.onmessage = function(event) {
  const message = event.data;
  updateMessageContainer(message);
};

socket.onclose = function(event) {
  console.log('WebSocket connection closed:', event);
};

socket.onerror = function(error) {
  console.error('WebSocket error:', error);
};

function updateMessageContainer(message) {
  const messageContainer = document.getElementById('message-container');
  messageContainer.innerHTML += `<p>${message}</p>`;
}