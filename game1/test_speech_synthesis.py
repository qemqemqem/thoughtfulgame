from gtts import gTTS
import pygame

# Set the text to be spoken
text = "Hello, World! This is a test of the speech synthesis system."

# Create a gTTS object and specify the language
tts = gTTS(text, lang='en')

# Save the audio file
tts.save('output.mp3')

# Load the audio file with pygame
pygame.mixer.init()
pygame.mixer.music.load('output.mp3')

# Play the audio file
pygame.mixer.music.play()

# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)



# import threading
#
# from gtts import gTTS
# import pygame
#
# def text_to_speech(text):
#     # Initialize pygame mixer
#     pygame.mixer.init()
#
#     # Create a gTTS object
#     tts = gTTS(text=text)
#
#     # Save the audio file
#     tts.save('output.mp3')
#
#     # Load the audio file into pygame mixer
#     pygame.mixer.music.load('output.mp3')
#
#     # # Speed up playback
#     # pygame.mixer.music.set_pos(1.0)
#
#     # Play the audio file
#     pygame.mixer.music.play()
#
#     # Wait for the audio to finish playing
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#
#     # Clean up
#     pygame.mixer.quit()
#
# # from playsound import playsound
# #
# # def text_to_speech2(text):
# #     # Create a gTTS object
# #     tts = gTTS(text)
# #
# #     # Save the mp3 file
# #     tts.save("speech.mp3")
# #
# #     # Load the mp3 file with speed 2x
# #     playsound("speech.mp3", True)
# #
# # text_to_speech2("This is a test of the fast talking synthesis system")
#
# # import pyttsx3
# #
# # def text_to_speech2(text, rate=150):
# #     engine = pyttsx3.init()
# #     engine.setProperty('rate', rate)  # Adjust playback speed
# #     engine.say(text)
# #     engine.runAndWait()
# #
# # text_to_speech2("This is a test of the fast talking synthesis system", 200)
#
# if __name__ == "__main__":
#     text = "This is a test of the fast talking synthesis system"
#     t = threading.Thread(target=text_to_speech, args=(text,))
# #     t.start()