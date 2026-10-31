"""Telegram interface. Configure TELEGRAM_BOT_TOKEN in the environment."""
import asyncio
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from predict import predict


def main():
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN in your environment")
    weights = Path(os.environ.get("MODEL_WEIGHTS", "weights/best.pt"))
    if not weights.is_file():
        raise SystemExit(f"Trained weights not found: {weights}")

    async def start(update, context):
        await update.effective_message.reply_text(
            "Отправьте фотографию яиц Manduca sexta. Я верну разметку и число обнаруженных объектов."
        )

    async def photo(update, context):
        message = update.effective_message
        try:
            with TemporaryDirectory(prefix="egg-counter-") as directory:
                source = Path(directory) / "input.jpg"
                output = Path(directory) / "prediction.jpg"
                file = await message.photo[-1].get_file()
                await file.download_to_drive(custom_path=source)
                result = await asyncio.to_thread(predict, weights, source, output)
                with output.open("rb") as image:
                    await message.reply_photo(image, caption=f"Обнаружено яиц: {result['count']}")
        except Exception:
            # Do not log request URLs: they can contain the Telegram token.
            await message.reply_text("Не удалось обработать фото. Проверьте изображение и настройки модели.")

    app = ApplicationBuilder().token(token).concurrent_updates(False).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo))
    app.run_polling()


if __name__ == "__main__":
    main()
