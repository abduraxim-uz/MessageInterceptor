import os
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient, events


# BASE_DIR = Path(__file__).resolve().parent
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

DESTINATION_CHAT = "me"

MAX_SIZE = 50 * 1024 * 1024

def build_link(event):
    try:
        chat = event.chat
        msg_id = event.message.id

        # public group bo'lsa username bilan
        if chat.username:
            return f"https://t.me/{chat.username}/{msg_id}"

        # private group bo'lsa
        else:
            chat_id = str(chat.id)
            clean_id = chat_id.replace("-100", "")
            return f"https://t.me/c/{clean_id}/{msg_id}"

    except:
        return "link unavailable"


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if not event.is_private:
            return

        sender = await event.get_sender()
        msg = event.message

        text = msg.message or ""
        link = build_link(event)

        caption = (
            f"📩 From: {sender.first_name}\n"
            f"🔗 Message: {link}\n\n"
            f"{text}"
        )
    
        # 📷 PHOTO
        if msg.photo:
            file_path = await event.download_media()
            await client.send_file(DESTINATION_CHAT, file_path, caption=caption)
            os.remove(file_path)

        # 🎞 GIF
        elif msg.gif:
            file_path = await event.download_media()
            await client.send_file(DESTINATION_CHAT, file_path, caption=caption)
            os.remove(file_path)

        # 🎥 VIDEO
        elif msg.video:
            if msg.file and msg.file.size <= MAX_SIZE:
                file_path = await event.download_media()
                await client.send_file(DESTINATION_CHAT, file_path, caption=caption)
                os.remove(file_path)

        else:
            print("Skipped")

    except Exception as e:
        print(f"Error: {e}")


async def main():
    await client.start()
    print("🚀 Userbot running with links...")

    await client.run_until_disconnected()


if __name__ == "__main__":
    client.loop.run_until_complete(main())
