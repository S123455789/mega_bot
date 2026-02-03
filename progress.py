async def progress(current, total, msg):
    percent = current * 100 / total
    bar = "▓" * int(percent/5) + "░" * (20-int(percent/5))

    try:
        await msg.edit_text(f"{bar} {round(percent,2)}%")
    except:
        pass