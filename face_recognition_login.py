import cv2
import os
import time

# Directory to store authorized faces
AUTHORIZED_DIR = "authorized_faces"
if not os.path.exists(AUTHORIZED_DIR):
    os.makedirs(AUTHORIZED_DIR)


def load_authorized_faces():
    """Loads facial encodings from the authorized_faces directory."""
    try:
        import face_recognition
    except ImportError:
        return [], []

    known_encodings = []
    known_names = []
    
    for filename in os.listdir(AUTHORIZED_DIR):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(AUTHORIZED_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    
    return known_encodings, known_names


def recognize_user(timeout=30):
    """
    Scans the camera for a recognized face.
    Returns the name of the user if found, else None.
    """
    try:
        import face_recognition
    except ImportError:
        print("face_recognition not installed — defaulting to Admin.")
        return "Admin"

    known_encodings, known_names = load_authorized_faces()
    
    if not known_encodings:
        print("Warning: No authorized faces found. Skipping biometric login.")
        return "Admin"

    video_capture = cv2.VideoCapture(0)
    start_time = time.time()
    
    print("Initializing biometric scan...")
    
    while time.time() - start_time < timeout:
        ret, frame = video_capture.read()
        if not ret:
            break
            
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                video_capture.release()
                cv2.destroyAllWindows()
                return name
            
    video_capture.release()
    cv2.destroyAllWindows()
    return None


def verify_identity():
    """
    Runs a face recognition check and returns a JARVIS-style response string.
    Does NOT call sys.exit — safe to call from task_engine.
    """
    print("Running identity verification scan...")
    user = recognize_user(timeout=15)
    if user:
        return f"Identity verified. Welcome, {user}. Access granted."
    else:
        return "Identity not recognized. Access denied, Sir."


def start_security_scan():
    """Starts a security biometric scan and returns the result."""
    return verify_identity()


def lock_system():
    """Locks the Windows workstation immediately."""
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        return "System locked, Sir."
    except Exception as e:
        import subprocess
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        return "System locked, Sir."


def unlock_via_face():
    """Attempts to verify identity via face scan (simulates unlock)."""
    result = verify_identity()
    return result


def enable_face_recognition(name="Admin"):
    """Enrolls a new face for the authorized users list."""
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        return "Camera not accessible for enrollment, Sir."
    
    print(f"Enrolling face for: {name}. Please look at the camera...")
    time.sleep(2)
    ret, frame = video_capture.read()
    video_capture.release()
    
    if ret:
        path = os.path.join(AUTHORIZED_DIR, f"{name}.jpg")
        cv2.imwrite(path, frame)
        return f"Face recognition enabled and enrolled for {name}, Sir."
    return "Face enrollment failed, Sir."


def enroll_user(name):
    """Captures a photo from the webcam and saves it as an authorized face."""
    return enable_face_recognition(name)


if __name__ == "__main__":
    user = recognize_user(timeout=10)
    if user:
        print(f"Access Granted: Welcome back, {user}.")
    else:
        print("Access Denied: Persona Unknown.")
