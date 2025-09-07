# random-RPG

A project built with the Python Arcade library. The repo currently contains:

main.py: a minimal RGB animation demo using Arcade + Pillow + NumPy.
RPG.py: a tile-based RPG prototype that loads sprites/tiles from parsed assets.
parser.py and parser_font.py: utilities to slice raw tileset/font images into per-tile files used by the game.

## Requirements

Python 3.10–3.12 recommended
pip
ffmpeg (only required if you regenerate animated GIF assets with the parsers)
  - macOS: brew install ffmpeg
  - Ubuntu/Debian: sudo apt-get install ffmpeg

Install Python dependencies:
bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

The pinned dependencies in requirements.txt are:
arcade~=3.3.2
numpy~=2.3.2
Pillow~=11.3.0
moviepy~=2.2.1

## Assets setup

The RPG uses pre-parsed assets located in Tileset-parsed/ and Fonts-parsed/.
You have two options to provide them:

Option A: Use the pre-parsed assets included in this repo
  1. Unzip Tileset-parsed.zip into Tileset-parsed/ at the repo root.
  2. Unzip Fonts-parsed.zip into Fonts-parsed/ at the repo root.

Option B: Regenerate from the raw sources
  1. Unzip Tileset.zip into a directory named Tileset/ at the repo root.
  2. Unzip Fonts.zip into a directory named Fonts/ at the repo root.
  3. Run the parsers:
bash
     # From the repo root
     python parser.py          # processes Tileset/ -> Tileset-parsed/
     python "parser (font).py"  # processes Fonts/   -> Fonts-parsed/
    

After either option, you should have these directories:
Tileset-parsed/
Fonts-parsed/

## How to run

Optional: Run the demo (simple game):
bash
  python main.py
 

Run the RPG:
bash
  # Make sure Tileset-parsed/ and Fonts-parsed/ exist (see Assets setup)
  python RPG.py
 

## Controls (RPG.py)

H — advance through tutorial
Arrow keys — move
Space — toggle compass overlay
1 2 3 4 5 6 7 8 9 0 - = — select inventory slot
Enter — pick up/put down items from selected slot
Shift+Enter — pick up/put down half of the stack
Mouse click — place/pick up items (your slot must be compatible or empty to pick up)
E — interact with an NPC or continue conversation
X / C — scroll dialogue choices
Z — select a dialogue option

## Troubleshooting

Import errors (e.g., ModuleNotFoundError: arcade): run pip install -r requirements.txt inside your virtual environment.
Asset not found (e.g., missing Tileset-parsed/...): ensure you unzipped the pre-parsed archives or ran the parsers.
GIF writing issues when running parsers: install ffmpeg (see Requirements). MoviePy uses imageio-ffmpeg and may need the system binary.

## Project structure (relevant parts)
.
├── RPG.py                    # RPG prototype
├── main.py                   # small RGB animation demo
├── parser.py                 # tileset slicer -> Tileset-parsed/
├── parser (font).py          # font slicer    -> Fonts-parsed/
├── Tileset.zip               # raw tileset (zip)
├── Fonts.zip                 # raw font sheet (zip)
├── Tileset-parsed.zip        # pre-parsed tiles (zip)
├── Fonts-parsed.zip          # pre-parsed fonts (zip)
├── requirements.txt          # pinned Python deps
└── LICENSE

## Credits

Fonts: https://dusk-games.itch.io/dusk-free-fonts
Tiles: https://o-lobster.itch.io/adventure-pack

## License

This project’s code is licensed under the terms in LICENSE. Asset licenses are governed by their respective sources linked above.

## Examples
