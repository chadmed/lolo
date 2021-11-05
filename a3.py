#!/usr/bin/env python3
"""
Lolo: A game similar to 2048 but not really for legal reasons.

__author__ = 'James Calligeros'
__student_number__ = '44806587'
__email__ = 'jcalligeros99@gmail.com'
__copyright__ = 'Copyright 2017, James Calligeros'
__license__ = 'MIT'
__version__ = '1.1'

Note: Requires Python 3.6 or later.

Support code and modules used under the MIT license.

TODO (in order of urgency):
    - Dialog for invalid tile activation

    - Make lightning disable itself

    - Fix lightning accumulation:
      I orignially had it working. I then changed gamemodes and it broke.

    - Make the automatic game reset properly

    - Fix the window hiding bug. Currently, we can make the Main Menu
      go away while we are playing the game, however when we leave the game,
      the original instance comes back as a 'ghost'. Clearly a problem with
      parent/child relationships or something.

    - Task 3

    - Make pylint stop hating me :(
"""


import tkinter as tk

# Import Merlin's Magic Methods
from colours import *
from base import BaseLoloApp
import random

# Import the gamemodes
from game_regular import RegularGame
from game_make13 import Make13Game
from game_lucky7 import Lucky7Game
from game_unlimited import UnlimitedGame

# Import platform module
import platform

# Import the high score manager and fire it up
import highscores as hs
hiscores = hs.HighScoreManager()

# Determine OS (necessary for OS-specific key bindings)
SYSTEM = platform.system()


class LoloLogo():
    """
    Draws the Lolo Logo in a blank canvas.
    """
    def __init__(self, master):
        """
        Creates a blank canvas and draws the logo out of rectangles and cir--
        err ovals.

        args:
            master (tk.Tk | tk.Toplevel | tk.Frame): The structure to inject
                                                     the logo into.
        """
        # Create a canvas for the logo
        self.logocanvas = tk.Canvas(master, width=450, height=150)
        self.logocanvas.grid(row=0, column=0)

        # Make the logo
        self.logocanvas.create_rectangle(10, 10, 40, 130,
                                         fill=VIBRANT_COLOURS['purple'],
                                         outline=VIBRANT_COLOURS['purple'])
        self.logocanvas.create_rectangle(10, 110, 110, 140,
                                         fill=VIBRANT_COLOURS['purple'],
                                         outline=VIBRANT_COLOURS['purple'])

        self.logocanvas.create_oval(120, 50, 210, 140,
                                    fill=VIBRANT_COLOURS['purple'],
                                    outline=VIBRANT_COLOURS['purple'])
        self.logocanvas.create_oval(145, 75, 185, 115,
                                    fill='white', outline='white')

        self.logocanvas.create_rectangle(225, 10, 255, 130,
                                         fill=VIBRANT_COLOURS['purple'],
                                         outline=VIBRANT_COLOURS['purple'])
        self.logocanvas.create_rectangle(225, 110, 325, 140,
                                         fill=VIBRANT_COLOURS['purple'],
                                         outline=VIBRANT_COLOURS['purple'])

        self.logocanvas.create_oval(340, 50, 430, 140,
                                    fill=VIBRANT_COLOURS['purple'],
                                    outline=VIBRANT_COLOURS['purple'])
        self.logocanvas.create_oval(365, 75, 405, 115,
                                    fill='white', outline='white')


class StatusBar():
    """
    Creates the Lolo Status Bar.
    """
    def __init__(self, master, mode):
        """
        Does the actual work of creating the status bar.

        Creates a label for the gamemode and the score and packs them into a
        single grid reference.

        args:
            master (tk.Tk | tk.Toplevel | tk.Frame): The structure to inject
                                                the bar into.

            mode (str): The name of the gamemode selected by the user.
        """
        # Game mode and score labels
        self.modelabel = tk.Label(master, text='Game Mode: ' + str(mode))
        self.modelabel.grid(row=1, column=0, sticky=tk.W)

        self.score = tk.Label(master, text='Score: 0')
        self.score.grid(row=1, column=0, sticky=tk.E)

    def set_score(self, score):
        """
        Updates the score in the status bar.

        args:
            score (int): The player's current score.

        returns:
            scoretext (str): The text to replace 'Score: 0' with in the
                             Status Bar.
        """
        # Create a var containing the string with the score in it
        self.scoretext = ('Score: ' + str(score))

        # Update the text in the label
        self.score['text'] = self.scoretext


