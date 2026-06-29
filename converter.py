#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
  🛠️  GLYPH CONVERTER — with AUTHOR, COMPOSER, TITLE tags support
  
  Compatible with GlyphVisualizer and Nothing Phone!
  Usage: glyph song.ogg
================================================================================
"""

import os
import sys
import json
import subprocess
import shutil
from datetime import datetime

# ============================================================
#  GLYPH CONFIGURATION — ALL NOTHING PHONE MODELS
# ============================================================

GLYPH_CONFIG = {
    "PHONE1": {
        "name": "Nothing Phone (1)",
        "zones": 12,
        "fragmentation": False,
        "led_count": 12,
        "description": "12 zones"
    },
    "PHONE2": {
        "name": "Nothing Phone (2)",
        "zones": 33,
        "fragmentation": False,
        "led_count": 33,
        "description": "33 zones"
    },
    "PHONE2A": {
        "name": "Nothing Phone (2a)",
        "zones": 5,
        "fragmentation": True,
        "led_count": 24,
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
        "name": "Nothing Phone (3a)",
        "zones": 3,
        "fragmentation": True,
        "led_count": 26,
        "description": "3 zones, 26 LEDs (each LED individually!)",
        "fragmentation_groups": [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24, 25]
        ]
    },
    "PHONE4A": {
        "name": "Nothing Phone (4a)",
        "zones": 3,
        "fragmentation": True,
        "led_count": 26,
        "description": "3 zones, 26 LEDs (each LED individually!)",
        "fragmentation_groups": [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24, 25]
        ]
    }
}

# ============================================================
#  GLYPH CONVERTER CLASS
# ============================================================

class GlyphConverter:
    """Main converter class with AUTHOR, COMPOSER, TITLE tags support"""
    
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.audio_dir = os.path.dirname(audio_file) or os.getcwd()
        self.base_name = os.path.splitext(os.path.basename(audio_file))[0]
        
        self.labels_file = os.path.join(self.audio_dir, self.base_name + '.txt')
        self.output_file = os.path.join(self.audio_dir, self.base_name + '_glyph.ogg')
        
        self.model = "PHONE3A"
        self.config = GLYPH_CONFIG["PHONE3A"]
        self.ffmpeg = shutil.which('ffmpeg')
        self.ffprobe = shutil.which('ffprobe')
    
    # ---------- CHECK FILES ----------
    
    def check_files(self):
        """Check if required files exist"""
        print("\n" + "=" * 60)
        print("  🛠️  GLYPH CONVERTER")
        print("=" * 60)
        
        print(f"\n📁 Working folder: {self.audio_dir}")
        
        if not os.path.exists(self.audio_file):
            print(f"\n❌ Audio file not found: {self.audio_file}")
            return False
        print(f"\n✅ Audio: {os.path.basename(self.audio_file)}")
        
        if not os.path.exists(self.labels_file):
            print(f"\n❌ Label file not found: {self.labels_file}")
            print("\n📝 How to create labels in Audacity:")
            print("  1. Open your audio in Audacity")
            print("  2. Tracks → Add New → Label Track")
            print("  3. Place labels (0-100, 5-50, 12-100, END)")
            print("  4. File → Export → Export Labels...")
            print(f"  5. Save as: {self.labels_file}")
            return False
        print(f"✅ Labels: {os.path.basename(self.labels_file)}")
        
        return True
    
    # ---------- ASK MODEL ----------
    
    def ask_model(self):
        """Ask user to select phone model"""
        print("\n📱 Choose your model:")
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
                        print("   🔮 Fragmentation ON (each LED controlled individually)")
                    return True
            print("❌ Invalid choice. Try again.")
    
    # ---------- PARSE LABELS ----------
    
    def parse_labels(self):
        """Parse labels from Audacity export"""
        labels = []
        end_time = 0
        
        with open(self.labels_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) >= 3:
                    start = float(parts[0])
                    end = float(parts[1])
                    name = parts[2].strip()
                    
                    if name.upper() == 'END':
                        end_time = start
                        continue
                    
                    labels.append({
                        'start': start,
                        'end': end,
                        'name': name
                    })
        
        return labels, end_time
    
    def parse_to_pattern(self, labels, duration, cols=16):
        """Convert labels to LED pattern matrix"""
        led_count = self.config['led_count']
        pattern = [[0] * cols for _ in range(led_count)]
        
        for label in labels:
            name = label['name'].upper()
            parts = name.split('-')
            if len(parts) >= 2:
                try:
                    led = int(parts[0])
                    intensity = int(parts[1])
                    if 0 <= led < led_count and duration > 0:
                        step = int((label['start'] / duration) * cols)
                        if step < cols:
                            pattern[led][step] = min(100, intensity)
                except:
                    pass
        
        return pattern
    
    def apply_fragmentation(self, pattern):
        """Apply fragmentation: LED groups → physical zones"""
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
    
    def to_blocks(self, pattern):
        """Convert pattern to blocks for JSON"""
        blocks = []
        for r in range(len(pattern)):
            start = -1
            for c in range(len(pattern[r])):
                if pattern[r][c] > 0 and start == -1:
                    start = c
                if pattern[r][c] == 0 and start != -1:
                    blocks.append({'row': r, 'start': start, 'end': c-1})
                    start = -1
            if start != -1:
                blocks.append({'row': r, 'start': start, 'end': len(pattern[r])-1})
        return blocks
    
    def get_stats(self, pattern):
        """Get pattern statistics"""
        active = sum(1 for r in pattern for c in r if c > 0)
        total = len(pattern) * len(pattern[0])
        return {
            'active': active,
            'total': total,
            'density': round((active/total)*100, 1) if total > 0 else 0
        }
    
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
                    return float(result.stdout.strip())
            except:
                pass
        return 30.0
    
    # ============================================================
    #  BUILD OGG WITH AUTHOR, COMPOSER, TITLE TAGS
    # ============================================================
    
    def build_ogg(self, pattern, blocks):
        """
        Create .ogg file with AUTHOR, COMPOSER, TITLE tags
        Compatible with GlyphVisualizer and Nothing Phone
        """
        
        rows = len(pattern)
        cols = len(pattern[0]) if pattern else 16
        
        # ============================================================
        #  STEP 1: CREATE AUTHOR DATA (SebiAi format)
        # ============================================================
        
        flat_data = []
        for r in range(rows):
            for c in range(cols):
                if r < len(pattern) and c < len(pattern[r]):
                    flat_data.append(str(pattern[r][c]))
                else:
                    flat_data.append('0')
        
        # Format: "rows,cols,value1,value2,value3,..."
        author_data = f"{rows},{cols}," + ",".join(flat_data)
        
        # ============================================================
        #  STEP 2: CREATE METADATA FOR CUSTOM1
        # ============================================================
        
        metadata = {
            'version': '2.0',
            'tool': 'Glyph Converter',
            'model': self.model,
            'model_name': self.config['name'],
            'zones': self.config['zones'],
            'fragmentation': self.config['fragmentation'],
            'led_count': self.config['led_count'],
            'rows': rows,
            'steps': cols,
            'pattern': pattern,
            'blocks': blocks,
            'audio_file': os.path.basename(self.audio_file),
            'created': datetime.now().isoformat()
        }
        
        json_data = json.dumps(metadata, ensure_ascii=False, separators=(',', ':'))
        
        # ============================================================
        #  STEP 3: WRITE TO .ogg USING FFMPEG
        # ============================================================
        
        if self.ffmpeg:
            author_escaped = author_data.replace('"', '\\"')
            json_escaped = json_data.replace('"', '\\"').replace('\\', '\\\\')
            
            # ============================================================
            #  ВАЖНО! Используем полное имя модели для COMPOSER
            # ============================================================
            
            cmd = [
                self.ffmpeg,
                '-i', self.audio_file,
                '-metadata', f'AUTHOR={author_escaped}',
                '-metadata', f'COMPOSER={self.config["name"]}',      # ← ИСПРАВЛЕНО!
                '-metadata', f'TITLE={self.base_name}',
                '-metadata', f'CUSTOM1={json_escaped}',
                '-metadata', f'GLYPH_MODEL={self.model}',
                '-codec', 'copy',
                self.output_file
            ]
            
            print(f"\n🔧 Writing tags:")
            print(f"   AUTHOR: {rows}x{cols} = {rows * cols} values")
            print(f"   COMPOSER: {self.config['name']}")
            print(f"   TITLE: {self.base_name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return True, metadata
            else:
                print(f"⚠️ ffmpeg warning: {result.stderr}")
                # Fallback: save JSON
                json_file = os.path.splitext(self.output_file)[0] + '.json'
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                return False, metadata
        else:
            print("⚠️ ffmpeg not found! Saving JSON only.")
            print("   Install ffmpeg from: https://ffmpeg.org/")
            json_file = os.path.splitext(self.output_file)[0] + '.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            return False, metadata
    
    # ---------- SHOW HELP ----------
    
    def show_help(self):
        """Display help information"""
        print("""
