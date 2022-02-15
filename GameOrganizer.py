# Author: Kaiser Imam
# Date: 2/13/2021
# Description: TODO Description

import os
import subprocess
import textwrap


class PCGameEntry:
    """
    TODO Description
    """

    def __init__(self, title, source, application_path):
        """Creates a PCGameEntry object with the given title, source PC games service, and application path."""
        self._title = title
        self._source = source
        self._application_path = application_path
        self._last_played_date = ""
        self._description = ""
        self._cover_art_file = ""
        self._alternate_configs = []

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
        # TODO: Set last played date to current date

    def set_description(self, input_description):
        """Updates the game's description to the text input received from the Wikipedia Scraper microservice."""
        self._description = input_description

    def set_cover_art_file(self, input_cover_art_file):
        """Updates the game entry's stored cover art filename to the input cover art filename."""
        self._cover_art_file = input_cover_art_file

    def rename_cover_art_file(self):
        """Renames the game's cover art file received from the Image Scraper microservice to the title of the game."""
        # TODO: rename cover art file

    def add_alternate_config(self, config_dictionary):
        """Adds the received alternate configuration dictionary object to the game entry's list of alternate configs."""
        self._alternate_configs.append(config_dictionary)


class ConsoleGameEntry:
    """
    TODO Description
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
        self._alternate_roms = []

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

    def get_alternate_configs(self):
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
        # TODO: Set last played date to current date

    def set_description(self, input_description):
        """Updates the game's description to the text input received from the Wikipedia Scraper microservice."""
        self._description = input_description

    def set_cover_art_file(self, input_cover_art_file):
        """Updates the game entry's stored cover art filename to the input cover art filename."""
        self._cover_art_file = input_cover_art_file

    def rename_cover_art_file(self):
        """Renames the game's cover art file received from the Image Scraper microservice to the title of the game."""
        # TODO: rename cover art file

    def add_alternate_rom(self, rom_dictionary):
        """Adds the received alternate ROM file dictionary object to the game entry's list of alternate ROMs."""
        self._alternate_roms.append(rom_dictionary)


