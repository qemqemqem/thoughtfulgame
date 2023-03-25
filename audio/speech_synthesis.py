from gtts import gTTS
import pygame
import threading
import os
import tempfile

def _speak(text):
    # Create a gTTS object and specify the language
    tts = gTTS(text, lang='en')

    # Save the audio data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        tts.write_to_fp(f)
        file_name = f.name

    # Load the audio data from the temporary file with pygame
    pygame.mixer.init()
    pygame.mixer.music.load(file_name)

    # Play the audio data from memory
    pygame.mixer.music.play()

    # Delete the temporary file
    # TODO This does not work in Windows
    # os.remove(file_name)


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
