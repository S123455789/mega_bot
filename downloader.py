import yt_dlp

def download(url, quality):
    if quality == "mp3":
        opt = {
            'format': 'bestaudio',
            'outtmpl': 'audio.mp3',
            'postprocessors':[{
                'key':'FFmpegExtractAudio',
                'preferredcodec':'mp3'
            }]
        }
        file="audio.mp3"
    else:
        opt = {
            'format': f'best[height<={quality}]',
            'outtmpl':'video.mp4'
        }
        file="video.mp4"

    with yt_dlp.YoutubeDL(opt) as y:
        info = y.extract_info(url, download=True)

    return file, info.get("title")