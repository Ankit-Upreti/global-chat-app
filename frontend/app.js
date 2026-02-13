let socket;
let currentUser = "";
const url = "wss://chaton-4i6d.onrender.com";

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    currentUser = username;
    socket = new WebSocket(url);

    socket.onopen = function() {
        socket.send(JSON.stringify({
            username: username,
            password: password
        }));
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.status) {
            if (data.status === "denied") {
                alert("Authentication failed");
                return;
            }
            if (data.status === "already_logged_in") {
                alert("Already logged in elsewhere");
                return;
            }

            document.getElementById("login").style.display = "none";
            document.getElementById("chat").style.display = "block";
            return;
        }

        addMessage(data.user, data.message);
    };
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value;

    if (!message) return;

    addMessage(currentUser, message); // show instantly
    socket.send(message);
    input.value = "";
}

function addMessage(user, message) {
    const messages = document.getElementById("messages");

    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message");

    if (user === currentUser) {
        msgDiv.classList.add("self");
        msgDiv.textContent = "You: " + message;
    } else {
        msgDiv.classList.add("other");
        msgDiv.textContent = user + ": " + message;
    }

    messages.appendChild(msgDiv);
    messages.scrollTop = messages.scrollHeight;
}

function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
