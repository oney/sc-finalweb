if (performance.navigation.type == 2) {
  location.reload(true);
}

var room = document.getElementById("room");
var input = document.getElementById("input");

var timeEls = document.querySelectorAll('time');
if (timeEls.length)
  timeago.render(timeEls);

room.scrollIntoView(false);

function addMessage(content, user) {
  var li = document.createElement("li");
  li.classList = "list-group-item " + (user === undefined ? "me" : "other");

  var contentEl = document.createElement("div");
  contentEl.classList = "content";

  contentEl.appendChild(document.createTextNode(
    (user ? user + ":\n" : "") + content
  ));
  li.appendChild(contentEl);

  var createdAt = document.createElement("small");
  createdAt.classList = "badge badge-secondary badge-pill";
  createdAt.innerHTML = `<time datetime="${new Date().toISOString()}"></time>`;
  li.appendChild(createdAt);
  room.appendChild(li);
  timeago.render(li.querySelectorAll('time'));

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
  if (event.keyCode === 13 && !event.shiftKey) {
    chatsend()
  }
}

function chatsend() {
  var content = input.value.trim();
  if (content) {
    if (ws.readyState != 1) {
      alert("Connecting to chat server...\nTry later");
      return;
    }
    
    addMessage(content);
    ws.send(JSON.stringify({
      'content': content
    }));
    input.value = "";
    input.focus();
  }
}