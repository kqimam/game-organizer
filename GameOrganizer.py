# Author: Kaiser Imam
# Last updated: 3/15/2022
# Description: Universal launcher for PC and console games stored on the user's system.  Allows users to launch games,
# view game details, and download a game description and cover art.  Each PC game can store multiple launch
# configurations which can be chosen at will by the user.

import os
import os.path
import random
import pickle
import subprocess
import textwrap
import socket
import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import urllib

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


class PCGameEntry:
    """
    Represents a game in the user's PC game collection with a title, source PC games platform, and default application
    path. The user can optionally download a description and cover art or store alternate launch configurations.
    """

    def __init__(self, title, source, application_path):
        """Creates a PCGameEntry object with the given title, source PC games service, and application path."""
        self._title = title
        self._source = source
        self._application_path = application_path
        self._last_played_date = ""
        self._description = ""
        self._cover_art_file = ""
        self._alternate_configs = []  # List of dictionary objects, each with a config title and path

    def get_title(self):
        """Returns the game entry's title."""
        return self._title

    def get_source(self):
        """Returns the game entry's source platform (Steam, Epic Games, GOG Galaxy, etc.)."""
        return self._source

    def get_application_path(self):
        """Returns the game entry's default application path."""
        return self._application_path

    def get_last_played_date(self):
        """Returns the date of the last time the game was played in the MM/DD/YYYY format."""
        return self._last_played_date

    def get_description(self):
        """Returns the game entry's description downloaded from Wikipedia."""
        return self._description

    def get_cover_art_file(self):
        """Returns the filename for the game's downloaded cover art image, if there is one."""
        return self._cover_art_file

    def get_alternate_configs(self):
        """Returns the list of alternate configurations for a given PC game."""
        return self._alternate_configs

    def set_title(self, input_title):
        """Updates the game's title to the input title string."""
        self._title = input_title

    def set_source(self, input_source):
        """Updates the game entry's source platform to the input source string."""
        self._source = input_source

    def set_application_path(self, input_application_path):
        """Updates the game's default application path to the input path string."""
        self._application_path = input_application_path

    def set_last_played_date(self):
        """Set the game entry's last played date to the current date when a game is played."""
        self._last_played_date = date.today().strftime("%m/%d/%y")

    def set_description(self, input_description):
        """Updates the game's description to the text received from the Wikipedia Scraper microservice."""
        self._description = input_description

    def set_cover_art_file(self, input_cover_art_file):
        """Updates the game entry's stored cover art filename to the input cover art filename."""
        self._cover_art_file = input_cover_art_file

    def add_alternate_config(self, config_dictionary):
        """Adds the received alternate configuration dictionary object to the game entry's list of alternate configs."""
        self._alternate_configs.append(config_dictionary)

    def update_alternate_config(self, index, config_dictionary):
        """Updates the alternate configuration at the received index position."""
        self._alternate_configs[index] = config_dictionary

    def delete_alternate_config(self, index):
        """Deletes the alternate configuration at the received index position."""
        del self._alternate_configs[index]

    # Class object export code adapted from
    # https://stackoverflow.com/questions/55584882/trying-to-save-a-class-in-a-list-to-a-file

    def dump_pc_game(self):
        """Condenses a PCGameEntry object into a list of attributes for use in storing the PC games list to a file."""
        return [self._title, self._source, self._application_path, self._last_played_date, self._description,
                self._cover_art_file, self._alternate_configs]

    @staticmethod
    def rebuild_pc_game_entry(attributes):
        """Returns a PCGameEntry object built from a list of attributes."""
        new_game = PCGameEntry(attributes[0], attributes[1], attributes[2])  # Create new PCGameEntry object
        new_game._last_played_date = attributes[3]
        new_game._description = attributes[4]
        new_game._cover_art_file = attributes[5]
        new_game._alternate_configs = attributes[6]

        return new_game


