import pygame

# Initialize pygame mixer
def player():
    pygame.mixer.init()

    # Load your music file
    pygame.mixer.music.load('wallet_empty/trimmed_sad.mp3')
    # Play the music
    pygame.mixer.music.play()
    # print('chalaaa')
    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(2)