class AutoPlay(BaseLoloApp):
    """
    Automatically plays a game of Lolo.
    """
    def __init__(self, master, autoplay, grid=None):
        """
        Makes the game appear in the window.

        args:
            master (tk.Tk | tk.Toplevel |tk.Frame): The object to inject the
                                                    autogame into.
        """
        if grid is not None:
            self._grid = grid

        self._master = master
        self._move_delay = 350

        if autoplay == 1:
            super().__init__(master)
            self.move()

        else:
            super().__init__(master, self._grid)

    def bind_events(self):
        """Binds relevant events."""
        self._game.on('resolve', self.resolve)

    def resolve(self, delay=None):
        """Makes a move after a given movement delay."""
        if delay is None:
            delay = self._move_delay

        self._master.after(delay, self.move)

    def move(self):
        """Finds a connected tile randomly and activates it."""
        connections = list(self._game.find_groups())

        if connections:
            # pick random valid move
            cells = list()

            for connection in connections:
                for cell in connection:
                    cells.append(cell)

            self.activate(random.choice(cells))

    def game_over(self):
        """
        Called when the game emits the game over event.
        """
        self.reset()

    def reset(self, event=None):
        """
        Resets the current game.
        """
        self._game.reset()
        self._grid_view.draw(self._game.grid)
        self._game.set_score(0)

    def score(self, points):
        """
        Override score with pass to clean up stdout.

        stdout gets really cluttered with all those score() calls from
        BaseLoloApp. Since we don't really care about the score of the
        autogame, we can override score() to save (very little) memory
        and prevent headaches.
        """
        pass


class HighScores(AutoPlay):
    def __init__(self, master):
        self.window = master
        self.window.title('Highscores')

        # Get the list of sorted scores
        self.hiscores = hiscores.get_sorted_data()

        # Dicts with best players' scores
        self.bestplayer = self.hiscores[0]
        self.p2 = self.hiscores[1]
        self.p3 = self.hiscores[2]
        self.p4 = self.hiscores[3]
        self.p5 = self.hiscores[4]
        self.p6 = self.hiscores[5]
        self.p7 = self.hiscores[6]
        self.p8 = self.hiscores[7]
        self.p9 = self.hiscores[8]
        self.p10 = self.hiscores[9]

        # Display the best player's details
        self.label_bestplayer = tk.Label(self.window, text='Best Player: ' +
                                         self.bestplayer['name'] + ' with ' +
                                         str(self.bestplayer['score']) +
                                         ' points!')
        self.label_bestplayer.grid(row=0, column=0)

        # Create a frame for the static grid
        self.frame_grid = tk.Frame(self.window)
        self.frame_grid.grid(row=1, column=0)

        # Do something
        self.playergrid = self.bestplayer['grid']
        self.game = RegularGame.deserialize(self.playergrid)
        super(AutoPlay, self).__init__(self.frame_grid, self.game)

        self.label_other = tk.Label(self.window, text='Other top scorers:')
        self.label_other.grid(row=2, column=0, sticky=tk.N)

        # Display the other 'best' player's names
        self.label_p2name = tk.Label(self.window, text=self.p2['name'])
        self.label_p3name = tk.Label(self.window, text=self.p3['name'])
        self.label_p4name = tk.Label(self.window, text=self.p4['name'])
        self.label_p5name = tk.Label(self.window, text=self.p5['name'])
        self.label_p6name = tk.Label(self.window, text=self.p6['name'])
        self.label_p7name = tk.Label(self.window, text=self.p7['name'])
        self.label_p8name = tk.Label(self.window, text=self.p8['name'])
        self.label_p9name = tk.Label(self.window, text=self.p9['name'])
        self.label_p10name = tk.Label(self.window, text=self.p10['name'])

        self.label_p2name.grid(row=3, column=0, sticky=tk.W)
        self.label_p3name.grid(row=4, column=0, sticky=tk.W)
        self.label_p4name.grid(row=5, column=0, sticky=tk.W)
        self.label_p5name.grid(row=6, column=0, sticky=tk.W)
        self.label_p6name.grid(row=7, column=0, sticky=tk.W)
        self.label_p7name.grid(row=8, column=0, sticky=tk.W)
        self.label_p8name.grid(row=9, column=0, sticky=tk.W)
        self.label_p9name.grid(row=10, column=0, sticky=tk.W)
        self.label_p10name.grid(row=11, column=0, sticky=tk.W)

        # Display their scores
        self.label_p2score = tk.Label(self.window, text=self.p2['score'])
        self.label_p3score = tk.Label(self.window, text=self.p3['score'])
        self.label_p4score = tk.Label(self.window, text=self.p4['score'])
        self.label_p5score = tk.Label(self.window, text=self.p5['score'])
        self.label_p6score = tk.Label(self.window, text=self.p6['score'])
        self.label_p7score = tk.Label(self.window, text=self.p7['score'])
        self.label_p8score = tk.Label(self.window, text=self.p8['score'])
        self.label_p9score = tk.Label(self.window, text=self.p9['score'])
        self.label_p10score = tk.Label(self.window, text=self.p10['score'])

        self.label_p2score.grid(row=3, column=0, sticky=tk.E)
        self.label_p3score.grid(row=4, column=0, sticky=tk.E)
        self.label_p4score.grid(row=5, column=0, sticky=tk.E)
        self.label_p5score.grid(row=6, column=0, sticky=tk.E)
        self.label_p6score.grid(row=7, column=0, sticky=tk.E)
        self.label_p7score.grid(row=8, column=0, sticky=tk.E)
        self.label_p8score.grid(row=9, column=0, sticky=tk.E)
        self.label_p9score.grid(row=10, column=0, sticky=tk.E)
        self.label_p10score.grid(row=11, column=0, sticky=tk.E)