class ConsoleGameEntry:
    """
    Represents a game in the user's console game collection with a title, platform, emulator, and default ROM file.
    The user can optionally download a description and cover art or store alternate launch configurations.
    """

    def __init__(self, title, platform, emulator, default_rom):
        """Creates a ConsoleGameEntry object with the given title, platform, emulator, and default ROM file."""
        self._title = title
        self._platform = platform
        self._emulator = emulator
        self._default_rom = default_rom
        self._last_played_date = ""
        self._description = ""
        self._cover_art_file = ""
        self._alternate_roms = []  # List of dictionary objects, each with a ROM title and path

    def get_title(self):
        """Returns the game entry's title."""
        return self._title

    def get_platform(self):
        """Returns the game entry's platform."""
        return self._platform

    def get_emulator(self):
        """Returns the name of the game entry's emulator program."""
        return self._emulator

    def get_default_rom(self):
        """Returns the filename of the game entry's default ROM file."""
        return self._default_rom

    def get_last_played_date(self):
        """Returns the date of the last time the game was played in the MM/DD/YYYY format."""
        return self._last_played_date

    def get_description(self):
        """Returns the game entry's description downloaded from Wikipedia."""
        return self._description

    def get_cover_art_file(self):
        """Returns the filename for the game's downloaded cover art image, if there is one."""
        return self._cover_art_file

    def get_alternate_roms(self):
        """Returns the list of alternate ROM files for a given console game."""
        return self._alternate_roms

    def set_title(self, input_title):
        """Updates the game's title to the input title string."""
        self._title = input_title

    def set_platform(self, input_platform):
        """Updates the game entry's platform to the input platform string."""
        self._platform = input_platform

    def set_emulator(self, input_emulator):
        """Updates the game entry's emulator program to the input emulator name."""
        self._emulator = input_emulator

    def set_default_rom(self, input_default_rom):
        """Updates the game's default ROM filename to the input filename string."""
        self._default_rom = input_default_rom

    def set_last_played_date(self):
        """Set the game entry's last played date to the current date when a game is played."""
        self._last_played_date = date.today().strftime("%m/%d/%y")

    def set_description(self, input_description):
        """Updates the game's description to the text received from the Wikipedia Scraper microservice."""
        self._description = input_description

    def set_cover_art_file(self, input_cover_art_file):
        """Updates the game entry's stored cover art filename to the input cover art filename."""
        self._cover_art_file = input_cover_art_file

    def add_alternate_rom(self, rom_dictionary):
        """Adds the received alternate ROM file dictionary object to the game entry's list of alternate ROMs."""
        self._alternate_roms.append(rom_dictionary)


