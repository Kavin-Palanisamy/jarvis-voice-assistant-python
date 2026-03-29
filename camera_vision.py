import cv2
import os
import datetime
import time

def capture_photo():
    """Captures a photo and saves it to the gallery."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Camera not accessible, Sir."
        
    time.sleep(1)
    ret, frame = cap.read()
    
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = "gallery"
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = os.path.join(folder, f"photo_{timestamp}.jpg")
        cv2.imwrite(path, frame)
        cap.release()
        return f"Photo captured and saved to {path}, Sir."
    
    cap.release()
    return "I failed to capture the image, Sir."


def take_selfie():
    """Takes a selfie photo from the camera."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Camera not accessible for selfie, Sir."
    
    speak_hint = "Smile, Sir!"
    print(speak_hint)
    time.sleep(1.5)  # pause for user to smile
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = "gallery"
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = os.path.join(folder, f"selfie_{timestamp}.jpg")
        cv2.imwrite(path, frame)
        return f"Selfie captured and saved to {path}, Sir. Looking sharp."
    return "Selfie capture failed, Sir."


def detect_faces():
    """Detects faces in the current camera frame and returns the count."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    time.sleep(0.5)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "Camera unavailable, Sir."
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    count = len(faces)
    if count == 0:
        return "I don't see anyone in the room, Sir."
    elif count == 1:
        return "I see one person in the room, Sir."
    else:
        return f"I detect {count} individuals present, Sir."


def count_people():
    """Counts people visible through the camera."""
    return detect_faces()


def detect_objects():
    """Detects common objects in the camera frame using OpenCV."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Camera not accessible for object detection, Sir."
    
    time.sleep(0.5)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "Camera unavailable for object detection, Sir."
    
    # Use face detection as one layer of object detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces  = face_cascade.detectMultiScale(gray, 1.1, 4)
    eyes   = eye_cascade.detectMultiScale(gray, 1.1, 4)
    bodies = body_cascade.detectMultiScale(gray, 1.05, 3)
    
    detections = []
    if len(faces)  > 0: detections.append(f"{len(faces)} face(s)")
    if len(bodies) > 0: detections.append(f"{len(bodies)} full body(s)")
    if len(eyes)   > 0: detections.append(f"{len(eyes)} eye region(s)")
    
    if detections:
        return f"Object scan complete. I detected: {', '.join(detections)}, Sir."
    else:
        return "No significant objects detected in frame, Sir."


def record_video(seconds=10):
    """Records a video from the webcam for the specified duration."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Camera not accessible for recording, Sir."
    
    folder = "gallery"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"video_{timestamp}.avi")
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = 20.0
    
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    
    print(f"Recording for {seconds} seconds...")
    start = time.time()
    while time.time() - start < seconds:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    cap.release()
    out.release()
    return f"Video recorded and saved to {path}, Sir."


def start_camera_feed():
    """Opens a window showing the live camera feed."""
    cap = cv2.VideoCapture(0)
    print("Starting visual feed... Press 'q' to close.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow('JARVIS - Optical Input', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return "Camera feed closed."


if __name__ == "__main__":
    pass
