# CatBurglar
 
A quick entry for [PyWeek](https://pyweek.org). [The theme given for pyweek 31 was "Cops".](https://pyweek.org/31/)
 
> You are a gorilla. Your cat was framed for illegal stonks trading, so you snuck into jail to bust her out. Now you need to make your escape!

This is a variation on a runner game genre, except there is a time limit of 2 minutes before the player wins.
Press space to jump over enemies. The longer you hold space, the higher you jump.

## Installation

[Python](https://python.org) >= 3.7 is required.
See [this guide](https://www.freecodecamp.org/news/the-python-guide-for-beginners/#installingpython3) for information
 on how to install it.
  
[Arcade](https://arcade.academy/) >= 2.5.6 and dependencies are also required. They will be installed by following the instructions below.

### Installation for Players

#### 1. Download the zip or clone the repo
#### 2. Enter the directory in your terminal or command prompt
#### 3. Create a virtual environment:
```
python -m venv CatBurglarVenv
```
#### 4. Activate the environment.

Choose the appropriate command from the table below based on your OS and shell.

| Operating System & Shell    |  Command                              |
------------------------------|---------------------------------------|
| Windows with cmd.exe        | `CatBurglarVenv\Scripts\activate.bat` |
| Windows with PowerShell     | `CatBurglarVenv\Scripts\Activate.ps1` |
| Linux , macOS , other *NIX  | `source CatBurglarVenv/bin/activate`  |

#### 5. Install the project and its requirements
Run the following command. It might take a bit to set up arcade.
```
pip install -e .
```

#### 6. Run the game
```
catburglar
```
You will need to have the virtual environment activated to run the game. If you open a new terminal
(such as after restarting your computer), you will need to activate the shell again.

### For developers

#### 1. Set up a virtual environment

Follow steps 1-5 above to create a virtual environment, or use your preferred manner.

#### 2. Set up your development environment for debugging
If you use a debugger in an IDE, you may need to alter the path that is set as the working directory when debugging from
`main.py`. On pycharm, this may be found under  `Run > Edit Configurations`.
You will need to set the run configuration for main.py to the root of the directory so that it can find assets
when run from the IDE ui.

## Asset citations

### Gorilla Sprites
Original Gorilla sprites by Salami. These don't show up in the game, but are bundled in the assets directory.
Cat added by Pushfoo (`cat*.png` in assets/gorilla)

### Cop and Drone
Cop and drone sprites by Pushfoo
