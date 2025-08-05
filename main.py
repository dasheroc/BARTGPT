<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bart Is Listening</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
</head>
<body>
    <div class="container">
        <h1>BART IS LISTENING</h1>
        <textarea id="user-input" placeholder="Unburden your soul here..."></textarea>
        <button id="submit">PROCEED</button>
        <div id="response" class="response"></div>
    </div>

    <script>
        const input = document.getElementById("user-input");
        const button = document.getElementById("submit");
        const responseDiv = document.getElementById("response");

        async function sendMessage() {
            const message = input.value.trim();
            if (!message) return;

            const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });

            const data = await res.json();
            responseDiv.textContent = data.response;
        }

        button.addEventListener("click", sendMessage);
        input.addEventListener("keydown", e => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
