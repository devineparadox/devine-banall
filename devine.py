from os import getenv
import logging
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
from config import API_HASH, API_ID, BOT_TOKEN, OWNER_ID

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# pyrogram client
devine = Client(
    "banall",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@devine.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply_photo(
        photo="https://telegra.ph/file/fff2ee6f504bc061cb7d3.jpg",
        caption="ʜᴇʏ, ᴛʜɪs ɪs ᴀ sɪᴍᴘʟᴇ ʙᴀɴ ᴀʟʟ ʙᴏᴛ ᴡʜɪᴄʜ ɪs ʙᴀsᴇᴅ ᴏɴ ᴘʏʀᴏɢʀᴀᴍ ʟɪʙᴇʀᴀʀʏ ᴛᴏ ʙᴀɴ ᴏʀ ᴅᴇsᴛʀᴏʏ ᴀʟʟ ᴛʜᴇ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴀ ɢʀᴏᴜᴘ ᴡɪᴛʜɪɴ ᴀ ғᴇᴡ sᴇᴄᴏɴᴅs!\n\nᴛʏᴘᴇ /ʙᴀɴᴀʟʟ ᴛᴏ ꜱᴇᴇ ᴍᴀɢɪᴄ ɪɴ ɢʀᴏᴜᴘ.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_ID}")
                ],
                [
                    InlineKeyboardButton("Update Channel", url="https://t.me/devine_network"),
                    InlineKeyboardButton("Source Code", url="https://github.com/devineparadox/Devine-banall")
                ]
            ]
        )
    )

@devine.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message: Message):
    print("getting members from {}".format(message.chat.id))
    banned_count = 0
    
    async for member in devine.get_chat_members(message.chat.id):
        try:
            await devine.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
            banned_count += 1
            print("banned {} from {}".format(member.user.id, message.chat.id))
            await message.reply_text(f"{member.user.mention} has been banned.")
        except Exception as e:
            print("failed to ban {} from {}".format(member.user.id, e))

    print(f"process completed. Total {banned_count} members banned.")
    await message.reply_text(f"Total {banned_count} members banned.")

# start bot client
devine.start()
print("Devine ban all started successfully")
idle()
