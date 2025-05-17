import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"

logging.basicConfig(level=logging.INFO)

# Hàm xử lý tin nhắn
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = str(update.effective_user.id)

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "inputs": {},  # nếu bạn cần truyền input phụ thì điền ở đây
        "query": user_message,
        "user": user_id,
    }

    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            reply = response.json().get("answer", "Không có phản hồi từ chatbot.")
        else:
            logging.error(f"Dify API error: {response.status_code} {response.text}")
            reply = "Chatbot gặp lỗi khi phản hồi."
    except Exception as e:
        logging.exception("Lỗi khi gọi Dify API")
        reply = "Đã xảy ra lỗi."

    await update.message.reply_text(reply)

# Chạy bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot đang chạy... Nhắn tin thử vào Telegram để kiểm tra.")
    app.run_polling()

if __name__ == "__main__":
    main()
