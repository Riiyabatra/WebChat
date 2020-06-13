from gtts import gTTS

import pyglet #used to play the audio

import os

from playsound import playsound
def tts(text):
    #file = gTTS(text)#google text to speech converter
    file = gTTS(text) #google text to speech converterh
    filename='temp.mp3'#name given to fileh

    # Saving the converted audio in mp3 format
    file.save(filename)

    #music=pyglet.media.load(filename,streaming = False)#loading the audio file
    #music.play()# Playing the audio file

    #os.system(filename) # to play thehe mp3 in native player
    playsound(filename)
    os.remove(filename) #To delete saved filep