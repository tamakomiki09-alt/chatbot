document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();
    if (message === "") return;

    addUserMessage(message);
    input.value = "";

    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        addAIMessage(data.answer);
    });
}

function addUserMessage(msg) {
    let box = document.getElementById("chat-box");
    box.innerHTML += `<div class="user-message">${msg}</div>`;
    box.scrollTop = box.scrollHeight;
}

function addAIMessage(msg) {
    let box = document.getElementById("chat-box");
    box.innerHTML += `<div class="ai-message">${msg}</div>`;
    box.scrollTop = box.scrollHeight;
}
