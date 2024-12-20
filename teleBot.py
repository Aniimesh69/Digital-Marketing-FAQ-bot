import cohere
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your Telegram bot token and Cohere API key
BOT_TOKEN = "7645807839:AAGcmAT85BvYY9NKYZq6PiXxTsh5IR0peCk"
COHERE_API_KEY = "Ch42xoUih8Q6rGs8pDuBjrho9owL4c9wSH1G1h6j"

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Cohere Chat Function
def cohere_chat(prompt):
    try:
        response = co.generate(
            model="command-r-plus-08-2024",  # Use the correct model for your use case
            prompt=f"You are an expert in digital marketing. Answer the following question in detail: {prompt}",
            max_tokens=150,  # Maximum length of response
            temperature=0.7,  # Creativity level
            k=0,  # Disable nucleus sampling for deterministic output
            p=0.75,  # Adjust nucleus sampling if needed
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request."

# Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Digital Marketing FAQ bot! Ask me anything about digital marketing."
    )

# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text("Let me think...")

    # Generate response using Cohere chat model
    response = cohere_chat(user_message)

    # Fallback if the response is empty or invalid
    if not response.strip():
        response = "Sorry, I couldn't generate an answer for your question."

    await update.message.reply_text(response)

# Main Function
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
