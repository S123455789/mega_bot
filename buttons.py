from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def quality(url):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("360p", callback_data=f"360|{url}"),
            InlineKeyboardButton("720p", callback_data=f"720|{url}")
        ],
        [
            InlineKeyboardButton("1080p", callback_data=f"1080|{url}"),
            InlineKeyboardButton("🎵 MP3", callback_data=f"mp3|{url}")
        ]
    ])