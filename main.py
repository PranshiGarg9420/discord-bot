import discord
import google.generativeai as genai
import os

# Load API keys from Replit Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Ensure API Keys Exist
if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY is missing!")
    exit()
if not DISCORD_BOT_TOKEN:
    print("❌ ERROR: DISCORD_BOT_TOKEN is missing!")
    exit()

# ✅ Correct way to configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ✅ FIXED: Use latest method to initialize the model
model = genai.models.get("gemini-pro")  # ✅ Corrected

# Set up Discord bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!chat"):
        user_input = message.content[6:].strip()  # Extract user message
        if not user_input:
            await message.channel.send("⚠️ Please provide a message to chat with AI.")
            return

        try:
            response = model.generate_content(user_input)  # Get AI response
            await message.channel.send(response.text)  # Send AI response
        except Exception as e:
            await message.channel.send("❌ Error generating response. Try again later.")
            print(f"Error: {e}")

# Run the bot
client.run(DISCORD_BOT_TOKEN)
