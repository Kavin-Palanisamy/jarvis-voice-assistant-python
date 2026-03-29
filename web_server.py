import threading
import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO

# Import our JARVIS modules
from voice_engine import speak, listen
from command_parser import split_into_tasks, clean_task
from task_engine import execute_task

# Initialize Flask and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jarvis-secret-key'
socketio = SocketIO(app, async_mode='threading')

def emit_status(state, message=""):
    """Helper function to send status updates to the frontend."""
    socketio.emit('status_update', {'state': state, 'message': message})

def wish_me():
    """Greets the user based on the current time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning, Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Sir!")
    else:
        speak("Good Evening, Sir!")
    speak("Jarvis is online. Awaiting your command.")

def run_jarvis_loop():
    """
    Background loop updated for task chaining with real-time UI updates.
    """
    import time
    time.sleep(2)
    
    emit_status('speaking', "Initializing JARVIS Core...")
    wish_me()
    
    while True:
        print("\nAwaiting wake word 'Jarvis'...")
        emit_status('idle', "Awaiting Wake Word 'Jarvis'")
        
        wake_text = listen(timeout=None, phrase_time_limit=5)
        
        if not wake_text:
            continue
            
        if "jarvis" in wake_text:
            # Check for immediate command
            immediate_command = wake_text.replace("jarvis", "").strip()
            
            full_command = ""
            if immediate_command:
                full_command = immediate_command
            else:
                emit_status('speaking', "Yes, Sir?")
                speak("Yes, Sir?")
                emit_status('listening', "Listening for command...")
                full_command = listen(timeout=10, phrase_time_limit=15)
            
            if not full_command:
                emit_status('speaking', "I didn't catch that, Sir.")
                speak("I didn't catch that, Sir.")
                emit_status('idle')
                continue
                
            # Exit check
            if any(word in full_command.lower() for word in ["stop listening", "exit", "goodbye", "quit", "sleep", "shutdown jarvis"]):
                emit_status('speaking', "Goodbye, Sir. Shutting down systems.")
                speak("Goodbye, Sir. Shutting down systems.")
                emit_status('idle', "SYSTEM OFFLINE")
                break
                
            # Task Chaining Logic for Web UI
            tasks = split_into_tasks(full_command)
            cleaned_tasks = [clean_task(t) for t in tasks]
            
            for i, task in enumerate(cleaned_tasks):
                if i > 0:
                    time.sleep(1)
                
                emit_status('thinking', f"Executing: {task}")
                response = execute_task(task)
                
                if response:
                    emit_status('speaking', response)
                    speak(response)
                    
            emit_status('idle', "Awaiting Wake Word 'Jarvis'")

@app.route('/')
def index():
    """Serve the main JARVIS UI."""
    return render_template('index.html')

    # Start the Flask Web Server in a separate background thread
    print("Starting Web Server. Open http://127.0.0.1:5000 in your browser.")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    
    # Start the JARVIS Voice loop in the MAIN thread to avoid Windows COM crashes
    try:
        run_jarvis_loop()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
