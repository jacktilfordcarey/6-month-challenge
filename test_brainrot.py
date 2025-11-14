"""
Quick test of brainrot video generation
"""

import os
from brainrot_video import create_brainrot_video

# Test text
test_text = """Yo fam, check this data fr fr! 
So basically we got some numbers and they're going crazy no cap. 
The stats are bussin and the results? Absolutely fire. 
This analysis hits different when you see the correlation is straight up wildin. 
We're talking maximum rizz with these insights on god."""

print("=" * 60)
print("Brainrot Video Test")
print("=" * 60)
print()
print("Test Text:")
print(test_text)
print()
print("Starting video generation...")
print("This will take 1-2 minutes...")
print()

try:
    video_path = create_brainrot_video(
        text=test_text,
        background_video_path="gameplay.mp4",
        output_path="output_folder/test_brainrot.mp4"
    )
    
    print()
    print("=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print(f"Video saved to: {video_path}")
    print()
    print("You can now:")
    print("1. Open the video file to watch it")
    print("2. Use LillyExtractor to generate brainrot videos from your data!")
    print()
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERROR")
    print("=" * 60)
    print(f"Error: {str(e)}")
    print()
    print("Try running: streamlit run lillyextractor.py")
    print("and generate from the UI instead")
