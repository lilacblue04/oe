from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

app = Flask(__name__)

# Telegram bot token and admin ID
BOT_TOKEN = "7751609623:AAFKb3Wwb_MfcdSW3GcmoMt4kshZXDwpQog"
ADMIN_ID = 710165881

# Telegram bot application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Dictionary to map admin message IDs to user IDs and original user message IDs
message_mapping = {}
# List to store admin message IDs ("b" IDs)
admin_message_ids = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("بذار بقیه چای بریزن")
    else:
        await update.message.reply_text("spill the tea ☕")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:  # Only process messages from non-admin users
        user_message = update.message
        original_user_message_id = user_message.message_id  # Track original user message ID
        await update.message.reply_text("ارسال شد!")

        # Initialize sent_message as None
        sent_message = None

        # Send the message to admin as "b"
        if user_message.text:
            sent_message = await context.bot.send_message(chat_id=ADMIN_ID, text=user_message.text)
        elif user_message.photo:
            sent_message = await context.bot.send_photo(chat_id=ADMIN_ID, photo=user_message.photo[-1].file_id, caption=user_message.caption or "")
        elif user_message.video:
            sent_message = await context.bot.send_video(chat_id=ADMIN_ID, video=user_message.video.file_id, caption=user_message.caption or "")
        elif user_message.voice:
            sent_message = await context.bot.send_voice(chat_id=ADMIN_ID, voice=user_message.voice.file_id, caption=user_message.caption or "")
        elif user_message.audio:
            sent_message = await context.bot.send_audio(chat_id=ADMIN_ID, audio=user_message.audio.file_id, caption=user_message.caption or "")
        elif user_message.document:
            sent_message = await context.bot.send_document(chat_id=ADMIN_ID, document=user_message.document.file_id, caption=user_message.caption or "")
        elif user_message.sticker:
            sent_message = await context.bot.send_sticker(chat_id=ADMIN_ID, sticker=user_message.sticker.file_id)
        elif user_message.location:
            sent_message = await context.bot.send_location(chat_id=ADMIN_ID, latitude=user_message.location.latitude, longitude=user_message.location.longitude)
        elif user_message.poll:
            sent_message = await context.bot.send_poll(chat_id=ADMIN_ID, question=user_message.poll.question, options=user_message.poll.options, is_anonymous=user_message.poll.is_anonymous)

        # Ensure we have a sent message to reference
        if sent_message:
            # Map the admin message ID to both the user ID and the original user message ID
            message_mapping[sent_message.message_id] = {
                'user_id': user_id,
                'original_user_message_id': original_user_message_id  # Add original user message ID
            }
            # Store the admin message ID
            admin_message_ids.append(sent_message.message_id)

            # Prepare the user info as "c"
            user_info = (f"User Info:\n"
                         f"ID: {user_id}\n"
                         f"Full Name: {user_message.from_user.full_name}\n"
                         f"Username: @{user_message.from_user.username}\n"
                         f"Original User Message ID: {original_user_message_id}\n"
                         f"Admin Message ID: {sent_message.message_id}")

            # Send user info to admin as a separate message
            await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)

async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    print(f"Admin message received from user ID: {user_id}")

    if update.message.reply_to_message:
        print("This message is a reply.")
        original_message_id = update.message.reply_to_message.message_id
        print(f"Original message ID: {original_message_id}")

        # Check if the replied message ID is in the list of admin messages
        if original_message_id in admin_message_ids:
            print("Original message ID found in admin_message_ids.")

            # Find the user ID associated with this original message ID
            mapping = message_mapping.get(original_message_id)
            if mapping:
                original_user_id = mapping['user_id']
                original_user_message_id = mapping['original_user_message_id']
                print(f"Mapped user ID found: {original_user_id}")

                # Send the admin's message content as a reply to the original user message
                if update.message.text:
                    await context.bot.send_message(chat_id=original_user_id, text=update.message.text, reply_to_message_id=original_user_message_id)
                    print(f"Sent text message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.photo:
                    await context.bot.send_photo(chat_id=original_user_id, photo=update.message.photo[-1].file_id, caption=update.message.caption or "", reply_to_message_id=original_user_message_id)
                    print(f"Sent photo message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.video:
                    await context.bot.send_video(chat_id=original_user_id, video=update.message.video.file_id, caption=update.message.caption or "", reply_to_message_id=original_user_message_id)
                    print(f"Sent video message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.voice:
                    await context.bot.send_voice(chat_id=original_user_id, voice=update.message.voice.file_id, caption=update.message.caption or "", reply_to_message_id=original_user_message_id)
                    print(f"Sent voice message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.audio:
                    await context.bot.send_audio(chat_id=original_user_id, audio=update.message.audio.file_id, caption=update.message.caption or "", reply_to_message_id=original_user_message_id)
                    print(f"Sent audio message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.document:
                    await context.bot.send_document(chat_id=original_user_id, document=update.message.document.file_id, caption=update.message.caption or "", reply_to_message_id=original_user_message_id)
                    print(f"Sent document message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.sticker:
                    await context.bot.send_sticker(chat_id=original_user_id, sticker=update.message.sticker.file_id, reply_to_message_id=original_user_message_id)
                    print(f"Sent sticker message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.location:
                    await context.bot.send_location(chat_id=original_user_id, latitude=update.message.location.latitude, longitude=update.message.location.longitude, reply_to_message_id=original_user_message_id)
                    print(f"Sent location message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin
                elif update.message.poll:
                    await context.bot.send_poll(chat_id=original_user_id, question=update.message.poll.question, options=update.message.poll.options, is_anonymous=update.message.poll.is_anonymous, reply_to_message_id=original_user_message_id)
                    print(f"Sent poll message to user ID {original_user_id}")
                    await update.message.reply_text("ارسال شد!")  # Confirm to admin

        else:
            print("Original message ID not found in admin_message_ids.")
            await update.message.reply_text("Reply the message to answer")
    else:
        print("Admin message is not a reply.")
        await update.message.reply_text("Reply the message to answer")

# Add command and message handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND & ~filters.User(user_id=ADMIN_ID), handle_message))  # Handle all messages
application.add_handler(MessageHandler(filters.User(user_id=ADMIN_ID), handle_admin_message))  # Handle admin replies

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put(update)
    return "OK", 200

# Health check route
@app.route("/health", methods=["GET"])
def health():
    return "Healthy", 200

if __name__ == "__main__":
    # Start Flask server
    app.run(host="0.0.0.0", port=8000)
    
