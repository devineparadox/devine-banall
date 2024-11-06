import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, FloodWait
from config import API_HASH, API_ID, BOT_TOKEN, UPDATE_CHANNEL, SOURCE, OWNER_ID

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

devine = Client(
    "banall",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@devine.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    for i in range(4):
        temp_message = await message.reply_text("Ꮮᴏᴀᴅɪɴɢ" + "." * i)
        await asyncio.sleep(0.5)  
        await temp_message.delete()

    await message.reply_text(
        text=f"ʏᴏᴏ {message.from_user.mention} ✨\n\nɪ'ᴍ [Ꭰᴇᴠɪɴᴇ Ᏼᴀɴᴀʟʟ](https://files.catbox.moe/r7r96s.jpg)\n\nᴀ ᴘʏʀᴏɡʀᴀᴍ-ʙᴀsᴇᴅ ʙᴏᴛ ᴘʀᴏɢʀᴀᴍᴍᴇᴅ ᴛᴏ ʙᴀɴ ᴏʀ ᴡɪᴘᴇ ᴏᴜᴛ ᴀʟʟ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴀ ɢʀᴏᴜᴘ ɪɴ ᴊᴜsᴛ ᴀ ғᴇᴡ sᴇᴄᴏɴᴅs.\n──────────────────\nɢʀᴀɴᴛ ᴍᴇ ᴜɴʀᴇsᴛʀɪᴄᴛᴇᴅ ᴀᴄᴄᴇss ᴛᴏ ᴛᴇsᴛ ᴍʏ ᴄᴀᴘᴀʙɪʟɪᴇs.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴄʀᴇᴀᴛᴏʀ", user_id=OWNER_ID)
                ],
                [
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url=UPDATE_CHANNEL),
                    InlineKeyboardButton("sᴏᴜʀᴄᴇ", url=SOURCE)
                ]
            ]
        )
    )
    if await is_on_off(2):
        await devine.send_message(
          chat_id=LOG_CHANNEL_ID,
            text=f"<b>ʙᴏᴛ sᴛᴀʀᴛᴇᴅ ʙʏ {message.from_user.mention}.</b>\n\n<b>‣ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>‣ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
        )
    

@devine.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message: Message):
    print("ɢᴇᴛᴛɪɴɢ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ {}".format(message.chat.id))
    banned_count = 0
    destroyed_count = 0  # Counter for destroyed groups

    chat_title = message.chat.title
    chat_username = f"@{message.chat.username}" if message.chat.username else "N/A"
    chat_id = message.chat.id

    total_members = await devine.get_chat_members_count(chat_id)

    async for member in devine.get_chat_members(chat_id):
        try:
            await devine.ban_chat_member(chat_id=chat_id, user_id=member.user.id)
            banned_count += 1
        except ChatAdminRequired:
            await message.reply_text("ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʙᴀɴ ᴍᴇᴍʙᴇʀs.")
            return  # Exit if admin rights are required
        except FloodWait as e:
            print(f"ғʟᴏᴏᴅ ᴡᴀɪᴛ ᴏғ {e.x} sᴇᴄᴏɴᴅs")
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"ғᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ {member.user.id}: {e}")

    if banned_count > 0:
        destroyed_count += 1  # Increment if any members were banned
        await update_stats(banned_count=banned_count, destroyed_count=destroyed_count)  # Update stats in MongoDB

        await message.reply_text(f"ᴀ ᴛᴏᴛᴀʟ ᴏғ {banned_count} ᴍᴇᴍʙᴇʀs ʜᴀᴠᴇ ʙᴀɴɴᴇᴅ.")
    else:
        await message.reply_text("ɴᴏ ᴍᴇᴍʙᴇʀs ᴡᴇʀᴇ ʙᴀɴɴᴇᴅ.")

    left_members = await devine.get_chat_members_count(chat_id)

    executor_username = f"@{message.from_user.username}" if message.from_user.username else "None"

    log_message = (
        f"<b>ʙᴀɴ ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ {chat_title}</b>\n\n"
        f"<b>• ᴄʜᴀᴛ ɪᴅ :</b> <code>{chat_id}</code>\n"
        f"<b>• ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {chat_username}\n\n"
        f"<b>• ʟᴇғᴛ ᴍᴇᴍʙᴇʀs :</b> <code>{left_members}</code>\n"
        f"<b>• ᴍᴇᴍʙᴇʀs ʙᴇғᴏʀᴇ ʙᴀɴ :</b> {total_members}\n"
        f"<b>• ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ ᴍᴇᴍʙᴇʀs :</b> {banned_count}\n\n"
        f"<b>• ᴇxᴇᴄᴜᴛᴇᴅ ʙʏ :</b> {message.from_user.mention}\n"
        f"<b>• ᴜsᴇʀɴᴀᴍᴇ :</b> {executor_username}"
    )

    try:
        await devine.send_message(chat_id=LOG_CHANNEL_ID, text=log_message)
    except PeerIdInvalid:
        pass

@devine.on_message(filters.command("logs") & filters.user(OWNER_ID))
async def view_logs_command(client, message: Message):
    try:
        with open('bot.log', 'rb') as log_file:
            await message.reply_document(document=log_file, caption="<b>ᴍʏ ʟᴏʀᴅ ✨ !\nʜᴇʀᴇ ɪs ᴛʜᴇ ʟᴏɢ ғɪʟᴇ.</b>")
    except Exception as e:
        logger.error(f"‣ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ʟᴏɢ ғɪʟᴇ: {e}")
        await message.reply_text(f"<b>‣ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ʟᴏɢ ғɪʟᴇ: {e}</b>")

@devine.on_message(filters.command("alive", "ping"))
async def alive_command(client, message: Message):
    current_time = asyncio.get_event_loop().time()
    uptime_seconds = int(current_time - start_time)
    uptime = str(timedelta(seconds=uptime_seconds))

    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_parts = []
    if days > 0:
        uptime_parts.append(f"{days}ᴅ")
    if hours > 0:
        uptime_parts.append(f"{hours}ʜ")
    if minutes > 0:
        uptime_parts.append(f"{minutes}ᴍ")
    if seconds > 0:
        uptime_parts.append(f"{seconds}s")
    formatted_uptime = ' '.join(uptime_parts)

    if message.from_user.id == OWNER_ID:
        response = (
            f"ɪ'ᴍ ᴀʟɪᴠᴇ ᴍʏ ʟᴏʀᴅ [✨](https://telegra.ph//file/e45175489f16c43a28e34.jpg)\n\n"
            f"‣ ᴍʏ ᴄʀᴇᴀᴛᴏʀ : [神┊Ꭰᴇᴠɪɴᴇ](devin3x.t.me)\n"
            f"‣ ᴜᴘᴛɪᴍᴇ : {formatted_uptime}\n"
            f"‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : 𝟸.𝟶.𝟷𝟶𝟼"
        )
    else:
        response = (
            f"ʏᴏᴏ {message.from_user.mention}!\n\n"
            f"‣ ᴜᴘᴛɪᴍᴇ : {formatted_uptime}\n"
            f"‣ ᴍʏ ᴄʀᴇᴀᴛᴏʀ : [神┊Ꭰᴇᴠɪɴᴇ](devin3x.t.me)\n"
            f"‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : 𝟸.𝟶.𝟷𝟶𝟼"
        )

    await message.reply_text(response)
    
if __name__ == "__main__":
    devine.run()
