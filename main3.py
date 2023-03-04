import pygame
from pet_class import Pet
from button_class import Button
import functions
import random

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
clock = pygame.time.Clock()

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Capsumon")
# Define the button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100

# Define the button colors
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (200, 200, 200)
BACK_BUTTON_COLOR = (255, 255, 255)
YES_BUTTON_COLOR = (0, 255, 0)
NO_BUTTON_COLOR = (255, 0, 0)
BACK_BUTTON_WIDTH = 100
BACK_BUTTON_HEIGHT = 50
BACK_BUTTON_COLOR = (255, 255, 255)


# Define the font and font size for the button text
BUTTON_FONT = pygame.font.SysFont(None, 30)


# Initialization of game variables and user input box parameterss
show_load_game_screen = False
show_name_input_screen = False
show_pet_select_screen = False
show_pet_summary_screen = False
show_battle_screen = False
x = (screen_width - BUTTON_WIDTH) // 2
y = (screen_height - BUTTON_HEIGHT) // 2
game_running = True
user_ip = ''
font = pygame.font.SysFont(None, 40)
text_box = pygame.Rect(100, 100, 100, 50)
active = False
color = pygame.Color('white')
selected_button = 0

#game loop
loaded_pet = functions.load_game()
while game_running:


    mouse_pos = pygame.mouse.get_pos()

    # Create a new screen with button prompts
    screen.fill((0, 0, 0))

    # Show the main menu
    if not show_load_game_screen and not show_name_input_screen:
        # Create a new screen with button prompts
        screen.fill((0, 0, 0))
        functions.draw_text(screen, "Choose an option:", screen_width // 2, screen_height // 4, 30, (255, 255, 255))


        num_buttons = 2

        # Define the buttons using a dictionary
        buttons = {
            "new_game": {
                "text": "New Game",
                "x": x,
                "y": y,
            },
            "load_game": {
                "text": "Load Game",
                "x": x,
                "y": y + BUTTON_HEIGHT + 10,
            },
        }

        # Loop through the buttons and draw each one
        for i, (key, button) in enumerate(buttons.items()):
            highlighted = (i == selected_button)
            functions.draw_button(screen, button["x"], button["y"], button["text"], BUTTON_COLOR, highlighted)
        # Check for button presses on the main menu
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % num_buttons
                elif event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % num_buttons
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:  # New Game button is selected
                        show_name_input_screen = True
                        show_pet_select_screen = False
                        show_pet_summary_screen = False
                        show_battle_screen = False
            if event.type == pygame.QUIT:
                game_running = False




    #load game
    if show_load_game_screen:
        functions.select_save_file(functions.get_save_files())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False


    #new game
    if show_name_input_screen:

        # Show the name input screen
        functions.draw_text(screen, "Enter your name below...", screen_width // 2, screen_height // 4, 30, (255, 255, 255))
        text_box.centerx = screen.get_rect().centerx
        text_box.centery = screen.get_rect().centery
        pygame.draw.rect(screen, color, text_box, 4)
        surf = font.render(user_ip, True, 'orange')
        screen.blit(surf, (text_box.x + 5, text_box.y + 5))
        text_box.w = max(100, surf.get_width() + 10)
        functions.draw_button(screen, x, y + BUTTON_HEIGHT + 10, "Next", BUTTON_COLOR)

        # Handle key events for the text input box
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_ip = user_ip[:-1]
                    elif event.unicode.isalnum():
                        user_ip += event.unicode

            # Check if the "Next" button has been pressed
            if pygame.mouse.get_pressed()[0]:
                if x < mouse_pos[0] < x + BUTTON_WIDTH and y + BUTTON_HEIGHT + 10 < mouse_pos[
                    1] < y + 2 * BUTTON_HEIGHT + 10:
                    # Code for starting the game goes here
                    functions.draw_text(screen, f"Thanks {user_ip}. Next choose your Capsule Monster", screen_width // 2, screen_height // 4, 30,
                                        (255, 255, 255))
                    show_pet_select_screen = True
                    show_name_input_screen = False

    # Define the available pet species
    PET_SPECIES = ["Species 1", "Species 2", "Species 3", "Species 4"]

    # Show the pet select screen
    # Show the pet select screen
    if show_pet_select_screen:
        screen.fill((0, 0, 0))  # clear the screen
        functions.draw_text(screen, "Choose your Capsule Monster", screen_width // 2, screen_height // 4, 30,
                            (255, 255, 255))

        # Draw buttons for each available pet species
        for i, species in enumerate(SPECIES):
            button_x = x
            button_y = y + (i * (BUTTON_HEIGHT + 10)) + BUTTON_HEIGHT + 10
            functions.draw_button(screen, button_x, button_y, species, BUTTON_COLOR)


            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if a species button was clicked


                    if button_x < mouse_pos[0] < button_x + BUTTON_WIDTH and button_y < mouse_pos[
                        1] < button_y + BUTTON_HEIGHT:
                        pet_choice = species
                        player_pet = functions.create_player_pet(pet_choice, user_ip)

                        show_pet_summary_screen = True
                        show_pet_select_screen = False



    if show_pet_summary_screen:
        screen.fill((0, 0, 0))  # clear the screen
        functions.draw_text(screen, f"You chose {pet_choice}", screen_width // 2, ((screen_height // 2))-20, 30,(255, 255, 255))

        # Load pet image and draw it on the screen
        pet_img = pygame.image.load(f"art/small/{pet_choice}_small.png")
        screen.blit(pet_img,(screen_width // 2 - pet_img.get_width() // 2, screen_height // 4 - pet_img.get_height() // 2))

        # Draw the pet's name and stats
        functions.draw_text(screen, f"Name: {player_pet.name}", screen_width // 2, screen_height // 2, 20,
                            (255, 255, 255))
        functions.draw_text(screen, f"Level: {player_pet.level}", screen_width // 2, screen_height // 2 + 30, 20,
                            (255, 255, 255))
        functions.draw_text(screen, f"HP: {player_pet.current_hp}", screen_width // 2, screen_height // 2 + 60, 20,
                            (255, 255, 255))
        functions.draw_text(screen, f"Attack: {player_pet.attack}", screen_width // 2, screen_height // 2 + 90, 20,
                            (255, 255, 255))
        functions.draw_text(screen, f"Defense: {player_pet.defense}", screen_width // 2, screen_height // 2 + 120, 20,
                            (255, 255, 255))

        #back button
        back_button_x = x
        back_button_y = y + (BUTTON_HEIGHT + 10) + BUTTON_HEIGHT + 10 + (BUTTON_HEIGHT + 10)
        functions.draw_button(screen, back_button_x, back_button_y, 'BACK', BACK_BUTTON_COLOR)

        # next button
        button_x = x
        button_y = y + (BUTTON_HEIGHT + 10) + BUTTON_HEIGHT + 10
        functions.draw_button(screen, button_x, button_y, 'NEXT', BUTTON_COLOR)
        # Check for button presses on the pet select screen

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x < mouse_pos[0] < button_x + BUTTON_WIDTH and button_y < mouse_pos[
                    1] < button_y + BUTTON_HEIGHT:

                    show_battle_screen = True
                    show_pet_summary_screen = False
                elif back_button_x < mouse_pos[0] < back_button_x + BACK_BUTTON_WIDTH and back_button_y < mouse_pos[
                    1] < back_button_y + BACK_BUTTON_HEIGHT:
                    show_pet_select_screen = True
                    show_pet_summary_screen = False
            if event.type == pygame.QUIT:
                game_running = False



    if show_battle_screen:
        screen.fill((0, 0, 0))  # clear the screen
        functions.draw_text(screen, f"Start Battle!", screen_width // 2, screen_height // 4, 30,
                            (255, 255, 255))

    pygame.display.update()
    clock.tick(50)

