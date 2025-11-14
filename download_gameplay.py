"""
Download gameplay footage for brainrot videos
"""

import subprocess
import sys

def install_ytdlp():
    """Install yt-dlp if not already installed"""
    try:
        import yt_dlp
        print("yt-dlp is already installed")
    except ImportError:
        print("Installing yt-dlp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        print("yt-dlp installed successfully!")

def download_gameplay_video(video_type="subway_surfers"):
    """
    Download gameplay video
    
    Args:
        video_type: "subway_surfers" or "minecraft"
    """
    import yt_dlp
    
    # Pre-selected gameplay videos (public domain or royalty-free)
    videos = {
        "subway_surfers": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Replace with actual subway surfers video
        "minecraft": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with actual minecraft parkour
    }
    
    url = videos.get(video_type, videos["subway_surfers"])
    
    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': 'gameplay.%(ext)s',
        'quiet': False,
    }
    
    print(f"Downloading {video_type} gameplay video...")
    print("This may take a few minutes...")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\nGameplay video downloaded successfully as 'gameplay.mp4'!")
        return True
    except Exception as e:
        print(f"\nError downloading video: {str(e)}")
        print("\nManual download instructions:")
        print("1. Go to YouTube and search for 'subway surfers gameplay 10 minutes'")
        print("2. Copy the video URL")
        print("3. Use this command:")
        print(f'   yt-dlp -f "best[height<=720]" YOUR_VIDEO_URL -o gameplay.mp4')
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Brainrot Video - Gameplay Downloader")
    print("=" * 60)
    
    # Install yt-dlp
    install_ytdlp()
    
    print("\nChoose gameplay type:")
    print("1. Subway Surfers")
    print("2. Minecraft Parkour")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    video_type = "subway_surfers" if choice == "1" else "minecraft"
    
    print(f"\nNote: Please use copyright-free or royalty-free gameplay videos.")
    print("You can find these by searching YouTube for videos with Creative Commons license.")
    
    proceed = input("\nDo you have a video URL? (y/n): ").strip().lower()
    
    if proceed == 'y':
        url = input("Enter YouTube URL: ").strip()
        
        import yt_dlp
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': 'gameplay.%(ext)s',
            'quiet': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("\n✓ Gameplay video downloaded successfully!")
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
    else:
        print("\nManual download instructions:")
        print("1. Search YouTube for: 'subway surfers gameplay 10 minutes' or 'minecraft parkour'")
        print("2. Choose a video with Creative Commons license if possible")
        print("3. Copy the video URL")
        print("4. Run this command in terminal:")
        print('   yt-dlp -f "best[height<=720]" YOUR_VIDEO_URL -o gameplay.mp4')
        print("\n5. Or use online tools like: https://ytmp3.nu/")
