import pygame
import os
from rich import print
from mutagen.mp3 import MP3
import time
import asyncio

# Documentation: https://www.pygame.org/docs/
# or, search something like "playing audio pygame"

class AudioManager:

    def __init__(self):
        # Use higher frequency to prevent audio glitching noises
        pygame.mixer.init(frequency=48000, buffer=1024)

    def play_audio(self, file_path, use_music=True):
        """
        Parameters:
        file_path (str): path to the audio file
        sleep_during_playback (bool): means program will wait for length of audio file before returning
        delete_file (bool): means file is deleted after playback (note that this shouldn't be used for multithreaded function calls)
        play_using_music (bool): means it will use Pygame Music, if false then uses pygame Sound instead
        """
        print(f"Playing file with pygame: {file_path}")
        if not pygame.mixer.get_init(): # Reinitialize mixer if needed
            pygame.mixer.init(frequency=48000, buffer=1024) 
        if use_music:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            file_length = self.get_audio_length(file_path)
            time.sleep(file_length)
        else:
            # Pygame Sound lets you play multiple sounds simultaneously
            pygame_sound = pygame.mixer.Sound(file_path) 
            pygame_sound.play()
        
    def get_audio_length(self, file_path):
        # Calculate length of the file based on the file format
        _, ext = os.path.splitext(file_path) # Get the extension of this file
        if ext.lower() == '.mp3':
            mp3_file = MP3(file_path)
            file_length = mp3_file.info.length
        else:
            print("Unknown audio file type. Returning 0 as file length")
            file_length = 0
        return file_length
        


if __name__ == "__main__":
    # radio = AudioManager()
    # radio.play_audio("audio_test.mp3")
    pass