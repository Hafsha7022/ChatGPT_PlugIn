var chatBox = document.getElementById("chat");
var messageInput = document.getElementById("message");
var sendButton = document.getElementById("send-btn");
function addMessage(message, who) {
    var newMessage = document.createElement("div");
    newMessage.className = "message " + who;
    newMessage.innerText = message;
    chatBox.appendChild(newMessage);
    // chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

function sendMessage() {
    var message = messageInput.value.trim();
    if(message == "") {
        return; // Do not send empty messages
    }
    addMessage(message, "user");
    messageInput.value = ""; // Clear the input field
    
    fetch('/chat', {
        method: 'POST',
        headers: {
        
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        addMessage(data.reply, "bot");
    });
}
sendButton.onclick = sendMessage;
messageInput.onkeydown = function(event) {
    if(event.key === "Enter") {
        sendMessage();
    }
}