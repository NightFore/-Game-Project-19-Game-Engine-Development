# create_project.py

import json
import os
from datetime import datetime


def main():
    # Define the GitHub username
    username = "NightFore"

    # Define the project path (current working directory)
    project_path = os.getcwd()

    # Get the current folder name
    project_name = os.path.basename(project_path)

    # Define the project structure
    project_structure = {
        "assets": {
            "images": {
                "sprites": {},
                "backgrounds": {},
                "ui": {},
            },
            "sounds": {
                "effects": {},
                "music": {},
                "voices": {},
            },
            "fonts": {},
        },
        "docs": {},
        "engine": {
            "__init__.py": "",
            "audio.py": "",
            "graphics.py": "",
            "input.py": "",
            "physics.py": "",
            "ui.py": ""
        },
        "game": {
            "__init__.py": "",
            "game.py": "",
            "levels": {
                "__init__.py": ""
            },
            "scenes": {
                "__init__.py": ""
            },
            "entities": {
                "__init__.py": ""
            },
            "utils": {
                "__init__.py": ""
            },
        },
        "logs": {},
        "tests": {
            "__init__.py": "",
            "test_audio.py": "",
            "test_graphics.py": "",
            "test_input.py": "",
            "test_physics.py": "",
            "test_ui.py": ""
        },
        "config.py": "",
        "logger.py": "",
        "main.py": "",
        "test.py": "",
        "requirements.txt": "",
    }

    print(f"Project creation for '{project_name}'...")
    create_structure(".", project_structure)
    create_readme(".", project_structure, project_name, username)
    create_license(".", username)
    create_config(".", project_name)
    create_gitignore(".")
    print(f"-> Project creation for '{project_name}' completed!\n")


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"\tCreated directory: {os.path.relpath(str(path))}")
            else:
                print(f"\tAlready Exists: {os.path.relpath(str(path))}")
            # Recursively create subdirectories and files
            create_structure(path, content)
        else:
            # Create file if it doesn't exist
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    f.write(content)
                print(f"\tCreated file: {os.path.relpath(str(path))}")
            else:
                print(f"\tAlready Exists: {os.path.relpath(str(path))}")


def generate_structure_tree(structure, indent):
    tree_str = ""
    for idx, (name, content) in enumerate(structure.items()):
        if idx == len(structure) - 1:  # Last item in the current level
            tree_str += f"{indent}└── {name}/\n"
            new_indent = indent + "    "  # Adjust indentation for sub-level
        else:
            tree_str += f"{indent}├── {name}/\n"
            new_indent = indent + "│   "  # Adjust indentation for sub-level

        if isinstance(content, dict):
            tree_str += generate_structure_tree(content, new_indent)
    return tree_str


def create_readme(base_path, structure, project_name, username):
    # Project description
    project_description = ("This is a hobbyist game engine project aimed at recreating and constructing my projects "
                           "more effectively.")

    # Project timeline
    timeline = [
        {"event": "Started", "date": "August 5, 2023"},
        {"event": "Rebooted", "date": "July 13, 2024"}
    ]
    project_timeline = "\n".join([f"- **{event['event']}**: {event['date']}" for event in timeline])

    # Project structure
    structure_tree = generate_structure_tree(structure, '')
    project_structure = (
        f"\nThe project structure is organized as follows:"
        f"\n"
        f"\n```"
        f"\n{structure_tree}"
        f"\n```"
    )

    # Constructing the README content
    readme_content = (
        f"# {project_name}\n"
        f"\n"
        f"\n## Project Description"
        f"\n"
        f"\n{project_description}"
        f"\n"
        f"\n## Project Timeline"
        f"\n"
        f"\n{project_timeline}"
        f"\n"
        f"\n## Project Structure"
        f"\n"
        f"\n{project_structure}"
        f"\n"
        f"\n## Getting Started"
        f"\n"
        f"\nTo start using {project_name}, simply clone the repository."
        f"\n"
        f"\n## Installation"
        f"\n"
        f"\nClone the repository:"
        f"\n"
        f"\n```bash"
        f"\ngit clone https://github.com/{username}/{project_name}.git"
        f"\n```"
        f"\n"
        f"\nInstall dependencies:"
        f"\n"
        f"\n```bash"
        f"\npip install -r requirements.txt"
        f"\n```"
        f"\n"
        f"\n## License"
        f"\n"
        f"\nThis project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details."
    )

    readme_path = os.path.join(base_path, 'README.md')
    if not os.path.exists(readme_path) or os.path.getsize(readme_path) == 0:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"\tCreated file: README.md")
    else:
        print(f"\tAlready Exists: README.md is not empty, skipping creation.")


