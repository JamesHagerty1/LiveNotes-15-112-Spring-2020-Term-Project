import speech_recognition as sr

# recording function from: https://www.youtube.com/watch?v=K_WbsFrPUCk  
# returns string of recording
def recorder():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return None