class LoloApp(BaseLoloApp):
    """
    The game window itself. This is about 100x more complex than Dwarf Fortress
    so you probably shouldn't touch it. Changing things usually leaves it in
    a similar state to Big Rigs: Over the Road Racing.
    """
    def __init__(self, master, game_mode, name):
        """
        Does the brunt of the work.

        Places all the game elements into a window, configures said window,
        then starts the game.

        args:
            master (tk.Tk | tk.Toplevel): Where is the game going?

            game_mode (object): The game mode to load up and initialise.
                                When set to None, the game defaults to
                                RegularGame().

            name (str): The player's name for high score recording purposes.
        """
        self.window = master

        # Set the player's name for score recording
        self.playername = name

        # Create a menu system
        self.main_menu = tk.Menu(master)
        master.config(menu=self.main_menu)

        # Create a File menu
        self.file_menu = tk.Menu(self.main_menu)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)

        # Key bindings for the menu items
        # For superior *nix-like operating systems
        if SYSTEM == 'Darwin':
            self.file_menu.add_command(label='New Game', command=self.reset,
                                       accelerator='Command-n')
            self.file_menu.bind_all('<Command-n>', self.reset)
            self.file_menu.bind_all('<Control-n>', self.reset)

            self.file_menu.add_command(label='Quit', command=self.killgame,
                                       accelerator='Command-w')
            self.file_menu.bind_all('<Command-w>', self.killgame)
            self.file_menu.bind_all('<Control-w>', self.killgame)

            self.file_menu.add_separator()

            self.file_menu.add_command(label='LIGHTNING',
                                       command=self.lightning,
                                       accelerator='Command-l')
            self.file_menu.bind_all('<Command-l>', self.lightning)
            self.file_menu.bind_all('<Control-l>', self.lightning)

        # For some other operating systems
        else:
            self.file_menu.add_command(label='New Game', command=self.reset,
                                       accelerator='Ctrl-n')
            self.file_menu.bind_all('<Control-n>', self.reset)

            self.file_menu.add_command(label='Quit', command=self.killgame,
                                       accelerator='Ctrl-q')
            self.file_menu.bind_all('<Control-q>', self.killgame)

            self.file_menu.add_separator()

            self.file_menu.add_command(label='LIGHTNING',
                                       command=self.lightning,
                                       accelerator='Ctrl-l')
            self.file_menu.bind_all('<Control-l>', self.lightning)

        # Create a frame for the actual Lolo game grid to go in
        self.actual_game = tk.Frame(master)

        # Inherit the init method from BaseLoloApp
        super().__init__(self.actual_game, game_mode)

        # Create a game window title
        master.title('Lolo: ' + self._game.get_name())

        # GUI scaling
        master.resizable(0, 0)

        # Logo
        self.logo = LoloLogo(master)

        # Status bar
        self.status = StatusBar(master, self._game.get_name())

        # Pack the game
        self.actual_game.grid(row=2, column=0)

        # Greased lightning
        self.num_lightnings = 1
        self.lightning_button = tk.Button(master,
                                          text='Lightning ({})'.format(self.num_lightnings),
                                          command=self.lightning,
                                          state=tk.NORMAL)
        self.lightning_button.grid(row=3, column=0, columnspan=2, sticky=tk.N)
        self.lightning_status = False

    def score(self, points):
        """
        Sets the player's score in the status bar.
        """
        self.status.set_score(self._game.get_score())

        # Determine whether or not to give the player a lightning
        self.lightningchance = random.randint(1, 10)

        if self.lightningchance == '1' or '10':
            self.num_lightnings += 1
            self.lightning_button['text'] = 'Lightning ({})'.format(self.num_lightnings)

    def reset(self, event=None):
        """
        Resets the current game.
        """
        self._game.reset()
        self._grid_view.draw(self._game.grid)
        self.status.score['text'] = 'Score: 0'
        self._game.set_score(0)
        self.num_lightnings = 1

        # If the game over window still exists
        if self.gameover is not None:
            self.gameover.destroy()

    def activate(self, position):
        """
        Activates the selected tile.
        """
        if self.lightning_status is True:
            self.remove(position)

        else:
            super().activate(position)

    def game_over(self):
        """
        Is called when extremely advanced algorithms detect a crap player.

        Records the user's final score in the high scores DB, informs the user of their
        failure and then gives them the option to call the Quit menu or start a new game
        of the same mode.
        """
        # Record the user's score
        self.score_record(self._game.get_score(), self._game.grid, self.playername)

        # Create a popup
        self.gameover = tk.Toplevel()
        self.gameover.title('Game Over :(')

        # Deliver the bad news
        self.youlose = tk.Label(self.gameover, text='You lose. You scored ' +
                                str(self._game.get_score()) +
                                'points.')
        self.youlose.grid(row=0, column=0, columnspan=2, sticky=tk.N, padx=5, pady=5)

        # Seppuku or further embarassment?
        self.embarass = tk.Button(self.gameover, text='Try Again?', command=self.reset)
        self.embarass.grid(row=1, column=0, padx=5, pady=5)

        self.seppuku = tk.Button(self.gameover, text='Quit', command=self.killgame)
        self.seppuku.grid(row=1, column=1, padx=5, pady=5)

    def score_record(self, final_score, final_grid, name):
        """
        Records the score set by the player.

        Only invoked when game over conditions are met. If the player
        manually quits the game before the game is finished, their score
        is not recorded as punishment for their weakness.

        args:
            final_score (int): The player's final score.

            final_grid (???): Magic. A description of the grid at the end of the game.

            name (str): The player's name.
        """
        hiscores.record(final_score, final_grid, name)

    def lightning(self):
        """
        Allows the player to harness the power of Zeus.
        """
        if self.num_lightnings > 0:
            self.lightning_status = True

    def remove(self, position):
        """
        Removes a tile at the clicked position.

        Function only called if the player enables Lightning, which is
        disabled as soon as the player removes one tile.

        args:
            position (tuple <int, int>): The position of the tile to destroy
        """

        if self.lightning_status is True:
            super().remove(position)
            self.num_lightnings -= 1
            self.lightning_status = False
            self.lightning_button['text'] = 'Lightning ({})'.format(self.num_lightnings)

    def killgame(self):
        """
        Kills the game.

        Bog standard 'Are you sure?' dialog. The player can pick from quitting
        to the main menu, quitting to the desktop or continuing the current game.
        """
        # Create the window
        self.quit_win = tk.Toplevel()
        self.quit_win.title('Quit Game')

        # Ask the user
        self.message = tk.Label(self.quit_win, text='Are you sure you want to quit?\n'
                                'Your unsaved progress will be lost.')
        self.message.grid(row=0, column=0, columnspan=3, sticky=tk.N, padx=5, pady=5)

        # Give them options
        self.quit_to_menu = tk.Button(self.quit_win, text='Quit to Main Menu (BROKEN)',
                                      command=self.back_to_menu)
        self.quit_to_menu.grid(row=1, column=0, padx=5, pady=5)
        self.quit_to_os = tk.Button(self.quit_win, text='Quit to Desktop', command=exit)
        self.quit_to_os.grid(row=1, column=1, padx=5, pady=5)
        self.cancel = tk.Button(self.quit_win, text='Cancel', command=self.quit_win.destroy)
        self.cancel.grid(row=1, column=2, padx=5, pady=5)

    def back_to_menu(self):
        """
        Sends the user back to the main menu.

        |------------|
        |OUT OF ORDER| (see TODO at top)
        |------------|
              |
              |
              |
        """
        # Destroy the game window
        self.window.destroy()

        # Destroy the quit dialog
        self.quit_win.destroy()

        # THEORETICALLY, bring the Main Menu back to life.
        main().root.deiconify()


