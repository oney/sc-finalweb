var room = document.getElementById("room");
var input = document.getElementById("input");
room.scrollIntoView(false);

function addMessage(content, user) {
  var li = document.createElement("li");
  li.classList = "list-group-item " + (user === undefined ? "me" : "other");
  li.appendChild(document.createTextNode((user ? user + ": " : "") + content)); 
  room.appendChild(li);

  room.scrollIntoView(false);
}

var ws;
function connect() {
  ws = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomId + '/?token=' + jwtToken);

  ws.onmessage = function (e) {
    var data = JSON.parse(e.data);
    var message = data.message;
    if (meId == message.user.id) return;

    addMessage(message.content, message.user.name);
  };

  ws.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
    setTimeout(function() {
      connect();
    }, 500);
  };

  ws.onerror = function(err) {
    console.error('Socket encountered error: ', err.message, 'Closing socket');
    ws.close();
  };
}

connect();

input.onkeyup = function(event) {
  if (ws.readyState != 1) {
    alert("Connecting to chat server...\nTry later");
    return;
  }

  if (event.keyCode === 13 && input.value) {
    addMessage(input.value);
    ws.send(JSON.stringify({
      'content': input.value
    }));
    input.value = "";
  }
}