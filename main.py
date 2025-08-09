from pyrogram import Client, filters
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_usernames = [u.strip() for u in os.getenv("BOT_USERNAMES").split(",")]
target_channel = os.getenv("TARGET_CHANNEL_ID")  # Can be ID (int) or username (str)

app = Client("media_forwarder", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(bot_usernames) & filters.media)
async def forward_media(client, message):
    try:
        await message.copy(target_channel)
        print(f"✅ Forwarded media from {message.chat.username} (ID: {message.id})")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    async with app:
        # Verify channel access
        try:
            chat = await app.get_chat(target_channel)
            print(f"🔗 Connected to: {chat.title} (ID: {chat.id})")
        except Exception as e:
            print(f"🚫 Failed to access channel: {e}")
            return

        print("👂 Listening for bot messages...")
        await app.run()

if __name__ == "__main__":
    app.run()