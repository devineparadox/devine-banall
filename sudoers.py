from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID, API_ID, API_HASH, BOT_TOKEN

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
SUDOERS = set()

async def extract_user(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    else:
        user_id = message.command[1]
        user = await app.get_users(user_id)
        return user

@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
async def useradd(client, message: Message):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("Please reply to a user's message or provide a user ID.")
    
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(f"{user.mention} is already a sudo user.")
    
    SUDOERS.add(user.id)
    await message.reply_text(f"{user.mention} has been added as a sudo user.")

@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
async def userdel(client, message: Message):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("Please reply to a user's message or provide a user ID.")
    
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(f"{user.mention} is not a sudo user.")
    
    SUDOERS.remove(user.id)
    await message.reply_text(f"{user.mention} has been removed from sudo users.")

@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~filters.user(BANNED_USERS))
async def sudoers_list(client, message: Message):
    if not SUDOERS:
        return await message.reply_text("No sudo users found.")
    
    text = "Sudo Users:\n"
    for idx, user_id in enumerate(SUDOERS, start=1):
        user = await app.get_users(user_id)
        user_mention = user.mention if user.mention else user.first_name
        text += f"{idx}. {user_mention}\n"
    
    await message.reply_text(text)

app.run()
