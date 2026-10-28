# Desktop Pet

A small desktop pet for Windows 10/11, written in Python with Tkinter.

## Features

- Always-on-top transparent pet window
- Drag the pet with the left mouse button
- Double-click the pet to pet it
- Right-click for the interaction menu
- Feed, play with, and put the pet to sleep
- Hunger, energy, happiness, and mood indicators
- Press `Esc` to close the pet
- Press `F1` to show the controls

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer (to run from source)
- Tkinter, which is included with most standard Windows Python installations

No third-party Python packages are required.

## Run from source

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python desktop_pet.py
   ```

## Build an executable with PyInstaller

Install PyInstaller:

```bash
python -m pip install pyinstaller
```

Build the EXE:

```bash
pyinstaller --onefile --windowed --name DesktopPet desktop_pet.py
```

The executable will be created in the `dist` folder.

## Controls

| Action | Control |
| --- | --- |
| Move the pet | Hold left mouse button and drag |
| Pet it | Double-click with left mouse button |
| Open menu | Right-click |
| Show help | `F1` |
| Close | `Esc` |

## Notes

This project is provided as-is. If you encounter a bug, please open an issue in the repository.
