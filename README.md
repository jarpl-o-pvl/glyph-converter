# 🚀 Glyph Converter

**Convert Audacity labels into custom glyph ringtones for Nothing Phone (1, 2, 2a, 3a, 4a)**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jarp1-o-pvl/glyph-converter?style=social)](https://github.com/jarp1-o-pvl/glyph-converter/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/jarp1-o-pvl/glyph-converter?style=social)](https://github.com/jarp1-o-pvl/glyph-converter/network/members)
[![GitHub issues](https://img.shields.io/github/issues/jarp1-o-pvl/glyph-converter)](https://github.com/jarp1-o-pvl/glyph-converter/issues)
[![GitHub release](https://img.shields.io/github/v/release/jarp1-o-pvl/glyph-converter)](https://github.com/jarp1-o-pvl/glyph-converter/releases)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> One command. One `.ogg` file. A custom light show on your Nothing Phone.

---

## 📱 Demo

![Glyph Converter Demo](https://via.placeholder.com/800x400/0a0a0a/00ff88?text=Glyph+Converter+in+Action)

*Watch the glyphs light up in sync with your music!*

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **All Nothing Phones** | Supports PHONE1, PHONE2, PHONE2A, PHONE3A, PHONE4A |
| **Glyph Fragmentation** | Control every single LED individually (2a, 3a, 4a) |
| **Audacity Integration** | Export `.txt` labels directly from Audacity |
| **One-Command Workflow** | Just type `glyph song.ogg` |
| **Presets** | Wave, Pulse, Flash, Rainbow — ready to use |
| **BPM Sync** | Synchronize lights with music tempo |
| **Console Visualization** | See your pattern in the terminal |
| **100% Compatible** | Works -- official Glyph Composer |

---

## 🎯 Quick Start

### Step 1: Install Dependencies

Run as Administrator:

```cmd
install_dependencies.bat
This installs:

 - Python 3.11
 - Audacity
 - ffmpeg

install.bat
```
Step 3: Create Labels in Audacity
Open your audio in Audacity

Go to Tracks → Add New → Label Track

Place labels at the moments you want the glyphs to light up

Name each label: LED-INTENSITY

Label Example	What it does
0-100	LED 0 at 100% brightness
5-50	LED 5 at 50% brightness
12-100	LED 12 at 100% brightness
END	Required — marks the end of the track
Export:

File → Export → Export Audio → save as .ogg

File → Export → Export Labels... → save as .txt

Important: .ogg and .txt files must have the same name!

Step 4: Run the Converter
cmd
glyph my_song.ogg
Step 5: Follow the Prompts
text
📱 Select model:
   1. Nothing Phone (1) — 12 zones
   2. Nothing Phone (2) — 33 zones
   3. Nothing Phone (2a) — 5 zones, 24 LEDs
   4. Nothing Phone (3a) — 3 zones, 26 LEDs
   5. Nothing Phone (4a) — 3 zones, 26 LEDs

>>> 4
Step 6: Install on Your Phone
Copy .ogg to:

text
/Internal Storage/ringtones/composition/
Open Glyph Composer → Library → Import

Select your file and set as ringtone!

📁 Project Structure
text
glyph-converter/
├── converter.py                 # Main converter script
├── glyph.bat                    # Launcher: glyph song.ogg
├── install_dependencies.bat      # Installs Python, Audacity, ffmpeg
├── install_libraries.bat         # Installs mutagen, pydub
├── my_song.ogg                  # Your audio (from Audacity)
├── my_song.txt                  # Your labels (from Audacity)
├── my_song_glyph.ogg            # Output — ready to install!
├── README.md                    # This file
├── LICENSE                      # MIT License
└── .gitignore                   # Ignored files

📱 Supported Models
Model	Zones	LEDs	Fragmentation
Phone (1)	12	12	❌ No
Phone (2)	33	33	❌ No
Phone (2a)	5	24	✅ Yes
Phone (3a)	3	26	✅ Yes
Phone (4a)	3	26	✅ Yes
🎹 Usage Reference
Basic Commands
cmd
# Simple conversion
glyph my_song.ogg

# With model and preset
glyph my_song.ogg --model PHONE3A --preset wave

# With BPM
glyph my_song.ogg --bpm 128

# All options
glyph my_song.ogg --model PHONE3A --preset pulse --bpm 120 --steps 32
Parameters
Parameter	Description	Options
--model	Phone model	PHONE1, PHONE2, PHONE2A, PHONE3A, PHONE4A
--preset	Pattern preset	wave, pulse, flash, rainbow, custom
--bpm	Beats per minute	60-200
--steps	Number of steps	8-64
🧠 How Glyph Fragmentation Works
On Nothing Phone (2a), (3a), and (4a), the glyphs are physically grouped into zones, but the software allows you to control each individual LED.

Phone	Physical Zones	Individual LEDs	Fragmentation
Phone (3a)	3	26	✅ Each LED individually controllable
Example labels for Phone (3a):

text
# Top Zone (LEDs 0–8)
0-100
1-80
2-60
3-100
4-50
5-100
6-70
7-90
8-100

# Middle Zone (LEDs 9–16)
9-50
10-80
11-100
12-60
13-100
14-40
15-80
16-100

# Bottom Zone (LEDs 17–25)
17-100
18-50
19-80
20-100
21-60
22-90
23-100
24-70
25-100

END
🔧 Troubleshooting
Issue	Solution
"File not found"	Make sure .ogg and .txt have the same name
"ffmpeg not found"	Run install_dependencies.bat as Administrator
"Python not found"	Run install_dependencies.bat as Administrator
GlyphVisualizer error	Use the latest version from SebiAi's GitHub
Lights don't match rhythm	Place labels precisely on beats in Audacity
📦 Dependencies
Library	Purpose
mutagen	Audio metadata handling
pydub	Audio processing
colorama	Colored console output
Install manually:

bash
pip install mutagen pydub colorama