def create_license(base_path, username):
    current_year = datetime.now().year
    license_content = (
        f"MIT License"
        f"\n"
        f"\nCopyright (c) {current_year} {username}"
        f"\n"
        f"\nPermission is hereby granted, free of charge, to any person obtaining a copy"
        f"\nof this software and associated documentation files (the \"Software\"), to deal"
        f"\nin the Software without restriction, including without limitation the rights"
        f"\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell"
        f"\ncopies of the Software, and to permit persons to whom the Software is"
        f"\nfurnished to do so, subject to the following conditions:"
        f"\n"
        f"\nThe above copyright notice and this permission notice shall be included in all"
        f"\ncopies or substantial portions of the Software."
        f"\n"
        f"\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR"
        f"\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,"
        f"\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE"
        f"\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"
        f"\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,"
        f"\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE"
        f"\nSOFTWARE."
    )

    license_path = os.path.join(base_path, 'LICENSE')
    if not os.path.exists(license_path) or os.path.getsize(license_path) == 0:
        with open(license_path, 'w') as f:
            f.write(license_content)
        print(f"\tCreated file: LICENSE")
    else:
        print(f"\tAlready Exists: LICENSE is not empty, skipping creation.")


def create_config(base_path, project_name):
    config_data = {
        "window": {
            "width": 800,
            "height": 600,
            "title": project_name,
            "fullscreen": False,
            "vsync": True,
            "resizable": True
        },
        "audio": {
            "master_volume": 1.0,
            "bgm_volume": 0.5,
            "sfx_volume": 0.5,
            "voice_volume": 0.5,
            "mute": False
        },
        "graphics": {
            "background_color": "#000000",
            "fps_limit": 60,
            "anti_aliasing": True
        },
        "input": {
            "keyboard": {
                "move_up": "W",
                "move_down": "S",
                "move_left": "A",
                "move_right": "D",
                "action": "SPACE",
                "cancel": "ESCAPE"
            },
            "mouse": {
                "sensitivity": 1.0,
                "invert_y_axis": False
            },
            "controller": {
                "enabled": False,
                "sensitivity": 1.0
            }
        },
        "gameplay": {
            "difficulty": "normal",
            "language": "english",
            "tutorial": True
        },
        "physics": {
            "gravity": 9.81,
            "air_friction": 0.01,
            "ground_friction": 0.5
        },
        "ui": {
            "font_size": 16,
            "default_font": "Arial",
            "show_fps": True,
        },
        "save_system": {
            "autosave": True,
            "save_interval": 300
        },
    }

    config_path = os.path.join(base_path, 'config.json')
    if not os.path.exists(config_path) or os.path.getsize(config_path) == 0:
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"\tCreated file: config.json")
    else:
        print(f"\tAlready Exists: config.json is not empty, skipping creation.")


def create_gitignore(base_path):
    # List of files/directories to ignore
    ignore_list = [
        "__pycache__/",
        ".idea",
        ".DS_Store",
        "*.log"
    ]

    gitignore_content = "\n".join(ignore_list)

    gitignore_path = os.path.join(base_path, '.gitignore')
    if not os.path.exists(gitignore_path) or os.path.getsize(gitignore_path) == 0:
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        print(f"\tCreated file: .gitignore")
    else:
        print(f"\tAlready Exists: .gitignore is not empty, skipping creation.")


# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
