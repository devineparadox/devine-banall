from config import OWNER_ID, API_ID, API_HASH, BOT_TOKEN
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

START_IMG = "https://telegra.ph//file/721a7c1b34195a7a6f727.jpg"

devine = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler for /start command
@devine.on_message(filters.command("start") & filters.private)
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
@devine.on_message(filters.command("banall") & filters.group)
async def ban_all(client, message: Message):
    if message.from_user.id == OWNER_ID:
        chat_id = message.chat.id
        banned_count = 0
        failed_count = 0
        async for member in devine.iter_chat_members(chat_id):
            if member.user.id != OWNER_ID and not member.user.is_bot:
                try:
                    await devine.kick_chat_member(chat_id, member.user.id)
                    user_mention = f"@{member.user.username}" if member.user.username else member.user.first_name
                    await devine.send_message(chat_id, f"{user_mention} has been banned.", reply_to_message_id=message.message_id)
                    banned_count += 1
                except Exception as e:
                    failed_count += 1
                    await message.reply_text(f"Failed to ban {user_mention}: {e}")
        
        if failed_count == 0:
            await message.reply_text("All members have been banned.")
        else:
            await message.reply_text(f"Banned {banned_count} members. {failed_count} members could not be banned.")
    else:
        await message.reply_text("You are not authorized to use this command.")

devine.run()
