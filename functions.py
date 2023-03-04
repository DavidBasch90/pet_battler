import pickle
import pygame
import os
import random
from pet_class import Pet
# Function to save player's pet to a file

def create_player_pet(pet_choice, user_ip):
    player_level = 1
    player_hp, player_attack, player_defense, moves = generate_pet_stats(pet_choice, player_level)

    # Create a new pet instance with the selected species
    player_pet = Pet(user_ip, pet_choice, player_level, player_hp, player_attack, player_defense,
                     moves)
    return player_pet
def save_game(pet):
    with open("saves/saved_game.dat", "wb") as f:
        # Add the attacks to the pet object

        pickle.dump(pet, f)
# Define the button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
screen_width = 800
screen_height = 600
# Define the button colors
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (200, 200, 200)
YES_BUTTON_COLOR = (0, 255, 0)
NO_BUTTON_COLOR = (255, 0, 0)

# Initialize Pygame
pygame.init()


# Define the font and font size for the button text
BUTTON_FONT = pygame.font.SysFont(None, 30)

# Function to load player's pet from a file
def load_game():
    try:
        with open("saves/saved_game.dat", "rb") as f:
            pet = pickle.load(f)

        # Get the attacks from the Pet object and assign them to the moves attribute
        return pet
    except FileNotFoundError:
        print("No saved game found.")
        return None

SPECIES = ["Bunyip", "Griffin"]
SPECIES_STATS = {
    "Bunyip":{
        "name": "Bunyip",
        "min_hp": 10,
        "max_hp": 20,
        "min_attack": 5,
        "max_attack": 10,
        "min_defense": 5,
        "max_defense": 10,
        "attacks": [
            {"name": "Scratch", "damage": 5},
            {"name": "Bite", "damage": 8},
            {"name": "Tackle", "damage": 6},
            {"name": "Growl", "damage": 8}
        ]
    },
    "Griffin": {
        "name": "Griffin",
        "min_hp": 15,
        "max_hp": 25,
        "min_attack": 8,
        "max_attack": 12,
        "min_defense": 8,
        "max_defense": 12,
        "attacks": [
            {"name": "Peck", "damage": 6},
            {"name": "Claw", "damage": 8},
            {"name": "Fly", "damage": 5},
            {"name": "Roar", "damage": 2}
        ]
    },
    # Add more species here
}
# Create a function to display a button on the screen
def draw_button(screen, x, y, text, color,highlighted=False):
    # Check if the mouse is hovering over the button
    button_color = color

    if highlighted:
        button_color = BUTTON_HOVER_COLOR


    # Draw the button rectangle
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, button_color, button_rect)

    # Draw the button text
    button_text = BUTTON_FONT.render(text, True, (0, 0, 0))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def draw_text(screen, text, x, y, font_size, color):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)

    # Get the dimensions of the text surface
    text_rect = text_surface.get_rect()

    # Center the text within the given x, y coordinates
    text_rect.center = (x, y)

    screen.blit(text_surface, text_rect)

# Function to display a list of save files and return the selected file
def select_save_file(save_files):
    # Get a list of available save files


    # Create a new screen to display the save file list
    save_file_screen = pygame.display.set_mode((screen_width, screen_height))
    save_file_screen.fill((0, 0, 0))
    draw_text(save_file_screen, "Select a save file to load:", screen_width // 2, screen_height // 4, 30, (255, 255, 255))

    # Display the save files as a list of buttons
    button_y = screen_height // 2
    for save_file in save_files:
        draw_button(save_file_screen, screen_width // 2 - BUTTON_WIDTH // 2, button_y, save_file, BUTTON_COLOR)
        button_y += BUTTON_HEIGHT + 10

def get_save_files():
    # Get the current working directory
    cwd = os.getcwd()

    # Get the path to the saves directory
    saves_path = os.path.join(cwd, 'saves')

    # Create the saves directory if it doesn't already exist
    if not os.path.exists(saves_path):
        os.mkdir(saves_path)

    # Get a list of all the files in the saves directory
    save_files = os.listdir(saves_path)

    # Filter out any files that don't end in ".dat"
    save_files = [file for file in save_files if file.endswith('.dat')]

    # Return the list of save files
    return save_files

def generate_pet_stats(pet_choice, player_level):
    species_stats = SPECIES_STATS[pet_choice]

    player_hp = random.randint(species_stats["min_hp"], species_stats["max_hp"]) * player_level
    player_attack = random.randint(species_stats["min_attack"], species_stats["max_attack"]) * player_level
    player_defense = random.randint(species_stats["min_defense"], species_stats["max_defense"]) * player_level

    moves = random.sample(species_stats["attacks"], k=min(4, len(species_stats["attacks"])))

    return player_hp, player_attack, player_defense, moves