class GameOrganizerApp:
    """
    Represents a running instance of the Game Organizer app.
    """

    def __init__(self):
        """
        Initializes a new instance of the Game Organizer program.  Imports PC and console game collections if they have
        been saved to a file.  Otherwise, creates empty PC and console game lists.
        """

        # Class object import code adapted from
        # https://stackoverflow.com/questions/55584882/trying-to-save-a-class-in-a-list-to-a-file

        if os.path.isfile('pc_games_list.pkl'):  # If the PC games collection has previously been saved to a file
            with open('pc_games_list.pkl', 'rb') as infile:
                self._pc_games_list = [PCGameEntry.rebuild_pc_game_entry(attributes) for attributes in
                                       pickle.load(infile)]
        else:
            self._pc_games_list = []  # List of PCGameEntry objects that represents PC games in the user's collection

        self._console_games_list = []  # List of ConsoleGameEntry objects for console games in the user's collection
        self._selected_game_index = -1

        # Create an "images" folder in the root directory if one does not already exist
        if not os.path.isdir("./images"):
            os.mkdir("images")

    # Methods used for both PC and console games

    def game_organizer(self):
        """Runs a new instance of the Game Organizer program."""
        print("\nGame Organizer")

        self.top_level_menu()

    def top_level_menu(self):
        """Displays the top level menu with choices to view games lists, add a game, or exit the program."""
        choice_string = ''

        print("\nMain Menu")
        print("1. View PC Games")
        print("2. View Console Games")
        print("3. Add a Game")
        print("4. Exit Program")

        choice_string = input()

        if choice_string == '1':
            self.view_pc_games()
        elif choice_string == '2':
            self.view_console_games()
        elif choice_string == '3':
            self.add_new_game_menu()
        elif choice_string == '4':
            exit()

    def add_new_game_menu(self):
        """Displays the menu to allow the user to add a new PC or console game."""
        choice_string = ''

        print("\nAdd a New Game")
        print("1. Add a PC Game")
        print("2. Add a Console Game")
        print("3. Go back to the Main Menu")

        choice_string = input()

        if choice_string == '1':
            self.new_pc_game()
        elif choice_string == '2':
            self.new_console_game()
        elif choice_string == '3':
            self.top_level_menu()

    def get_selected_game_index(self):
        """Returns the index value of the game currently selected by the user."""
        return self._selected_game_index

    def set_selected_game_index(self, num):
        """Sets the selected game index to the received number."""
        self._selected_game_index = num

    def download_game_description(self, game_name):
        """Connects to the Wikipedia Scraper microservice and downloads a 1-paragraph description."""
        # Connect to the Wikipedia Scraper microservice
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)

        # Send the name of the currently selected game to the server
        client_socket.send(game_name)

        # Receive a single paragraph description from the Wikipedia Scraper service
        received_description = client_socket.recv(2048).decode(FORMAT)

        # Close the connection
        client_socket.close()

        return received_description

    def download_cover_art(self, game_name):
        """Connects to the Image Scraper microservice and downloads a cover art image."""

        # Query the Image Scraper microservice for a link to the game's cover art
        search_query = "https://us-central1-osu-project-342203.cloudfunctions.net/image-generator?query=" + \
                       urllib.parse.quote_plus(game_name) + "+cover&size=large"

        # Receive a URL linking to the image file
        search_response = requests.get(search_query, auth=HTTPBasicAuth('admin_T42', 'admin_T42'))
        image_link_text = search_response.text  # Remove extra characters from the front and end of the received string
        temp_string = image_link_text[8:]
        image_link = temp_string[:-2]

        # Download the cover art image to the "images" folder
        download_image_response = requests.get(image_link)
        output_path_temp = "./images/" + game_name + ".png"
        output_path = output_path_temp.replace(" ", "_")

        file = open(output_path, "wb")
        file.write(download_image_response.content)
        file.close()

        return output_path

    # Methods related to the PC games collection

    def get_pc_games_list(self):
        """Returns the list of stored PC games."""
        return self._pc_games_list

    def save_pc_games_list(self):
        """Exports the PC games list to a Python pickle file in the local directory."""
        with open('pc_games_list.pkl', 'wb') as outfile:
            pickle.dump([i.dump_pc_game() for i in self.get_pc_games_list()], outfile)

    def view_pc_games(self):
        """
        Displays the list of PC games available.  Allows the user to choose a game and either play it or view its
        details.  Also includes an option to select a random game or go back to the top level menu.
        """
        choice_string = ''
        display_index = 1

        print("\nPC Games List")  # Print numbered list of games
        for current_game in self.get_pc_games_list():
            print(str(display_index) + ". " + current_game.get_title())
            display_index += 1

        print("\nPlease enter the number of the game you would like to view.")
        print("Enter 'R' to select a random game.")
        print("Enter 'B' to go back to the Main Menu.")

        choice_string = input()

        if choice_string.lower() == 'r':
            self.select_random_pc_game()
        elif choice_string.lower() == 'b':
            self.set_selected_game_index(-1)
            self.top_level_menu()
        else:
            self.set_selected_game_index(int(choice_string) - 1)
            self.view_pc_game_details()

    def view_pc_game_details(self):
        """
        After the user selects a game from the PC games list, displays a menu with the options to play the game
        or view/edit the game's stored details.
        """
        choice_string = ''

        print("\n" + self.get_pc_games_list()[self._selected_game_index].get_title() + " Details")
        print("1. Play Default Configuration")
        print("2. View Alternate Configurations")
        print("3. View Basic Game Information")
        print("4. View Game Description")
        print("5. View Cover Art")
        print("6. Edit Game Entry")
        print("7. Delete Game Entry")
        print("8. Go Back to PC Games List")

        choice_string = input()

        if choice_string == '1':
            self.run_default_config_pc()
        elif choice_string == '2':
            self.view_alternate_configs_pc()
        elif choice_string == '3':
            self.view_basic_game_info_pc()
        elif choice_string == '4':
            self.view_game_description_pc()
        elif choice_string == '5':
            self.view_cover_art_pc()
        elif choice_string == '6':
            self.edit_pc_game()
        elif choice_string == '7':
            self.delete_pc_game()
        elif choice_string == '8':
            self.set_selected_game_index(-1)
            self.view_pc_games()

    def add_pc_game(self, game_entry_object):
        """Adds the received PC game entry object to the list of PC games."""
        self._pc_games_list.append(game_entry_object)

    def new_pc_game(self):
        """Displays the menu to add a new PC game."""
        print("\nPlease enter the following information for the new game.")
        game_title = input("\nGame Title: ")
        source_platform = input("\nSource Platform: ")
        application_path = input("\nApplication Path: ")

        # Create a PCGameEntry object for the game
        new_game = PCGameEntry(game_title, source_platform, application_path)

        # Register the received application path as the default command in the alternate configs list
        new_game.add_alternate_config({"title": game_title, "path": application_path})

        # Add the new game to the PC games collection
        self.add_pc_game(new_game)
        self.sort_pc_games()  # Sort the PC games list after a new game is appended to the end
        self.save_pc_games_list()  # Save the PC games list file after a new game is added

        print("\nAdded " + game_title + " to the PC games collection.")
        self.view_pc_games()

    def sort_pc_games(self):
        """Sorts the PC games list by game title whenever a game is added."""
        self.get_pc_games_list().sort(key=self.get_pc_game_entry_title)

    def get_pc_game_entry_title(self, game):
        """
        Used in the self.sort_pc_games method for sorting the games list. Receives a PCGameEntry object and returns
        the game's title.
        """
        return game.get_title()

    def edit_pc_game(self):
        """Edit the details of a PC game entry."""
        print("\nEdit Details for " + self.get_pc_games_list()[self._selected_game_index].get_title())
        print("\nCurrent Title: " + self.get_pc_games_list()[self._selected_game_index].get_title())
        print("\nCurrent Source Platform: " + self.get_pc_games_list()[self._selected_game_index].get_source())
        print("\nCurrent Application Path: " + self.get_pc_games_list()[self._selected_game_index].
              get_application_path())

        choice_string = ''

        print("\n1. Edit Title")
        print("2. Edit Source Platform")
        print("3. Edit Application Path")
        print("4. Go back to Game Details Menu for " + self.get_pc_games_list()[
            self._selected_game_index].get_title())

        choice_string = input()

        if choice_string == '1':
            self.edit_title_pc()
        elif choice_string == '2':
            self.edit_source_platform_pc()
        elif choice_string == '3':
            self.edit_application_path_pc()
        elif choice_string == '4':
            self.view_pc_game_details()

    def edit_title_pc(self):
        """
        Displays a menu to edit the currently selected game's title. Saves the PC games list to a local file after
        each edit.
        """
        print("\nCurrent Title: " + self.get_pc_games_list()[self._selected_game_index].get_title() + "\n")
        new_title = input("New Title: ")

        # Save the new title to the game's entry
        self.get_pc_games_list()[self._selected_game_index].set_title(new_title)
        self.save_pc_games_list()  # Save the PC games list file after an edit is made

        # Go back to the Edit Game menu
        self.edit_pc_game()

    def edit_source_platform_pc(self):
        """
        Displays a menu to edit the currently selected game's source platform. Saves the PC games list to a local file
        after each edit.
        """
        print("\nCurrent Source Platform: " + self.get_pc_games_list()[self._selected_game_index].get_source() + "\n")
        new_source_platform = input("New Source Platform: ")

        # Save the new source platform to the game's entry
        self.get_pc_games_list()[self._selected_game_index].set_source(new_source_platform)
        self.save_pc_games_list()  # Save the PC games list file after an edit is made

        # Go back to the Edit Game menu
        self.edit_pc_game()

    def edit_application_path_pc(self):
        """
        Displays a menu to edit the currently selected game's application path. Saves the PC games list to a local file
        after each edit.
        """
        print("\nCurrent Application Path: " + self.get_pc_games_list()[self._selected_game_index].
              get_application_path() + "\n")
        new_application_path = input("New Application Path: ")

        # Save the new application path to the game's entry
        self.get_pc_games_list()[self._selected_game_index].set_application_path(new_application_path)
        self.save_pc_games_list()  # Save the PC games list file after an edit is made

        # Go back to the Edit Game menu
        self.edit_pc_game()

    def delete_pc_game(self):
        """Displays a menu to delete the currently selected game from the list of PC games."""
        choice_string = ''
        game_name = self.get_pc_games_list()[self._selected_game_index].get_title()

        print("\nAre you sure you wish to permanently delete " + game_name + "?")
        print("Please enter 'Y' for Yes or 'N' for No.")

        choice_string = input()

        if choice_string.lower() == 'y':
            del self.get_pc_games_list()[self._selected_game_index]
            self.save_pc_games_list()  # Save the PC games list file after an entry is deleted

            print("\nDeleted " + game_name + ".\n")
            self.set_selected_game_index(-1)
            self.view_pc_games()
        elif choice_string.lower() == 'n':
            self.view_pc_game_details()

    def select_random_pc_game(self):
        """Returns the index of a random game from the PC games list."""
        list_length = len(self.get_pc_games_list())

        random_game_index = random.randint(0, list_length - 1)  # Pick a random index from 0 to the list length

        self.set_selected_game_index(random_game_index)
        self.view_pc_game_details()

    def go_back_menu_pc(self):
        """Presents the user with choices to go back to the Game Details menu, PC Games List, or Main Menu."""

        choice_string = ''

        print("1. Go back to Game Details Menu for " + self.get_pc_games_list()[
            self._selected_game_index].get_title())
        print("2. Go back to PC Games List")
        print("3. Go back to Main Menu")

        choice_string = input()

        if choice_string == '1':
            self.view_pc_game_details()
        elif choice_string == '2':
            self.set_selected_game_index(-1)
            self.view_pc_games()
        elif choice_string == '3':
            self.set_selected_game_index(-1)
            self.top_level_menu()

    def run_default_config_pc(self):
        """Run the default configuration for a PC game."""

        # Format the game's application path for use in the launch command
        raw_string = r"{}".format(self.get_pc_games_list()[self._selected_game_index].get_application_path())

        subprocess.Popen(raw_string)  # Execute the currently selected game
        self.get_pc_games_list()[self._selected_game_index].set_last_played_date()  # Set to the current date
        self.save_pc_games_list()  # Save the PC games list file in order to save the last played date

        print("\nNow running " + self.get_pc_games_list()[self._selected_game_index].get_title() + "\n")

        self.go_back_menu_pc()  # Go back to any previous menu

    def view_alternate_configs_pc(self):
        """Displays the details menu for a PC game's registered alternate configurations."""
        choice_string = ''
        display_index = 1

        # Display numbered list of alternate configurations
        print("\nAlternate Configurations for " + self.get_pc_games_list()[self._selected_game_index].get_title())
        for item in self.get_pc_games_list()[self._selected_game_index].get_alternate_configs():
            print(str(display_index) + ". " + item["title"])
            display_index += 1

        print("\nPlease enter the number of the configuration you would like to play.")
        print("Enter 'A' to add a new configuration.")
        print("Enter 'E' to edit a configuration.")
        print("Enter 'D' to delete a configuration.")
        print("Enter 'H' to view an explanation of the Alternate Configurations feature.")
        print("Enter 'B' to go back to the previous menu.")

        choice_string = input()

        if choice_string.lower() == 'a':
            self.new_alternate_config_pc()
        elif choice_string.lower() == 'e':
            self.edit_alternate_config_pc_menu_1()
        elif choice_string.lower() == 'd':
            self.delete_alternate_config_pc_menu()
        elif choice_string.lower() == 'h':
            self.view_alternate_config_explanation()
        elif choice_string.lower() == 'b':
            self.view_pc_game_details()
        else:  # Run the selected alternate configuration
            self.run_alternate_config_pc(int(choice_string) - 1)
            self.go_back_menu_pc()

    def run_alternate_config_pc(self, selected_config_index):
        """Runs an alternate configuration for a PC game."""
        # Format the game's application path for use in the launch command
        raw_string = r"{}".format(
            self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[selected_config_index][
                "path"])
        subprocess.Popen(raw_string)
        self.get_pc_games_list()[self._selected_game_index].set_last_played_date()  # Set to the current date
        self.save_pc_games_list()  # Save the PC games list file in order to save the last played date

        print("\nNow running " + self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[
            selected_config_index]["title"] + "\n")

    def new_alternate_config_pc(self):
        """Displays the menu to add a new launch configuration for a PC game."""
        print("\nPlease enter the following information for the new launch configuration.")
        config_title = input("\nConfiguration Title: ")
        application_path = input("\nApplication Path: ")

        # Create a config dictionary for the game
        new_config = {"title": config_title, "path": application_path}

        # Add the new config to the alternate configs list
        self.get_pc_games_list()[self._selected_game_index].add_alternate_config(new_config)
        self.save_pc_games_list()  # Save the PC games list file after a new config is added

        print("\nAdded " + config_title + " to the alternate configurations list.\n")
        self.view_alternate_configs_pc()

    def edit_alternate_config_pc_menu_1(self):
        """Displays the menu to choose an alternate configuration to edit."""
        choice_string = ''
        display_index = 1

        # Display numbered list of alternate configurations
        print("Edit an Alternate Configuration for " + self.get_pc_games_list()[self._selected_game_index].get_title())
        for item in self.get_pc_games_list()[self._selected_game_index].get_alternate_configs():
            print(str(display_index) + ". " + item["title"])
            display_index += 1

        print("\nPlease enter the number of the configuration you would like to edit.")
        print("Enter 'B' to go back to the previous menu.")

        choice_string = input()

        if choice_string.lower() == 'b':
            self.view_alternate_configs_pc()
        else:  #
            self.edit_alternate_config_pc_menu_2(int(choice_string) - 1)

    def edit_alternate_config_pc_menu_2(self, config_index):
        """Displays the menu to edit a configuration's fields."""
        config_title = \
            self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[config_index]["title"]

        print("\nEdit Details for " + config_title)
        print("\nCurrent Title: " + config_title)
        print("\nCurrent Application Path: "
              + self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[config_index]["path"])

        choice_string = ''

        print("\n1. Edit Title")
        print("2. Edit Application Path")
        print("3. Go back to the previous menu")

        choice_string = input()

        if choice_string == '1':
            self.edit_config_title_pc(config_index)
        elif choice_string == '2':
            self.edit_config_application_path_pc(config_index)
        elif choice_string == '3':
            self.edit_alternate_config_pc_menu_1()

    def edit_config_title_pc(self, config_index):
        """
        Displays a menu to edit the currently selected configuration's's title.
        """
        print("\nCurrent Title: " +
              self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[config_index]["title"] + "\n")
        new_title = input("New Title: ")

        # Create a temporary dictionary with the new details which will replace the current configuration
        new_config = {"title": new_title,
                      "path": self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[config_index][
                          "path"]}

        # Save the edited configuration
        self.get_pc_games_list()[self._selected_game_index].update_alternate_config(config_index, new_config)
        self.save_pc_games_list()  # Save the PC games list file after an edit is made

        self.edit_alternate_config_pc_menu_2(config_index)

    def edit_config_application_path_pc(self, config_index):
        """
        Displays a menu to edit the currently selected configuration's's application path.
        """
        print("\nCurrent Application Path: " +
              self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[config_index]["path"] + "\n")
        new_application_path = input("New Application Path: ")

        # Create a temporary dictionary with the new details which will replace the current configuration
        new_config = {
            "title": self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[config_index]["title"],
            "path": new_application_path}

        # Save the edited configuration
        self.get_pc_games_list()[self._selected_game_index].update_alternate_config(config_index, new_config)
        self.save_pc_games_list()  # Save the PC games list file after an edit is made

        self.edit_alternate_config_pc_menu_2(config_index)

    def delete_alternate_config_pc_menu(self):
        """Displays the menu to delete an alternate configuration for a PC game."""
        choice_string = ''
        display_index = 1

        # Display numbered list of alternate configurations
        print("Alternate Configurations for " + self.get_pc_games_list()[self._selected_game_index].get_title())
        for item in self.get_pc_games_list()[self._selected_game_index].get_alternate_configs():
            print(str(display_index) + ". " + item["title"])
            display_index += 1

        print("\nPlease enter the number of the configuration you would like to delete.")
        print("Enter 'B' to go back to the previous menu.")

        choice_string = input()

        if choice_string.lower() == 'b':
            self.view_alternate_configs_pc()
        else:  # Delete the selected alternate configuration
            self.delete_alternate_config_pc(int(choice_string) - 1)

    def delete_alternate_config_pc(self, index):
        """Deletes an alternate configuration for a PC game."""
        choice_string = ''
        config_name = self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[index]["title"]

        print("\nAre you sure you wish to permanently delete " + config_name + "?")
        print("Please enter 'Y' for Yes or 'N' for No.")

        choice_string = input()

        if choice_string.lower() == 'y':
            self.get_pc_games_list()[self._selected_game_index].delete_alternate_config(index)
            self.save_pc_games_list()  # Save the PC games list file after an entry is deleted

            print("\nDeleted " + config_name + ".\n")
            self.view_alternate_configs_pc()
        elif choice_string.lower() == 'n':
            self.view_alternate_configs_pc()

    def view_alternate_config_explanation(self):
        """Displays a short description of the Alternate Configurations feature to help new users."""
        print("\nThe Alternate Configurations feature allows users to register multiple alternate launch commands")
        print("for a PC game, each with a title and application path.")
        print("\nExamples of alternate launch commands include secondary executables and mod organizers.")
        print("\nThe default application path for a PC game is always listed as Alternate Configuration #1.\n")
        self.view_alternate_configs_pc()

    def view_basic_game_info_pc(self):
        """
        Displays the game title, source platform, date the game was last played, and the default application path.
        """
        print("\n" + self.get_pc_games_list()[self._selected_game_index].get_title() + " Basic Information")
        print("\nTitle: " + self.get_pc_games_list()[self._selected_game_index].get_title())
        print("\nSource Platform: " + self.get_pc_games_list()[self._selected_game_index].get_source())

        if self.get_pc_games_list()[self._selected_game_index].get_last_played_date() == '':
            print("\nLast Played: Never")
        else:
            print("\nLast Played: " + self.get_pc_games_list()[self._selected_game_index].get_last_played_date())

        print("\nDefault Application Path: " + self.get_pc_games_list()[self._selected_game_index].
              get_application_path() + "\n")

        self.go_back_menu_pc()

    def view_game_description_pc(self):
        """
        Displays the stored PC game description if one exists, or offers the user the choice to download a description
        from Wikipedia.
        """
        # If a game description has already been downloaded from Wikipedia, display it
        if self.get_pc_games_list()[self._selected_game_index].get_description() != '':
            print("\n" + textwrap.fill(self.get_pc_games_list()[self._selected_game_index].get_description(), 140)
                  + "\n")

            self.go_back_menu_pc()

        # If there is currently no stored game description
        else:
            choice_string = ''

            print("\nThere is currently no description stored for this game.")
            print("\nWould you like to download the game description from Wikipedia?")
            print("Please enter 'Y' for Yes or 'N for No.")

            choice_string = input()

            if choice_string.lower() == 'y':
                # Download a description from Wikipedia
                description = self.download_game_description(self.get_pc_games_list()[self._selected_game_index].
                                                             get_title().encode(FORMAT))

                # Store the received description
                self.get_pc_games_list()[self._selected_game_index].set_description(description)
                self.save_pc_games_list()  # Save the PC games list file

                # Print the newly downloaded description
                print(textwrap.fill(self.get_pc_games_list()[self._selected_game_index].get_description(), 140) + "\n")

                self.go_back_menu_pc()

            elif choice_string.lower() == 'n':
                self.view_pc_game_details()

    def view_cover_art_pc(self):
        """
        Displays a menu to open a game's cover art if one is stored, or download one online.
        """
        # If a cover art image has already been downloaded for the current game
        if self.get_pc_games_list()[self._selected_game_index].get_cover_art_file() != '':
            print("\nView Cover Art")
            self.display_cover_art_pc()

        # If there is currently no stored cover art file
        else:
            choice_string = ''

            print("\nThere is currently no cover art for this game.")
            print("\nWould you like to download a cover art image?")
            print("Please enter 'Y' for Yes or 'N for No.")

            choice_string = input()

            if choice_string.lower() == 'y':
                # Download a cover art image using the Image Scraper microservice
                file_path = self.download_cover_art(self.get_pc_games_list()[self._selected_game_index].get_title())

                # Save the path of the downloaded image file in the game's entry
                self.get_pc_games_list()[self._selected_game_index].set_cover_art_file(file_path)
                self.save_pc_games_list()  # Save the PC games list file

                # Inform the user that a cover art image has been downloaded and give them a choice to open it
                print("\nDownloaded Cover Art for " + self.get_pc_games_list()[self._selected_game_index].get_title()
                      + ".")
                self.display_cover_art_pc()

            elif choice_string.lower() == 'n':
                self.view_pc_game_details()

    def display_cover_art_pc(self):
        """Allows the user to open a stored cover art image in Windows Photo Viewer."""
        choice_string = ''

        print("1. Open cover art image in Windows Photo Viewer")
        print("2. Go back to Game Details Menu for " + self.get_pc_games_list()[
            self._selected_game_index].get_title())

        choice_string = input()

        if choice_string == '1':  # Open image in Windows Photo Viewer
            os.system("start " + self.get_pc_games_list()[self._selected_game_index].get_cover_art_file())
            self.view_pc_game_details()
        elif choice_string == '2':
            self.view_pc_game_details()

    # Methods related to the console games collection

    def get_console_games_list(self):
        """Returns the list of stored console games."""
        return self._console_games_list

    def add_console_game(self, game_entry_object):
        """Adds the received console game entry object to the list of console games."""
        self._console_games_list.append(game_entry_object)

    def edit_console_game(self, game_index):
        """Edit the details of the console game entry with the received index from the list of console games."""
        # TODO: edit console game

    def delete_console_game(self, game_index):
        """Removes the console game entry with the received index from the list of console games."""
        # TODO: delete console game

    def new_console_game(self):
        """Displays the menu to add a new console game."""
        # TODO: implement add games menu.  Add a game, then sort list by game title

    def view_console_games(self):
        """
        Displays the list of console games available.  Allows the user to choose a game and either play it or view its
        details.  Also includes an option to select a random game or go back to the top level menu.
        """
        # TODO: view console games

    def select_random_console_game(self):
        """Returns the index of a random game from the console games list."""
        # TODO: select random game

    # Methods for testing purposes only

    def create_sample_data(self):
        """Creates a list of sample PC game entries for testing purposes only."""
        # Game #1
        self.add_pc_game(PCGameEntry("AM2R", "Steam", "D:\Program Files\AM2R_15\AM2R.exe"))
        self.get_pc_games_list()[0].add_alternate_config({"title": "AM2R", "path": "D:\Program Files\AM2R_15.exe"})
        self.get_pc_games_list()[0].set_description(
            "AM2R (Another Metroid 2 Remake) is an action-adventure game developed by Argentinian programmer Milton "
            "Guasti (also known as DoctorM64) and released on August 6, 2016, Metroid's 30th anniversary. It was "
            "originally released for Windows. It is an unofficial remake of the 1991 Game Boy game Metroid II: "
            "Return of Samus in the style of Metroid: Zero Mission (2004). As in the original Metroid II, players "
            "control bounty hunter Samus Aran, who aims to eradicate the parasitic Metroids. AM2R adds several "
            "features, including new graphics and music, new areas and bosses, altered controls, and a map system.\n"
            "The game received positive reviews, particularly for its improved visuals. It was nominated for The Game "
            "Awards 2016, but was later dropped from the nominee list without notice. Shortly after release, Nintendo "
            "sent DMCA notices to websites hosting AM2R, and download links were removed. Though Guasti planned to "
            "continue working on the game privately, in September 2016, he ended development after receiving a DMCA "
            "takedown request. Nintendo released an official Metroid II remake, Metroid: Samus Returns, in 2017.")
        self.get_pc_games_list()[0].set_cover_art_file("./images/AM2R.png")

        # Game #2
        self.add_pc_game(PCGameEntry("DOOM Eternal", "Steam", "steam://rungameid/782330"))
        self.get_pc_games_list()[1].add_alternate_config({"title": "DOOM Eternal", "path": "steam://rungameid/782330"})

        # Game #3
        self.add_pc_game(PCGameEntry("Red Dead Redemption 2", "Epic Games Launcher",
                                     "com.epicgames.launcher://apps/b30b6d1b4dfd4dcc93b5490be5e094e5%3A22a7b503221442da"
                                     "a2fb16ad37b6ccbf%3AHeather?action=launch&silent=true"))
        self.get_pc_games_list()[2].add_alternate_config({"title": "Red Dead Redemption 2",
                                                          "path": "com.epicgames.launcher://apps/b30b6d1b4dfd4dcc93b549"
                                                                  "0be5e094e5%3A22a7b503221442daa2fb16ad37b6ccbf%3AHea"
                                                                  "ther?action=launch&silent=true"})

        # Game #4
        self.add_pc_game(PCGameEntry("Stardew Valley", "Steam", "steam://rungameid/413150"))
        self.get_pc_games_list()[3].add_alternate_config({"title": "Stardew Valley",
                                                          "path": "steam://rungameid/413150"})

        # Game #5
        self.add_pc_game(PCGameEntry("The Elder Scrolls III: Morrowind", "Steam", "steam://rungameid/22321"))
        self.get_pc_games_list()[4].add_alternate_config({"title": "The Elder Scrolls III: Morrowind",
                                                          "path": "steam://rungameid/22321"})
        self.get_pc_games_list()[4].add_alternate_config({"title": "Mod List 1",
                                                          "path": "H:\Games\MOISE\ModOrganizer.exe"})
        self.get_pc_games_list()[4].add_alternate_config({"title": "Mod List 2",
                                                          "path": "H:\Games\MOISE\ModOrganizer.exe"})

        # Game #6
        self.add_pc_game(PCGameEntry("The Elder Scrolls V: Skyrim", "Steam", "steam://rungameid/489831"))
        self.get_pc_games_list()[5].add_alternate_config({"title": "The Elder Scrolls V: Skyrim",
                                                          "path": "steam://rungameid/22321"})
        self.get_pc_games_list()[5].add_alternate_config({"title": "Mod List 1",
                                                          "path": "H:\Games\QWEST\ModOrganizer.exe"})

        # Game #7
        self.add_pc_game(PCGameEntry("The Witcher III: Wild Hunt", "GOG Galaxy", "test string"))
        self.get_pc_games_list()[6].add_alternate_config({"title": "The Witcher III: Wild Hunt",
                                                          "path": "test string"})


if __name__ == '__main__':
    test_run = GameOrganizerApp()
    # test_run.create_sample_data()
    test_run.game_organizer()
