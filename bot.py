from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from yt_dlp import YoutubeDL
import os

BOT_TOKEN = '7563398928:AAFKQHwtmc-YeesXlQWbS280SuUBy2JFFSE'

def search_youtube(query):
    with YoutubeDL({'quiet': True}) as ydl:
        return ydl.extract_info(f"ytsearch10:{query}", download=False)['entries'][:10]

def download_audio(url):
    filename = "audio.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qo‘shiq nomini yuboring:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = search_youtube(query)
    buttons = [[InlineKeyboardButton(f"{i+1}. {v['title'][:50]}", callback_data=v['webpage_url'])] for i, v in enumerate(results)]
    await update.message.reply_text("Natijalar:", reply_markup=InlineKeyboardMarkup(buttons))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    url = q.data
    try:
        file = download_audio(url)
        await context.bot.send_audio(chat_id=q.message.chat.id, audio=open(file, 'rb'))
        os.remove(file)
    except:
        await q.message.reply_text("Xatolik yuz berdi.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.run_polling()
