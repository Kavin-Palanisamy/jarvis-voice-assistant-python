document.addEventListener("DOMContentLoaded", () => {
    // Connect to the Flask-SocketIO server
    const socket = io();

    const statusText = document.getElementById("status-text");
    const subtitleText = document.getElementById("subtitle-text");

    // Listen for 'status_update' events from the Python backend
    socket.on("status_update", (data) => {
        const state = data.state;
        const message = data.message;

        // Strip previous state classes
        document.body.className = '';

        if (state === "idle") {
            statusText.innerText = "JARVIS";
            subtitleText.innerText = message || "System Online // Mark VII";
            document.body.className = 'state-idle';
        } 
        else if (state === "listening") {
            document.body.classList.add("state-listening");
            statusText.innerText = "LISTENING";
            subtitleText.innerText = message || "Awaiting Voice Command...";
        } 
        else if (state === "thinking" || state === "SECURITY SCAN") {
            document.body.classList.add("state-thinking");
            statusText.innerText = state === "SECURITY SCAN" ? "SCANNING" : "PROCESSING";
            subtitleText.innerText = message || "Analyzing...";
        } 
        else if (state === "speaking" || state === "ACCESS GRANTED") {
            document.body.classList.add("state-speaking");
            statusText.innerText = state === "ACCESS GRANTED" ? "CONFIRMED" : "RESPONDING";
            subtitleText.innerText = message || "...";
        }

        // Update current task log if message is task-related
        const taskEl = document.getElementById("current-task");
        if (taskEl && message) {
            taskEl.innerText = message;
        }
    });

    // Optional: Send a connected ping
    socket.on("connect", () => {
        console.log("Connected to JARVIS Engine.");
    });
});