class GameOrganizerApp:
    """
    TODO Description
    """

    def __init__(self):
        """Initializes a new instance of the Game Organizer program with empty game lists."""
        self._pc_games_list = []  # List of PCGameEntry objects that represents PC games in the user's collection
        self._console_games_list = []  # List of ConsoleGameEntry objects for console games in the user's collection
        self._still_running = 1
        self._selected_game_index = -1

    def get_pc_games_list(self):
        """Returns the list of stored PC games."""
        return self._pc_games_list

    def get_console_games_list(self):
        """Returns the list of stored console games."""
        return self._console_games_list

    def add_pc_game(self, game_entry_object):
        """Adds the received PC game entry object to the list of PC games."""
        self._pc_games_list.append(game_entry_object)

    def edit_pc_game(self, game_index):
        """Edit the details of the PC game entry with the received index from the list of PC games."""
        # TODO: edit PC game

    def delete_pc_game(self, game_index):
        """Removes the PC game entry with the received index from the list of PC games."""
        # TODO: delete PC game

    def add_console_game(self, game_entry_object):
        """Adds the received console game entry object to the list of console games."""
        self._console_games_list.append(game_entry_object)

    def edit_console_game(self, game_index):
        """Edit the details of the console game entry with the received index from the list of console games."""
        # TODO: edit console game

    def delete_console_game(self, game_index):
        """Removes the console game entry with the received index from the list of console games."""
        # TODO: delete console game

    def get_selected_game_index(self):
        """Returns the index value of the game selected by the user."""
        return self._selected_game_index

    def set_selected_game_index(self, num):
        """Sets the selected game index to the received number."""
        self._selected_game_index = num

    def game_organizer(self):
        """Runs a new instance of the game organizer program."""
        print("Game Organizer\n")

        # while self._still_running == 1:
        #     self.top_level_menu()

        self.top_level_menu()

    def top_level_menu(self):
        """Displays the top level menu with choices to view games lists, add a game, or exit the program."""
        choice_string = ''

        print("Main Menu")
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
            self.new_game()
        elif choice_string == '4':
            # self._still_running = 0
            exit()

    def view_pc_games(self):
        """
        Displays the list of PC games available.  Allows the user to choose a game and either play it or view its
        details.  Also includes an option to select a random game or go back to the top level menu.
        """
        choice_string = ''
        display_index = 1

        print("PC Games List")
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

    def view_console_games(self):
        """
        Displays the list of console games available.  Allows the user to choose a game and either play it or view its
        details.  Also includes an option to select a random game or go back to the top level menu.
        """
        # TODO: view console games

    def new_game(self):
        """Displays the menu to add a PC or console game."""
        # TODO: implement add games menu.  Add a game, then sort list by game title

    def select_random_pc_game(self):
        """Returns the index of a random game from the PC games list."""
        # TODO: select random game

    def select_random_console_game(self):
        """Returns the index of a random game from the console games list."""
        # TODO: select random game

    def view_pc_game_details(self):
        """
        After the user selects a game from the PC games list, displays a menu with the options to play the game
        or view/edit the game's stored details.
        """
        choice_string = ''

        print(self.get_pc_games_list()[self._selected_game_index].get_title() + " Details")
        print("1. Play Default Configuration")
        print("2. View Alternate Configurations")
        print("3. View Game Description")
        print("4. View Cover Art")
        print("5. Edit Game Entry")
        print("6. Delete Game Entry")
        print("7. Go Back to PC Games List")

        choice_string = input()

        # Choice 1: Play default configuration
        if choice_string == '1':
            # Run the default configuration
            raw_string = r"{}".format(self.get_pc_games_list()[self._selected_game_index].get_application_path())
            subprocess.Popen(raw_string)

            print("\nNow running " + self.get_pc_games_list()[self._selected_game_index].get_title() + "\n")

            # Choice to go back to any previous menu
            choice_string_2 = ''

            print("1. Go back to Game Details Menu for " + self.get_pc_games_list()[
                self._selected_game_index].get_title())
            print("2. Go back to PC Games List")
            print("3. Go back to Main Menu")

            choice_string_2 = input()

            if choice_string_2 == '1':
                self.view_pc_game_details()
            elif choice_string_2 == '2':
                self.set_selected_game_index(-1)
                self.view_pc_games()
            elif choice_string_2 == '3':
                self.set_selected_game_index(-1)
                self.top_level_menu()

        # Choice 2: View the alternate configurations for the currently selected game
        elif choice_string == '2':
            choice_string_2 = ''
            display_index = 1

            print("Alternate Configurations for " + self.get_pc_games_list()[self._selected_game_index].get_title())
            for item in self.get_pc_games_list()[self._selected_game_index].get_alternate_configs():
                print(str(display_index) + ". " + item["title"])
                display_index += 1

            print("\nPlease enter the number of the configuration you would like to play.")
            print("Enter 'B' to go back to the previous menu.")

            choice_string_2 = input()

            if choice_string_2.lower() == 'b':
                self.view_pc_game_details()
            else:
                selected_config_index = int(choice_string_2) - 1

                # Run the selected configuration
                raw_string = r"{}".format(
                    self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[selected_config_index][
                        "path"])
                subprocess.Popen(raw_string)

                print("\nNow running " + self.get_pc_games_list()[self._selected_game_index].get_alternate_configs()[
                    selected_config_index]["title"] + "\n")

                # Choice to go back to any previous menu
                choice_string_3 = ''

                print("1. Go back to Game Details Menu for " + self.get_pc_games_list()[
                    self._selected_game_index].get_title())
                print("2. Go back to PC Games List")
                print("3. Go back to Main Menu")

                choice_string_3 = input()

                if choice_string_3 == '1':
                    self.view_pc_game_details()
                elif choice_string_3 == '2':
                    self.set_selected_game_index(-1)
                    self.view_pc_games()
                elif choice_string_3 == '3':
                    self.set_selected_game_index(-1)
                    self.top_level_menu()

        # Choice 3: View game description from Wikipedia
        elif choice_string == '3':
            # If a game description has already been downloaded from Wikipedia
            if self.get_pc_games_list()[self._selected_game_index].get_description() != '':
                print(textwrap.fill(self.get_pc_games_list()[self._selected_game_index].get_description(), 140))

                # Choice to go back to any previous menu
                choice_string_2 = ''

                print("\n1. Go back to Game Details Menu for " + self.get_pc_games_list()[
                    self._selected_game_index].get_title())
                print("2. Go back to PC Games List")
                print("3. Go back to Main Menu")

                choice_string_2 = input()

                if choice_string_2 == '1':
                    self.view_pc_game_details()
                elif choice_string_2 == '2':
                    self.set_selected_game_index(-1)
                    self.view_pc_games()
                elif choice_string_2 == '3':
                    self.set_selected_game_index(-1)
                    self.top_level_menu()

            # If there is currently no stored game description
            else:
                choice_string_2 = ''

                print("There is currently no description stored for this game.")
                print("\nWould you like to download the game description from Wikipedia?")
                print("Please enter 'Y' for Yes or 'N for No.")

                choice_string_2 = input()

                if choice_string_2.lower() == 'y':
                    print("Wikipedia Scraper microservice would be called here.")
                elif choice_string_2.lower() == 'n':
                    self.view_pc_game_details()

        # Choice 4: View downloaded game cover art file
        elif choice_string == '4':
            # If a cover art image has already been downloaded for the current game
            if self.get_pc_games_list()[self._selected_game_index].get_cover_art_file() != '':
                choice_string_2 = ''

                print("View Cover Art")
                print("1. Open cover art image in Windows Photo Viewer")
                print("2. Go back to Game Details Menu for " + self.get_pc_games_list()[
                    self._selected_game_index].get_title())

                choice_string_2 = input()

                if choice_string_2 == '1':
                    os.system("start " + self.get_pc_games_list()[self._selected_game_index].get_cover_art_file())
                    self.view_pc_game_details()
                elif choice_string_2 == '2':
                    self.view_pc_game_details()

            # If there is currently no stored cover art file
            else:
                choice_string_2 = ''

                print("There is currently no cover art for this game.")
                print("\nWould you like to download a cover art image from Google Images?")
                print("Please enter 'Y' for Yes or 'N for No.")

                choice_string_2 = input()

                if choice_string_2.lower() == 'y':
                    print("Image Scraper microservice would be called here.")
                elif choice_string_2.lower() == 'n':
                    self.view_pc_game_details()

        # Choice 5: Edit the currently selected game's details
        elif choice_string == '5':
            self.edit_pc_game(self.get_selected_game_index())

        # Choice 6: Delete the currently selected game from the PC Games List
        elif choice_string == '6':
            choice_string_2 = ''

            print("\nAre you sure you wish to permanently delete " + self.get_pc_games_list()[
                self._selected_game_index].get_title() + "?")
            print("Please enter 'Y' for Yes or 'N for No.")

            choice_string_2 = input()

            if choice_string_2.lower() == 'y':
                self.delete_pc_game(self.get_selected_game_index())
            elif choice_string_2.lower() == 'n':
                self.view_pc_game_details()

        # Choice 7: Go back to PC Games List
        elif choice_string == '7':
            self.set_selected_game_index(-1)
            self.view_pc_games()

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
    test_run.create_sample_data()
    test_run.game_organizer()
