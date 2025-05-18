let ws = null;

async function register() {
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;
    const response = await fetch("/register", {
        method: "POST",
        body: new URLSearchParams({ username, password }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    const data = await response.json();
    alert(data.message);
    if (data.status === "ok") {
        document.getElementById("register-username").value = "";
        document.getElementById("register-password").value = "";
    }
}

async function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const response = await fetch("/login", {
        method: "POST",
        body: new URLSearchParams({ username, password }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    const data = await response.json();
    alert(data.message);
    if (data.status === "ok") {
        document.getElementById("login-username").value = "";
        document.getElementById("login-password").value = "";
        window.location.reload();
    }
}

async function logout() {
    await fetch("/logout", { method: "POST" });
    window.location.reload();
}

async function connectWebSocket() {
    const me = await fetch("/me");
    if (!me.ok) return;
    const userData = await me.json();
    const username = userData.username;
    ws = new WebSocket("ws://localhost:8000/ws/1");

    ws.onopen = () => {
        console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
        const chat = document.getElementById("chat");
        const message = document.createElement("div");
        message.textContent = event.data;
        chat.appendChild(message);
    };

    ws.onclose = () => {
        console.log("WebSocket closed");
    };

    document.getElementById("send").onclick = () => {
        const content = document.getElementById("message").value;
        ws.send(JSON.stringify({
            content,
            room_id: 1,
            user_id: 1,
            username
        }));
        document.getElementById("message").value = "";
    };

    document.getElementById("logout").onclick = logout;
}

window.onload = async () => {
    const me = await fetch("/me");
    if (me.ok) {
        const userData = await me.json();
        document.getElementById("user-info").textContent = `Zalogowano jako: ${userData.username}`;
        document.getElementById("logout").style.display = "inline-block";
        connectWebSocket();
    }
};
