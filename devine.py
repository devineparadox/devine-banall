from config import OWNER_ID, API_ID, API_HASH, BOT_TOKEN
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

START_IMG = "https://telegra.ph//file/721a7c1b34195a7a6f727.jpg"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler for /start command
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply_photo(
        photo=START_IMG,
        caption="Hello! I am a bot designed to ban all members from a group. "
                "Use /banall to ban all members in a group where I am admin.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Creator", url=f"tg://openmessage?user_id={OWNER_ID}"),
                    InlineKeyboardButton("Updates", url="https://t.me/devine_network")
                ],
                [
                    InlineKeyboardButton("Source", url="https://github.com/devineparadox/Devine-banall"),
                ]
            ]
        )
    )

# Handler for /banall command
@app.on_message(filters.command("banall") & filters.group)
async def ban_all(client, message: Message):
    if message.from_user.id == OWNER_ID:
        chat_id = message.chat.id
        async for member in client.get_chat_members(chat_id):
            if member.user.id != OWNER_ID and not member.user.is_bot:
                try:
                    await client.kick_chat_member(chat_id, member.user.id)
                    user_mention = f"@{member.user.username}" if member.user.username else member.user.first_name
                    await client.send_message(chat_id, f"{user_mention} has been banned.", reply_to_message_id=message.message_id)
                except Exception as e:
                    await message.reply_text(f"Failed to ban {member.user.first_name}: {e}")
        await message.reply_text("Banned all members.")
    else:
        await message.reply_text("You are not authorized to use this command.")

app.run()
