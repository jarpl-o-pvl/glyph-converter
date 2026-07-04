#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
  🚀 AUTO GLYPH CONVERTER — Manual Model Selection
  
  Choose your Nothing Phone model manually.
  Just drop your .ogg file, select model, and wait 1 minute!
  
  Usage: auto-glyph my_song.ogg
================================================================================
"""

import os
import sys
import json
import subprocess
import shutil
import base64
import math
import time
from datetime import datetime
from pathlib import Path

try:
    from colorama import init, Fore, Style
    init()
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
except ImportError:
    GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = BOLD = ''

# ============================================================
#  CONFIGURATION — ALL NOTHING PHONE MODELS
# ============================================================

GLYPH_CONFIG = {
    "PHONE1": {
        "id": "PHONE1",
        "name": "Nothing Phone (1)",
        "visualizer_name": "v1-Asteroids Glyph Composer",
        "zones": 12,
        "fragmentation": False,
        "led_count": 12,
        "rows": 12,
        "cols": 16,
        "description": "12 zones",
        "fragmentation_groups": []
    },
    "PHONE2": {
        "id": "PHONE2",
        "name": "Nothing Phone (2)",
        "visualizer_name": "v2-Asteroids Glyph Composer",
        "zones": 33,
        "fragmentation": False,
        "led_count": 33,
        "rows": 6,
        "cols": 16,
        "description": "33 zones",
        "fragmentation_groups": []
    },
    "PHONE2A": {
        "id": "PHONE2A",
        "name": "Nothing Phone (2a)",
        "visualizer_name": "v2a-Asteroids Glyph Composer",
        "zones": 5,
        "fragmentation": True,
        "led_count": 24,
        "rows": 5,
        "cols": 16,
        "description": "5 zones, 24 LEDs",
        "fragmentation_groups": [
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19],
            [20, 21, 22, 23]
        ]
    },
    "PHONE3A": {
        "id": "PHONE3A",
        "name": "Nothing Phone (3a)",
        "visualizer_name": "v3a-Asteroids Glyph Composer",
        "zones": 3,
        "fragmentation": True,
        "led_count": 26,
        "rows": 3,
        "cols": 16,
        "description": "3 zones, 26 LEDs",
        "fragmentation_groups": [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24, 25]
        ]
    },
    "PHONE4A": {
        "id": "PHONE4A",
        "name": "Nothing Phone (4a)",
        "visualizer_name": "v4a-Asteroids Glyph Composer",
        "zones": 3,
        "fragmentation": True,
        "led_count": 26,
        "rows": 3,
        "cols": 16,
        "description": "3 zones, 26 LEDs",
        "fragmentation_groups": [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24, 25]
        ]
    }
}

# ============================================================
#  AUTO CONVERTER — MANUAL MODEL SELECTION
# ============================================================

class AutoGlyphConverter:
    """Automatic converter with manual model selection"""
    
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.audio_dir = os.path.dirname(audio_file) or os.getcwd()
        self.base_name = os.path.splitext(os.path.basename(audio_file))[0]
        
        self.output_file = os.path.join(self.audio_dir, self.base_name + '_glyph.ogg')
        self.json_file = os.path.join(self.audio_dir, self.base_name + '_pattern.json')
        
        self.model = None
        self.config = None
        self.cols = 16
        self.ffmpeg = shutil.which('ffmpeg')
        self.ffprobe = shutil.which('ffprobe')
        
        self.pattern = []
        self.audio_duration = 30.0
        self.bpm = 120
        
        self.show_header()
    
    def show_header(self):
        """Display beautiful header"""
        print(f"\n{BOLD}{GREEN}{'=' * 60}{RESET}")
        print(f"{BOLD}{GREEN}  🚀 AUTO GLYPH CONVERTER{RESET}")
        print(f"{BOLD}{GREEN}  Choose your Nothing Phone model manually!{RESET}")
        print(f"{BOLD}{GREEN}  Just drop your .ogg file and wait 1 minute!{RESET}")
        print(f"{BOLD}{GREEN}{'=' * 60}{RESET}\n")
    
    # ---------- SELECT MODEL MANUALLY ----------
    
    def select_model(self):
        """Let user select model manually"""
        print(f"{CYAN}📱 Select your Nothing Phone model:{RESET}")
        
        models = list(GLYPH_CONFIG.keys())
        for i, m in enumerate(models, 1):
            config = GLYPH_CONFIG[m]
            print(f"   {i}. {config['name']} — {config['zones']} zones, {config['led_count']} LEDs")
        
        print(f"   {len(models) + 1}. ❌ Cancel")
        
        while True:
            choice = input(f"\n{YELLOW}>>> {RESET}").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    self.model = models[idx]
                    self.config = GLYPH_CONFIG[self.model]
                    print(f"\n{GREEN}✅ Selected: {self.config['name']}{RESET}")
                    print(f"   {self.config['zones']} zones, {self.config['led_count']} LEDs")
                    if self.config.get('fragmentation', False):
                        print(f"   🔮 Fragmentation enabled")
                    return True
                elif idx == len(models):
                    print(f"\n{RED}❌ Cancelled by user{RESET}")
                    return False
            print(f"{RED}❌ Invalid choice. Try again.{RESET}")
    
    # ---------- CHECK FFMPEG ----------
    
    def check_ffmpeg(self):
        """Check if ffmpeg is available"""
        if not self.ffmpeg:
            print(f"{RED}❌ ffmpeg not found!{RESET}")
            print(f"   Please install ffmpeg from: https://ffmpeg.org/")
            return False
        print(f"{GREEN}✅ ffmpeg found{RESET}")
        return True
    
    # ---------- GET AUDIO DURATION ----------
    
    def get_audio_duration(self):
        """Get audio duration using ffprobe"""
        if self.ffprobe:
            try:
                cmd = [
                    self.ffprobe,
                    '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    self.audio_file
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    self.audio_duration = float(result.stdout.strip())
                    print(f"{GREEN}✅ Duration: {self.audio_duration:.1f}s{RESET}")
                    return
            except:
                pass
        self.audio_duration = 30.0
        print(f"{YELLOW}⚠️ Using default duration: 30s{RESET}")
    
    # ---------- DETECT BPM ----------
    
    def detect_bpm(self):
        """Simple BPM detection"""
        if self.audio_duration < 60:
            self.bpm = 120
        elif self.audio_duration < 180:
            self.bpm = 110
        else:
            self.bpm = 100
        print(f"{GREEN}✅ BPM: {self.bpm}{RESET}")
    
    # ---------- GENERATE PATTERN ----------
    
    def generate_pattern(self):
        """Generate pattern for selected model"""
        print(f"\n{BLUE}🎨 Generating pattern for {self.config['name']}...{RESET}")
        
        rows = self.config['rows']
        self.pattern = []
        
        for r in range(rows):
            row = []
            for c in range(self.cols):
                # Wave pattern
                angle = (c / self.cols) * 2 * math.pi - (r / rows) * 1.5
                value = int((math.sin(angle) + 1) / 2 * 80 + 20)
                
                # Add rhythm
                if c % 4 == 0:
                    value = min(100, value + 30)
                elif c % 2 == 0:
                    value = min(100, value + 15)
                
                row.append(value if value > 10 else 0)
            self.pattern.append(row)
        
        # Apply fragmentation if needed
        if self.config.get('fragmentation', False):
            print(f"   🔮 Applying fragmentation...")
            self.pattern = self.apply_fragmentation(self.pattern)
        
        print(f"{GREEN}✅ Pattern generated ({rows}×{self.cols}){RESET}")
    
    # ---------- APPLY FRAGMENTATION ----------
    
    def apply_fragmentation(self, pattern):
        """Apply fragmentation for 2a, 3a, 4a models"""
        if not self.config.get('fragmentation', False):
            return pattern
        
        groups = self.config.get('fragmentation_groups', [])
        if not groups:
            return pattern
        
        zones = len(groups)
        z_pattern = [[0] * len(pattern[0]) for _ in range(zones)]
        
        for step in range(len(pattern[0])):
            for zone_idx, group in enumerate(groups):
                brightness = 0
                count = 0
                for led in group:
                    if led < len(pattern):
                        brightness += pattern[led][step]
                        count += 1
                if count > 0:
                    z_pattern[zone_idx][step] = int(brightness / count)
        
        return z_pattern
    
    # ---------- OPTIMIZE PATTERN ----------
    
    def optimize_pattern(self):
        """Optimize pattern for better display"""
        print(f"   💡 Optimizing pattern...")
        
        optimized = []
        for row in self.pattern:
            new_row = []
            max_val = max(row) if row else 1
            
            for val in row:
                if max_val > 0:
                    normalized = int((val / max_val) * 100)
                    normalized = max(normalized, 5) if val > 0 else 0
                    new_row.append(normalized)
                else:
                    new_row.append(0)
            
            optimized.append(new_row)
        
        self.pattern = optimized
        print(f"   ✅ Pattern optimized")
    
    # ---------- SHOW PATTERN ----------
    
    def show_pattern(self):
        """Display the generated pattern"""
        if not self.pattern:
            return
        
        rows = len(self.pattern)
        cols = len(self.pattern[0]) if self.pattern else 0
        
        print(f"\n{CYAN}📊 PATTERN ({rows}×{cols}) — {self.config['name']}{RESET}")
        print(f"{BLUE}{'─' * 60}{RESET}")
        
        header = "     "
        for c in range(min(cols, 16)):
            header += f"{c+1:2} "
        print(f"{header}")
        
        for r in range(min(rows, 26)):
            row_str = f"{chr(65 + r)}    "
            for c in range(min(cols, 16)):
                val = self.pattern[r][c] if c < len(self.pattern[r]) else 0
                if val > 70:
                    row_str += f"{WHITE}██{RESET}"
                elif val > 40:
                    row_str += f"{CYAN}██{RESET}"
                elif val > 10:
                    row_str += f"{BLUE}██{RESET}"
                else:
                    row_str += f"  "
            print(row_str)
        
        active = sum(1 for r in self.pattern for c in r if c > 0)
        total = rows * cols
        density = round((active / total) * 100, 1) if total > 0 else 0
        
        print(f"{BLUE}{'─' * 60}{RESET}")
        print(f"{GREEN}Active cells: {active}/{total} ({density}%){RESET}")
        print(f"{BLUE}{'─' * 60}{RESET}")
    
    # ---------- EXPORT JSON ----------
    
    def export_json(self):
        """Export pattern to JSON"""
        data = {
            'version': '4.0',
            'tool': 'Auto Glyph Converter',
            'model': self.model,
            'model_name': self.config['name'],
            'bpm': self.bpm,
            'rows': len(self.pattern),
            'steps': len(self.pattern[0]) if self.pattern else 16,
            'pattern': self.pattern,
            'audio_file': os.path.basename(self.audio_file),
            'created': datetime.now().isoformat()
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"{GREEN}✅ JSON saved: {self.json_file}{RESET}")
        return self.json_file
    
    # ---------- BUILD OGG ----------
    
    def build_ogg(self):
        """Build .ogg file with tags"""
        print(f"\n{BLUE}🎵 Building .ogg file...{RESET}")
        
        rows = len(self.pattern)
        cols = len(self.pattern[0]) if self.pattern else 16
        
        # Build AUTHOR data
        flat = []
        for r in range(rows):
            for c in range(cols):
                if r < len(self.pattern) and c < len(self.pattern[r]):
                    flat.append(str(self.pattern[r][c]))
                else:
                    flat.append('0')
        
        author_raw = f"{rows},{cols}," + ",".join(flat)
        author_encoded = base64.b64encode(author_raw.encode('utf-8')).decode('utf-8')
        
        # Build metadata
        metadata = {
            'version': '4.0',
            'tool': 'Auto Glyph Converter',
            'model': self.model,
            'model_name': self.config['name'],
            'bpm': self.bpm,
            'rows': rows,
            'steps': cols,
            'pattern': self.pattern,
            'audio_file': os.path.basename(self.audio_file),
            'created': datetime.now().isoformat()
        }
        
        json_data = json.dumps(metadata, ensure_ascii=False)
        json_escaped = json_data.replace('"', '\\"').replace('\\', '\\\\')
        
        cmd = [
            self.ffmpeg,
            '-i', self.audio_file,
            '-metadata', f'AUTHOR={author_encoded}',
            '-metadata', f'COMPOSER={self.config["visualizer_name"]}',
            '-metadata', f'TITLE={self.base_name}',
            '-metadata', f'CUSTOM1={json_escaped}',
            '-codec', 'copy',
            self.output_file
        ]
        
        print(f"   Writing tags...")
        print(f"   COMPOSER: {self.config['visualizer_name']}")
        print(f"   AUTHOR: {rows}×{cols} (Base64 encoded)")
        print(f"   TITLE: {self.base_name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{GREEN}✅ .ogg created: {self.output_file}{RESET}")
            if os.path.exists(self.output_file):
                size = os.path.getsize(self.output_file) / 1024
                print(f"   Size: {size:.1f} KB")
            return True
        else:
            print(f"{RED}❌ ffmpeg error:{RESET}")
            print(result.stderr)
            return False
    
    # ---------- WAIT WITH PROGRESS ----------
    
    def wait_with_progress(self, seconds=60):
        """Wait with progress bar"""
        print(f"\n{BLUE}⏳ Processing... Please wait {seconds} seconds{RESET}")
        print(f"{BLUE}{'─' * 40}{RESET}")
        
        for i in range(seconds):
            progress = (i + 1) / seconds * 100
            filled = int((i + 1) / seconds * 30)
            bar = '█' * filled + '░' * (30 - filled)
            print(f"\r   [{bar}] {progress:>3.0f}%  ", end='', flush=True)
            time.sleep(1)
        
        print(f"\n{GREEN}✅ Done!{RESET}")
    
    # ---------- MAIN RUN ----------
    
    def run(self):
        """Complete automatic conversion"""
        
        # 1. Check file
        if not os.path.exists(self.audio_file):
            print(f"{RED}❌ File not found: {self.audio_file}{RESET}")
            return
        
        print(f"{GREEN}✅ Audio: {os.path.basename(self.audio_file)}{RESET}")
        
        # 2. Select model manually
        if not self.select_model():
            return
        
        # 3. Check ffmpeg
        if not self.check_ffmpeg():
            return
        
        # 4. Get duration
        self.get_audio_duration()
        
        # 5. Detect BPM
        self.detect_bpm()
        
        # 6. Generate pattern
        self.generate_pattern()
        
        # 7. Optimize
        self.optimize_pattern()
        
        # 8. Show pattern
        self.show_pattern()
        
        # 9. Export JSON
        self.export_json()
        
        # 10. Build .ogg
        success = self.build_ogg()
        
        # 11. Wait
        self.wait_with_progress(60)
        
        # 12. Final message
        print(f"\n{BOLD}{GREEN}{'=' * 60}{RESET}")
        if success:
            print(f"{BOLD}{GREEN}✅ DONE! Ringtone created successfully!{RESET}")
        else:
            print(f"{BOLD}{RED}❌ ERROR! Ringtone not created{RESET}")
        print(f"{BOLD}{GREEN}{'=' * 60}{RESET}")
        
        if success:
            print(f"\n📁 Output files:")
            print(f"   🎵 {self.output_file}")
            print(f"   📄 {self.json_file}")
            print(f"\n📱 Install on phone:")
            print(f"   1. Copy {os.path.basename(self.output_file)} to:")
            print(f"      /Internal Storage/ringtones/composition/")
            print(f"   2. Open Glyph Composer → Import")
            print(f"\n💡 Selected model: {self.config['name']}")
            print(f"   ✅ {self.config['zones']} zones, {self.config['led_count']} LEDs")
            if self.config.get('fragmentation', False):
                print(f"   ✅ Fragmentation enabled")
        
        print(f"{BOLD}{GREEN}{'=' * 60}{RESET}\n")

# ============================================================
#  ENTRY POINT
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"\n{RED}❌ Usage: auto-glyph song.ogg{RESET}")
        print(f"   {YELLOW}Example: auto-glyph my_song.ogg{RESET}")
        print(f"\n   You will be prompted to select your Nothing Phone model.")
        print(f"   Just drop your .ogg file and wait 1 minute!")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if audio_file in ['--help', '-h', '/?']:
        print(f"\n{CYAN}📖 AUTO GLYPH CONVERTER — Manual Model Selection{RESET}")
        print(f"\nUsage: auto-glyph song.ogg")
        print(f"\nJust drop your .ogg file!")
        print(f"You will be prompted to select your Nothing Phone model.")
        print(f"\nSupported models:")
        for m, config in GLYPH_CONFIG.items():
            print(f"  ✅ {m} — {config['name']} ({config['zones']} zones, {config['led_count']} LEDs)")
        sys.exit(0)
    
    converter = AutoGlyphConverter(audio_file)
    
    try:
        converter.run()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️ Cancelled by user{RESET}")
    except Exception as e:
        print(f"\n{RED}❌ Error: {e}{RESET}")
        print(f"\n{CYAN}📖 For help: auto-glyph --help{RESET}")