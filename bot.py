import os
import traceback

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TOKEN
from processor import process_excel


TEMP_DIR = "temp"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Отправь Excel-файл (.xlsx), и я создам русификаторы."
    )


async def handle_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document.file_name.lower().endswith(".xlsx"):

        await update.message.reply_text(
            "Пожалуйста, отправьте Excel-файл (.xlsx)."
        )
        return

    await update.message.reply_text(
        "📄 Файл получен.\nНачинаю обработку..."
    )

    os.makedirs(TEMP_DIR, exist_ok=True)

    input_path = os.path.join(TEMP_DIR, document.file_name)

    telegram_file = await document.get_file()
    await telegram_file.download_to_drive(input_path)

    try:

        files, categories = process_excel(input_path)

        for filename in files:

            with open(filename, "rb") as f:

                await update.message.reply_document(f)

            os.remove(filename)

        os.remove(input_path)

        await update.message.reply_text("✅ Готово!")

    except Exception as e:
        
        traceback.print_exc()

        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            handle_excel
        )
    )

    print("Бот запущен...")

    app.run_polling()


if __name__ == "__main__":
    main()