================================================================================
  🛠️  GLYPH CONVERTER — Help
================================================================================

USAGE:
  glyph song.ogg
  python converter.py song.ogg

WHAT IT DOES:
  1. Finds song.txt (same name as song.ogg) in the same folder
  2. Parses your Audacity labels
  3. Applies glyph fragmentation (if supported)
  4. Creates song_glyph.ogg with AUTHOR, COMPOSER, TITLE tags

REQUIRED FILES:
  song.ogg  - Your audio file (from Audacity)
  song.txt  - Your labels (from Audacity)

LABEL FORMAT:
  LED-INTENSITY  (e.g. 0-100, 5-50, 12-100, END)

SUPPORTED MODELS:
  PHONE1, PHONE2, PHONE2A, PHONE3A, PHONE4A

OUTPUT:
  song_glyph.ogg  - Ready to install on your Nothing Phone!
================================================================================
""")
    
    # ---------- MAIN RUN ----------
    
    def run(self):
        """Main run method"""
        if not self.check_files():
            return
        
        self.ask_model()
        
        print("\n📊 Parsing labels...")
        labels, end_time = self.parse_labels()
        if not labels:
            print("❌ No labels found")
            return
        
        duration = self.get_audio_duration()
        if duration == 0:
            duration = end_time
        
        cols = 16
        raw_pattern = self.parse_to_pattern(labels, duration, cols)
        
        if self.config.get('fragmentation', False):
            print(f"🔮 Applying fragmentation: {self.config['led_count']} LEDs → {self.config['zones']} zones")
            pattern = self.apply_fragmentation(raw_pattern)
        else:
            pattern = raw_pattern
        
        blocks = self.to_blocks(pattern)
        stats = self.get_stats(pattern)
        
        print(f"\n✅ Active cells: {stats['active']}/{stats['total']} ({stats['density']}%)")
        print(f"   Blocks: {len(blocks)}")
        
        print(f"\n🎵 Creating {self.output_file}...")
        success, metadata = self.build_ogg(pattern, blocks)
        
        if success:
            print(f"\n✅ DONE! File: {self.output_file}")
            if os.path.exists(self.output_file):
                size = os.path.getsize(self.output_file) / 1024
                print(f"   Size: {size:.1f} KB")
        else:
            print(f"\n⚠️ Saved JSON: {os.path.splitext(self.output_file)[0] + '.json'}")
        
        print("\n" + "=" * 60)
        print("📱 INSTRUCTIONS FOR PHONE")
        print("=" * 60)
        print("1. Copy .ogg to folder:")
        print("   /Internal Storage/ringtones/composition/")
        print("2. Open Glyph Composer → Import")
        print("3. Now works in GlyphVisualizer too!")
        print("=" * 60)

# ============================================================
#  MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) < 2:
        print("\n❌ Usage: glyph song.ogg")
        print("   Example: glyph my_song.ogg")
        print("\n📖 For help: glyph --help")
        sys.exit(1)
    
    # Show help
    if sys.argv[1] in ['--help', '-h', '/?']:
        converter = GlyphConverter("dummy.ogg")
        converter.show_help()
        sys.exit(0)
    
    # Run converter
    converter = GlyphConverter(sys.argv[1])
    try:
        converter.run()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📖 For help: glyph --help")