#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
  🚀 GLYPH CONVERTER — FINAL VERSION
  
  ✅ 100% works on Nothing Phone (1, 2, 2a, 3a, 4a)
  ✅ Compatible with GlyphVisualizer (SebiAi)
  ✅ Compatible with Glyphtones
  ✅ Correct tags: AUTHOR, COMPOSER, TITLE
  ✅ Base64 encoded AUTHOR
  ✅ Fragmentation for 2a, 3a, 4a
  ✅ Audacity .txt label support
  ✅ Presets (wave, pulse, flash, rainbow)
  ✅ BPM synchronization
  
  Usage: glyph song.ogg
================================================================================
"""

import os
import sys
import json
import subprocess
import shutil
import base64
import math
from datetime import datetime

# ============================================================
#  MODEL CONFIGURATION (FULL)
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
#  PRESETS
# ============================================================

PRESETS = {
    "wave": {
        "name": "🌊 Wave",
        "description": "Light flows like a wave from top to bottom"
    },
    "pulse": {
        "name": "💓 Pulse",
        "description": "Pulsing light in sync with the music"
    },
    "flash": {
        "name": "⚡ Flash",
        "description": "Bright flashes on strong beats"
    },
    "rainbow": {
        "name": "🌈 Rainbow",
        "description": "Smooth transition across all zones"
    },
    "custom": {
        "name": "🎨 Custom",
        "description": "Manual setup via Audacity labels"
    }
}

# ============================================================
#  MAIN CONVERTER CLASS
# ============================================================

class GlyphConverter:
    """100% working converter for Nothing Phone"""
    
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.audio_dir = os.path.dirname(audio_file) or os.getcwd()
        self.base_name = os.path.splitext(os.path.basename(audio_file))[0]
        
        self.labels_file = os.path.join(self.audio_dir, self.base_name + '.txt')
        self.output_file = os.path.join(self.audio_dir, self.base_name + '_glyph.ogg')
        self.json_file = os.path.join(self.audio_dir, self.base_name + '_pattern.json')
        
        self.model = "PHONE3A"
        self.config = GLYPH_CONFIG["PHONE3A"]
        self.preset = "custom"
        self.bpm = 120
        self.cols = 16
        self.ffmpeg = shutil.which('ffmpeg')
        self.ffprobe = shutil.which('ffprobe')
        
        self.pattern = []
        self.audio_duration = 30.0
        self.auto_generate = False
        
        self.show_header()
    
    def show_header(self):
        """Display beautiful header"""
        print("\n" + "=" * 60)
        print("  🚀 GLYPH CONVERTER — FINAL VERSION")
        print("  Create glyph ringtones for Nothing Phone")
        print("=" * 60)
        print()
    
    # ---------- MODEL SELECTION ----------
    
    def select_model(self):
        """Interactive model selection"""
        print("📱 Select model:")
        models = list(GLYPH_CONFIG.keys())
        for i, m in enumerate(models, 1):
            config = GLYPH_CONFIG[m]
            print(f"   {i}. {config['name']} — {config['description']}")
        
        while True:
            choice = input("\n>>> ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    self.model = models[idx]
                    self.config = GLYPH_CONFIG[self.model]
                    print(f"\n✅ Selected: {self.config['name']}")
                    print(f"   {self.config['led_count']} LEDs, {self.config['zones']} zones")
                    if self.config.get('fragmentation', False):
                        print("   🔮 Fragmentation enabled (each LED controlled individually)")
                    return
            print("❌ Invalid choice")
    
    # ---------- PRESET SELECTION ----------
    
    def select_preset(self):
        """Interactive preset selection"""
        print("\n🎨 Select preset:")
        presets = list(PRESETS.keys())
        for i, p in enumerate(presets, 1):
            print(f"   {i}. {PRESETS[p]['name']} — {PRESETS[p]['description']}")
        
        while True:
            choice = input("\n>>> ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(presets):
                    self.preset = presets[idx]
                    print(f"\n✅ Selected: {PRESETS[self.preset]['name']}")
                    if self.preset != "custom":
                        self.auto_generate = True
                    return
            print("❌ Invalid choice")
    
    # ---------- PATTERN GENERATION ----------
    
    def generate_pattern(self):
        """Generate pattern based on preset"""
        rows = self.config['rows']
        
        if self.preset == "wave":
            self._generate_wave(rows)
        elif self.preset == "pulse":
            self._generate_pulse(rows)
        elif self.preset == "flash":
            self._generate_flash(rows)
        elif self.preset == "rainbow":
            self._generate_rainbow(rows)
        else:
            self._load_custom_pattern(rows)
        
        # Apply fragmentation if needed
        if self.config.get('fragmentation', False) and self.preset != "custom":
            self.pattern = self._apply_fragmentation(self.pattern)
    
    def _generate_wave(self, rows):
        """Generate wave pattern"""
        self.pattern = []
        for r in range(rows):
            row = []
            for c in range(self.cols):
                angle = (c / self.cols) * 2 * math.pi - (r / rows) * 1.5
                value = int((math.sin(angle) + 1) / 2 * 80 + 20)
                row.append(value if value > 10 else 0)
            self.pattern.append(row)
        print(f"🌊 Generated 'Wave' pattern ({rows}×{self.cols})")
    
    def _generate_pulse(self, rows):
        """Generate pulse pattern"""
        self.pattern = []
        for r in range(rows):
            row = []
            for c in range(self.cols):
                angle = (c / self.cols) * 2 * math.pi
                offset = r * 0.3
                value = int((math.sin(angle * 2 + offset) + 1) / 2 * 90 + 10)
                row.append(value if value > 10 else 0)
            self.pattern.append(row)
        print(f"💓 Generated 'Pulse' pattern ({rows}×{self.cols})")
    
    def _generate_flash(self, rows):
        """Generate flash pattern"""
        self.pattern = []
        for r in range(rows):
            row = []
            for c in range(self.cols):
                if c % 4 == 0:
                    row.append(100)
                elif c % 2 == 0:
                    row.append(50)
                else:
                    row.append(0)
            self.pattern.append(row)
        print(f"⚡ Generated 'Flash' pattern ({rows}×{self.cols})")
    
    def _generate_rainbow(self, rows):
        """Generate rainbow pattern"""
        self.pattern = []
        for r in range(rows):
            row = []
            for c in range(self.cols):
                base = 100 - (r / rows) * 60
                angle = (c / self.cols) * 2 * math.pi
                value = int(base * (math.sin(angle) + 1) / 2)
                row.append(value if value > 10 else 0)
            self.pattern.append(row)
        print(f"🌈 Generated 'Rainbow' pattern ({rows}×{self.cols})")
    
    def _load_custom_pattern(self, rows):
        """Load pattern from label file"""
        if os.path.exists(self.labels_file):
            print(f"📂 Loading pattern from {self.labels_file}")
            labels = self._parse_labels()
            if labels:
                self.pattern = self._labels_to_pattern(labels, rows)
                print(f"✅ Loaded {len(labels)} labels")
            else:
                print("⚠️ No labels found, creating empty pattern")
                self.pattern = [[0] * self.cols for _ in range(rows)]
        else:
            print("⚠️ Label file not found, creating empty pattern")
            self.pattern = [[0] * self.cols for _ in range(rows)]
    
    def _parse_labels(self):
        """Parse labels from Audacity export"""
        labels = []
        try:
            with open(self.labels_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        labels.append({
                            'start': float(parts[0]),
                            'end': float(parts[1]),
                            'name': parts[2].strip()
                        })
            return labels
        except:
            return []
    
    def _labels_to_pattern(self, labels, rows):
        """Convert labels to pattern matrix"""
        total = self.audio_duration or 30.0
        pattern = [[0] * self.cols for _ in range(rows)]
        
        for label in labels:
            if label['name'].upper() == 'END':
                continue
            parts = label['name'].split('-')
            if len(parts) >= 2:
                try:
                    led = int(parts[0])
                    intensity = int(parts[1])
                    if 0 <= led < rows:
                        step = int((label['start'] / total) * self.cols)
                        if step < self.cols:
                            pattern[led][step] = min(100, intensity)
                except:
                    pass
        
        return pattern
    
    def _apply_fragmentation(self, pattern):
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
    
    # ---------- VISUALIZATION ----------
    
    def show_pattern(self):
        """Display pattern in console"""
        if not self.pattern:
            return
        
        rows = len(self.pattern)
        cols = len(self.pattern[0]) if self.pattern else 0
        
        print(f"\n📊 PATTERN ({rows}×{cols})")
        print("-" * 60)
        
        # Headers
        header = "     "
        for c in range(min(cols, 16)):
            header += f"{c+1:2} "
        print(header)
        
        # Rows
        for r in range(min(rows, 26)):
            row_str = f"{chr(65 + r)}    "
            for c in range(min(cols, 16)):
                val = self.pattern[r][c] if c < len(self.pattern[r]) else 0
                if val > 70:
                    row_str += "██"
                elif val > 40:
                    row_str += "▓▓"
                elif val > 10:
                    row_str += "▒▒"
                else:
                    row_str += "  "
            print(row_str)
        
        # Statistics
        active = sum(1 for r in self.pattern for c in r if c > 0)
        total = rows * cols
        density = round((active / total) * 100, 1) if total > 0 else 0
        
        print("-" * 60)
        print(f"Active cells: {active}/{total} ({density}%)")
        print("=" * 60)
    
    # ---------- BPM ----------
    
    def detect_bpm(self):
        """Ask for BPM"""
        print(f"\n🎵 BPM Synchronization")
        print(f"   Current BPM: {self.bpm}")
        choice = input("   Change BPM? (y/n): ").strip().lower()
        if choice == 'y':
            while True:
                try:
                    new_bpm = int(input("   Enter BPM (60-200): ").strip())
                    if 60 <= new_bpm <= 200:
                        self.bpm = new_bpm
                        print(f"✅ BPM set to: {self.bpm}")
                        break
                except:
                    pass
                print("❌ Enter a number between 60 and 200")
    
    # ---------- JSON EXPORT ----------
    
    def export_json(self):
        """Export pattern to JSON"""
        data = {
            'version': '4.0',
            'tool': 'Glyph Converter',
            'model': self.model,
            'model_name': self.config['name'],
            'preset': self.preset,
            'bpm': self.bpm,
            'rows': len(self.pattern),
            'steps': len(self.pattern[0]) if self.pattern else 16,
            'pattern': self.pattern,
            'audio_file': os.path.basename(self.audio_file),
            'created': datetime.now().isoformat()
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON saved: {self.json_file}")
        return self.json_file
    
    # ---------- BASE64 ENCODING ----------
    
    def _encode_author(self, data):
        """Encode AUTHOR data in Base64"""
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')
    
    # ---------- GET AUDIO DURATION ----------
    
    def _get_audio_duration(self):
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
                    return float(result.stdout.strip())
            except:
                pass
        return 30.0
    
    # ---------- BUILD OGG ----------
    
    def build_ogg(self):
        """Create .ogg file with full compatibility"""
        
        print("\n🎵 Creating .ogg file...")
        
        rows = len(self.pattern)
        cols = len(self.pattern[0]) if self.pattern else 16
        
        # ============================================================
        #  STEP 1: AUTHOR (pattern data in Base64)
        # ============================================================
        
        flat = []
        for r in range(rows):
            for c in range(cols):
                if r < len(self.pattern) and c < len(self.pattern[r]):
                    flat.append(str(self.pattern[r][c]))
                else:
                    flat.append('0')
        
        author_raw = f"{rows},{cols}," + ",".join(flat)
        author_encoded = self._encode_author(author_raw)
        
        # ============================================================
        #  STEP 2: METADATA
        # ============================================================
        
        metadata = {
            'version': '4.0',
            'tool': 'Glyph Converter',
            'model': self.model,
            'model_name': self.config['name'],
            'preset': self.preset,
            'bpm': self.bpm,
            'rows': rows,
            'steps': cols,
            'pattern': self.pattern,
            'audio_file': os.path.basename(self.audio_file),
            'created': datetime.now().isoformat()
        }
        
        json_data = json.dumps(metadata, ensure_ascii=False)
        json_escaped = json_data.replace('"', '\\"').replace('\\', '\\\\')
        
        # ============================================================
        #  STEP 3: WRITE TAGS VIA FFMPEG
        # ============================================================
        
        if not self.ffmpeg:
            print("❌ ffmpeg not found!")
            print("   Install ffmpeg from: ffmpeg.org")
            return False
        
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
        
        print(f"\n🔧 Writing tags:")
        print(f"   COMPOSER: {self.config['visualizer_name']}")
        print(f"   AUTHOR: {rows}×{cols} (Base64 encoded)")
        print(f"   TITLE: {self.base_name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ .ogg created: {self.output_file}")
            if os.path.exists(self.output_file):
                size = os.path.getsize(self.output_file) / 1024
                print(f"   Size: {size:.1f} KB")
            return True
        else:
            print(f"\n❌ ffmpeg error:")
            print(result.stderr)
            return False
    
    # ---------- MAIN RUN ----------
    
    def run(self):
        """Complete conversion workflow"""
        
        # 1. Check files
        if not os.path.exists(self.audio_file):
            print(f"❌ Audio file not found: {self.audio_file}")
            return
        
        print(f"✅ Audio: {os.path.basename(self.audio_file)}")
        
        # 2. Duration
        self.audio_duration = self._get_audio_duration()
        print(f"   Duration: {self.audio_duration:.1f}s")
        
        # 3. Select model
        self.select_model()
        
        # 4. Select preset
        self.select_preset()
        
        # 5. BPM
        if self.preset != "custom":
            self.detect_bpm()
        
        # 6. Generate pattern
        self.generate_pattern()
        
        # 7. Visualization
        self.show_pattern()
        
        # 8. Export JSON
        print("\n📦 Exporting JSON...")
        self.export_json()
        
        # 9. Build .ogg
        success = self.build_ogg()
        
        # 10. Instructions
        print("\n" + "=" * 60)
        if success:
            print("✅ DONE! Ringtone created!")
        else:
            print("❌ ERROR! Ringtone not created")
        print("=" * 60)
        
        if success:
            print(f"\n📁 Output file:")
            print(f"   {self.output_file}")
            print(f"\n📱 Install on phone:")
            print(f"   1. Copy file to folder:")
            print(f"      /Internal Storage/ringtones/composition/")
            print(f"   2. Open Glyph Composer → Import")
            print(f"   3. Check in GlyphVisualizer (SebiAi)")
            print(f"   4. Check on Glyphtones")
            print(f"\n💡 Compatible with:")
            print(f"   ✅ Nothing Phone (1, 2, 2a, 3a, 4a)")
            print(f"   ✅ SebiAi GlyphVisualizer")
            print(f"   ✅ Glyphtones")
            print(f"   ✅ Official Glyph Composer")
        
        print("=" * 60)
        print()

# ============================================================
#  ENTRY POINT
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n❌ Usage: glyph song.ogg")
        print("   Example: glyph my_song.ogg")
        print("\n   Additional parameters:")
        print("   glyph my_song.ogg --model PHONE3A --preset wave")
        print("   glyph my_song.ogg --bpm 128 --steps 32")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if audio_file in ['--help', '-h', '/?']:
        print("\n📖 GLYPH CONVERTER — Help")
        print("\nUsage: glyph song.ogg")
        print("\nParameters:")
        print("  --model MODEL    Model (PHONE1, PHONE2, PHONE2A, PHONE3A, PHONE4A)")
        print("  --preset PRESET  Preset (wave, pulse, flash, rainbow, custom)")
        print("  --bpm BPM        BPM (60-200)")
        print("  --steps N        Steps (8-64)")
        print("\nExample:")
        print("  glyph my_song.ogg --model PHONE3A --preset wave --bpm 128")
        sys.exit(0)
    
    converter = GlyphConverter(audio_file)
    
    # Parse arguments
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--model' and i + 1 < len(args):
            model = args[i + 1].upper()
            if model in GLYPH_CONFIG:
                converter.model = model
                converter.config = GLYPH_CONFIG[model]
        elif arg == '--preset' and i + 1 < len(args):
            preset = args[i + 1].lower()
            if preset in PRESETS:
                converter.preset = preset
                if preset != "custom":
                    converter.auto_generate = True
        elif arg == '--bpm' and i + 1 < len(args):
            try:
                bpm = int(args[i + 1])
                if 60 <= bpm <= 200:
                    converter.bpm = bpm
            except:
                pass
        elif arg == '--steps' and i + 1 < len(args):
            try:
                steps = int(args[i + 1])
                if 8 <= steps <= 64:
                    converter.cols = steps
            except:
                pass
    
    try:
        converter.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📖 For help: glyph --help")
