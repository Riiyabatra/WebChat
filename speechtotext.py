import speech_recognition as sr
import texttospeech 
sample_rate = 12000
chunk_size = 2048
def sst():
    
    r = sr.Recognizer() 
    with sr.Microphone(device_index = 2, sample_rate = sample_rate,  chunk_size = chunk_size) as source: 
        r.adjust_for_ambient_noise(source)   
        audio = r.listen(source) 
        try: 
            msg = r.recognize_google(audio) 
        except sr.UnknownValueError: 
            texttospeech.tts("Google Speech Recognition could not understand audio")
            print("Google Speech Recognition could not understand audio") 
      
        except sr.RequestError as e: 
            texttospeech.tts("Could not request results from Google Speech Recognition service; {0}".format(e))
            print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
        return msg


    