class LoloApp2():
    """
    The Lolo Main Menu.

    Gives the user access to the high scores, the ability to change game modes,
    and a pretty automatically playing game.
    """
    def __init__(self, master, game):
        """
        Draws the main menu.

        Creates the window and places everything in it.
        """
        # Set default gamemode to None for testing
        self.initmode = game
        self.window = master

        self.logoframe = tk.Frame(master)
        self.logoframe.grid(row=0, column=0, columnspan=2)
        self.logo = LoloLogo(self.logoframe)

        self.buttons = tk.Frame(master)
        self.buttons.grid(row=1, column=0)

        # Create buttons
        self.label_name = tk.Label(self.buttons, text='Enter your name: ')
        self.entry_name = tk.Entry(self.buttons)
        self.button_playgame = tk.Button(self.buttons, text='Play Game',
                                         command=self.rungame)
        self.button_hiscores = tk.Button(self.buttons, text='High Scores',
                                         command=self.hiscores)
        self.button_gamemode = tk.Button(self.buttons, text='Change Game Mode',
                                         command=self.gamemodes)
        self.button_quit = tk.Button(self.buttons, text='Quit Lolo',
                                     command=exit)

        # Grid buttons
        self.label_name.grid(row=0, column=0, padx=2, pady=2, sticky=tk.E)
        self.entry_name.grid(row=0, column=1, padx=2, pady=2)
        self.button_playgame.grid(row=1, column=0, padx=2, pady=2)
        self.button_hiscores.grid(row=1, column=1, padx=2, pady=2)
        self.button_gamemode.grid(row=2, column=0, padx=2, pady=2)
        self.button_quit.grid(row=2, column=1, padx=2, pady=2)

        # Add the autoplaying game
        self.frame_autoplay = tk.Frame(master)
        self.frame_autoplay.grid(row=1, column=1)
        self.game_autoplay = AutoPlay(self.frame_autoplay, 1, grid=None)

    def rungame(self):
        """
        Runs the game as configured by the player.

        Sets the player's name, creates a window for LoloApp then makes
        the Main Menu disappear.
        """
        self.playername = self.entry_name.get()

        # Make sure the player actually entered a name
        if self.playername == '':
            self.errname = tk.Toplevel(self.window)
            self.errname.title('Enter Name')
            self.errlabel = tk.Label(self.errname, text='You didn\'t enter name. ' +
                                     'Please enter a name.')
            self.errlabel.grid(row=0, column=0, columnspan=2, sticky=tk.N)
            self.errokay = tk.Button(self.errname, text='OK', command=self.errname.destroy)
            self.errokay.grid(row=1, column=0, columnspan=2)

        # If they entered a name
        else:
            self.gamewindow = tk.Toplevel()
            self.game = LoloApp(self.gamewindow, self.initmode, self.playername)
            self.window.withdraw()

    def hiscores(self):
        self.hiscore_window = tk.Toplevel()
        self.hiscores = HighScores(self.hiscore_window)

    def gamemodes(self):
        pass


def main():
    game = RegularGame()
    root = tk.Tk()
    root.resizable(0, 0)
    root.title('Lolo Main Menu')
    app = LoloApp2(root, game)
    root.mainloop()

if __name__ == '__main__':
    main()
