import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Optional: You can customize the voice here (0 for male, 1 for female typically)
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id) 

def speak(text):
    """
    Speaks the given text out loud and prints it to the console.
    """
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """
    Listens to the microphone and returns the recognized text in lowercase.
    Returns an empty string if nothing was recognized or an error occurred.
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise so it doesn't trigger randomly
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Listen to the audio from the microphone
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            
            # Convert audio to text using Google's free speech recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            # Reached when no speech is detected after a while
            pass 
        except sr.UnknownValueError:
            # Reached when speech was detected but could not be understood
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            # Reached when the internet connection is down or API fails
            print(f"Could not request results; {e}")
            
    return ""
