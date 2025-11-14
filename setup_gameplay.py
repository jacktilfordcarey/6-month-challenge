"""
Quick gameplay download helper
Run this to get a gameplay video for brainrot generation
"""

print("""
╔════════════════════════════════════════════════════════════╗
║        Brainrot Video - Gameplay Download Helper          ║
╚════════════════════════════════════════════════════════════╝

To download gameplay footage, follow these steps:

STEP 1: Install yt-dlp (if not already installed)
----------------------------------------
Run: pip install yt-dlp


STEP 2: Find a gameplay video on YouTube
----------------------------------------
Search for one of these:
• "subway surfers gameplay 10 minutes"
• "minecraft parkour gameplay"
• "temple run gameplay"

TIP: Look for videos marked as "No Copyright" or "Royalty Free"


STEP 3: Download the video
----------------------------------------
Copy the video URL and run this command:

yt-dlp -f "best[height<=720]" "YOUR_VIDEO_URL" -o gameplay.mp4

Example:
yt-dlp -f "best[height<=720]" "https://www.youtube.com/watch?v=abcd1234" -o gameplay.mp4


STEP 4: Verify the download
----------------------------------------
You should see a file called "gameplay.mp4" in this folder.


ALTERNATIVE: Use a pre-existing video
----------------------------------------
If you already have a gameplay video:
1. Rename it to "gameplay.mp4"
2. Move it to this folder
3. Make sure it's in MP4 format


READY TO GO?
----------------------------------------
Once you have gameplay.mp4:
1. Run: streamlit run lillyextractor.py
2. Upload your data
3. Generate AI Analysis
4. Click "Generate Brainrot Video"
5. Watch the magic happen! 🧠🔥

""")

# Check if gameplay video exists
import os
gameplay_files = [f for f in os.listdir('.') if 'gameplay' in f.lower() and f.endswith(('.mp4', '.avi', '.mov'))]

if gameplay_files:
    print(f"✅ Found gameplay video: {gameplay_files[0]}")
    print("You're ready to generate brainrot videos!")
else:
    print("❌ No gameplay video found yet.")
    print("\nWould you like to:")
    print("1. See download command again")
    print("2. Exit")
    
    choice = input("\nChoice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n" + "="*60)
        print("DOWNLOAD COMMAND:")
        print("="*60)
        print('\nyt-dlp -f "best[height<=720]" "YOUR_YOUTUBE_URL" -o gameplay.mp4\n')
        print("Replace YOUR_YOUTUBE_URL with the actual video URL")
        print("="*60)
