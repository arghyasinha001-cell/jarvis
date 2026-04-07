import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone() 

# Speed Tuning
r.dynamic_energy_threshold = False
r.energy_threshold = 300 
r.pause_threshold = 0.5    
r.non_speaking_duration = 0.3

def listen():
    with mic as source:
        try:
            # timeout=5: Waits 5s for you to START talking
            # phrase_time_limit=5: Stops listening after 5s of talking
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            query = r.recognize_google(audio, language="en-us").lower()
            return query
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""