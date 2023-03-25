from gtts import gTTS
import pygame
import threading
import os

def _speak(text):
    # Create a gTTS object and specify the language
    tts = gTTS(text, lang='en')

    file_name = "output" + str(hash(text)) + ".mp3"

    # Save the audio file
    tts.save(file_name)

    # Load the audio file with pygame
    pygame.mixer.init()
    pygame.mixer.music.load(file_name)

    # Delete the file
    os.remove(file_name)

    # Play the audio file
    pygame.mixer.music.play()

def speak(text):
    # Create a thread to run the _speak function
    thread = threading.Thread(target=_speak, args=(text,))
    thread.start()

if __name__ == '__main__':
    # Set the text to be spoken
    text = "Hello, World! This is a test of the speech synthesis system."

    # Speak the text
    speak(text)

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
