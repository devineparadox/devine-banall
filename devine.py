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

@devine.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message: Message):
    print("ɢᴇᴛᴛɪɴɢ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ {}".format(message.chat.id))
    banned_count = 0

    async for member in devine.get_chat_members(message.chat.id):
        try:
            await devine.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
            banned_count += 1
            print("ʙᴀɴɴᴇᴅ {} ғʀᴏᴍ {}".format(member.user.id, message.chat.id))
        except ChatAdminRequired:
            print(f"ʙᴏᴛ ᴅᴏᴇs ɴᴏᴛ ʜᴀᴠᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ {message.chat.id}")
            await message.reply_text("<b>‣ ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʙᴀɴ ᴍᴇᴍʙᴇʀs.</b>")
            break
        except FloodWait as e:
            print(f"ғʟᴏᴏᴅ ᴡᴀɪᴛ ᴏғ {e.x} sᴇᴄᴏɴᴅs")
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"ғᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ {member.user.id}: {e}")

    print(f"ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇᴅ, ᴛᴏᴛᴀʟ {banned_count} ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.")
    await message.reply_text(f"<b>‣ ᴛᴏᴛᴀʟ {banned_count} ᴍᴇᴍʙᴇʀs ʙᴀɴɴᴇᴅ.</b>")

if __name__ == "__main__":
    devine.run()
