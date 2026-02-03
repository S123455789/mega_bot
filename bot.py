import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN, ADMIN_ID, FORCE_CHANNEL, LANG
from downloader import download
from buttons import quality
import database as db

# ----- Database Start -----
db.init()

# ----- Force Join Check -----
async def force_join(update, context):
    try:
        user = update.message.chat_id
        member = await context.bot.get_chat_member(FORCE_CHANNEL, user)

        if member.status == "left":
            await update.message.reply_text(LANG["join"])
            return False
        return True
    except:
        return True


# ----- Start Command -----
async def start(update: Update, context):
    if not await force_join(update, context):
        return

    db.add(str(update.message.chat_id))
    await update.message.reply_text(LANG["start"])


# ----- Link Handle -----
async def handle(update: Update, context):
    if not await force_join(update, context):
        return

    url = update.message.text

    if "http" not in url:
        await update.message.reply_text("❌ Sahi link bhejo")
        return

    await update.message.reply_text(
        "🎯 Quality select karo:",
        reply_markup=quality(url)
    )


# ----- Button Click -----
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = query.data
    qual, url = data.split("|")

    msg = await query.message.reply_text(LANG["processing"])

    try:
        file, title = download(url, qual)

        if qual == "mp3":
            await query.message.reply_audio(
                audio=open(file, "rb"),
                title=title
            )
        else:
            await query.message.reply_video(
                video=open(file, "rb"),
                caption=title
            )

        os.remove(file)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ Error:\n{e}")


# ----- Broadcast (Admin) -----
async def broadcast(update: Update, context):
    if str(update.message.chat_id) != ADMIN_ID:
        return

    text = update.message.text.replace("/broadcast ", "")

    for u in db.all_users():
        try:
            await context.bot.send_message(u, text)
        except:
            pass


# ========== MAIN START ==========

def main():
    print("🚀 KOYEB READY BOT STARTED")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.TEXT, handle))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == "__main__":
    main()
