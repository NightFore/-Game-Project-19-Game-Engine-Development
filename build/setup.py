import sys
from cx_Freeze import setup, Executable

# Path to your game's main script
main_script = "main.py"

build_exe_options = {
    "includes": ["pygame"],  # Add other required modules here
    "excludes": [],
    "include_files": [
        "data",
        "readme.txt",
        # Add other files or folders as needed
    ],
}

base = None
if sys.platform == "win32":
    # If on Windows, use "Win32GUI" if you don't want a console window (useful for games)
    base = "Win32GUI"

setup(
    name="Game Engine Development",
    version="0.0",
    description="An executable for your game created using the custom game engine.",
    options={"build_exe": build_exe_options},
    executables=[Executable(main_script, base=base)]
)
