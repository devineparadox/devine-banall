from os import getenv
import logging
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
from config import API_HASH, API_ID, BOT_TOKEN, OWNER_ID, START_IMG, UPDATE_URL, SOURCE_URL, MUSIC_BOT_URL

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
        photo=START_IMG,
        caption=,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴄʀᴇᴀᴛᴏʀ", url=f"tg://openmessage?user_id={OWNER_ID}"),
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url=UPDATE_CHANNEL)
                ],
                [
                    InlineKeyboardButton("ᴍᴜsɪᴄ", url=MUSIC_BOT),
                    InlineKeyboardButton("sᴏᴜʀᴄᴇ", url=SOURCE)
                ]
            ]
        )
    )

@devine.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message: Message):
    print("ɢᴇᴛᴛɪɴɢ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ {}".format(message.chat.id))
    banned_count = 0
    
    async for member in devine.get_chat_members(message.chat.id):
        try:
            await devine.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
            banned_count += 1
            print("ʙᴀɴɴᴇᴅ {} ғʀᴏᴍ {}".format(member.user.id, message.chat.id))
            await message.reply_text(f"<b>‣ {member.user.mention} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.</b>")
        except Exception as e:
            print("ғᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ {} ғʀᴏᴍ {}".format(member.user.id, e))

    print(f"ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇᴅ, ᴛᴏᴛᴀʟ {banned_count} ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.")
    await message.reply_text(f"<b>‣ ᴛᴏᴛᴀʟ {banned_count} ᴍᴇᴍʙᴇʀs ʙᴀɴɴᴇᴅ.</b>")

# start bot client
devine.start()
print("ᴅᴇᴠɪɴᴇ ʙᴀɴᴀʟʟ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
idle()
