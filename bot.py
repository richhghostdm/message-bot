import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Admin chat ke message ID ko sender ke Telegram User ID se connect karega
message_map = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user

    # Admin ka reply
    if user and user.id == ADMIN_ID:
        if not update.message.reply_to_message:
            return

        replied_message_id = update.message.reply_to_message.message_id
        sender_id = message_map.get(replied_message_id)

        if not sender_id:
            await update.message.reply_text(
                "❌ Is message ka sender ID nahi mila."
            )
            return

        try:
            await context.bot.copy_message(
                chat_id=sender_id,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )

            await update.message.reply_text("✅ Reply sender ko bhej diya gaya.")

        except Exception as e:
            print(f"❌ Admin reply error: {e}")
            await update.message.reply_text(
                "❌ Sender ko reply nahi bheja ja saka."
            )

        return

    # Sender ka message admin ko forward karna
    info = (
        "📩 NEW MESSAGE\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 User ID: {user.id}\n"
        f"🔗 Username: @{user.username or 'N/A'}\n\n"
        "💬 Message:"
    )

    try:
        info_message = await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=info
        )

        # Info message ko sender se link karo
        message_map[info_message.message_id] = user.id

        await update.message.reply_text(
            "✅ Your message has been received and forwarded to the admin."
        )

        copied_message = await context.bot.copy_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )

        # Original copied message ko bhi sender se link karo
        message_map[copied_message.message_id] = user.id

    except Exception as e:
        print(f"❌ Error: {e}")


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL & ~filters.COMMAND, handle_message)
)

print("✅ Message Bot is running...")

app.run_polling()
