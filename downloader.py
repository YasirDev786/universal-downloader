import yt_dlp
import re
import os
from uuid import uuid4

def download_video(url, platform):
    patterns = {
        "youtube": r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/',
        "insta": r'(https?://)?(www\.)?instagram\.com/',
        "facebook": r'(https?://)?(www\.)?facebook\.com/',
    }

    if platform not in patterns or not re.match(patterns[platform], url):
        return {"error": f"Invalid {platform} URL."}

    try:
        filename = f"{uuid4()}.mp4"
        output_path = os.path.join("downloads", filename)

        ydl_opts = {
            'outtmpl': output_path,
            'quiet': True,
            'format': 'best[ext=mp4]/best',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return {"success": "Video downloaded", "file": filename}
    except Exception as e:
        return {"error": str(e)}
