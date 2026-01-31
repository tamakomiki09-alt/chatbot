document.getElementById("sendBtn").addEventListener("click", sendMessage);
document.getElementById("userInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.reply, "ai");
    })
    .catch(() => {
        addMessage("I'm sorry — I encountered an error.", "ai");
    });
}

function addMessage(msg, sender) {
    const chatBox = document.getElementById("chatBox");
    const bubble = document.createElement("div");

    bubble.className = sender === "user" ? "user-bubble" : "ai-bubble";
    bubble.textContent = msg;

    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
}
