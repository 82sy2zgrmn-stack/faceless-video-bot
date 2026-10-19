import os
import logging
from telegram import Update, LabeledPrice
from telegram.ext import (
    Application, CommandHandler, PreCheckoutQueryHandler,
    MessageHandler, ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
PRICE = 100  # 100 Telegram Stars

PRODUCT = """
🎬 FACELESS VIDEO PACK

В наборе:
• 50 идей для коротких видео
• 20 сценариев
• Контент-план на 30 дней
• Советы по монтажу

Спасибо за поддержку!
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Faceless Video Pack\n\n"
        "Набор для создания коротких видео без показа лица.\n\n"
        f"Цена: {PRICE} ⭐\n\n"
        "Нажми /buy, чтобы купить набор."
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="Faceless Video Pack",
        description="Идеи, сценарии и контент-план для коротких видео",
        payload="faceless_video_pack_v1",
        currency="XTR",
        prices=[LabeledPrice("Faceless Video Pack", PRICE)],
    )

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.successful_payment.invoice_payload == "faceless_video_pack_v1":
        await update.message.reply_text(PRODUCT)

async def paysupport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "По вопросам оплаты напиши в поддержку: укажи свой Telegram username и опиши проблему."
    )

def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("paysupport", paysupport))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.run_polling()

if __name__ == "__main__":
    main()
