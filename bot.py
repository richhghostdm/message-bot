import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user

    info = (
        "📩 NEW MESSAGE\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 User ID: {user.id}\n"
        f"🔗 Username: @{user.username or 'N/A'}\n\n"
        "💬 Message:"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=info
        )

        await context.bot.copy_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )

    except Exception as e:
        print(f"❌ Error: {e}")


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL & ~filters.COMMAND, forward_to_admin)
)

print("✅ Message Bot is running...")

app.run_polling()
D
