from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your own environment variables or configuration
BOT_TOKEN = "7290224551:AAGROA8Jv8amXKfOzJUxwsXGfAGXYVt_z1Q"
API_ID = 29230755  # Replace with your API ID
API_HASH = "ab41c7247a91680d2d0dc705ad7158da"
OWNER_ID = 6440363814  # Replace with your owner ID

# Initialize Pyrogram client
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start image URL
START_IMG = "https://telegra.ph/file/fff2ee6f504bc061cb7d3.jpg"

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

# Handler for /banall command in groups
@app.on_message(filters.command("banall") & filters.group & filters.me)
async def banall_command(client, message: Message):
    chat_id = message.chat.id
    members = await client.get_chat_members(chat_id)
    
    # Iterate through members and ban each one (except self and admins)
    for member in members:
        user_id = member.user.id
        if not member.user.is_bot and user_id != client.me.id:
            try:
                await client.kick_chat_member(chat_id, user_id)
            except Exception as e:
                print(f"Failed to ban user {user_id}: {str(e)}")
    
    await message.reply_text("All members banned from the group except admins.")

# Handler for /banallbot command in groups
@app.on_message(filters.command("banallbot") & filters.group & filters.me)
async def banallbot_command(client, message: Message):
    chat_id = message.chat.id
    members = await client.get_chat_members(chat_id)
    
    # Iterate through members and ban each bot (except self)
    for member in members:
        user_id = member.user.id
        if member.user.is_bot and user_id != client.me.id:
            try:
                await client.kick_chat_member(chat_id, user_id)
            except Exception as e:
                print(f"Failed to ban bot {user_id}: {str(e)}")
    
    await message.reply_text("All bots banned from the group.")

# Start the bot
async def main():
    await app.start()
    print(f"{(await app.get_me()).username} has started!")
    await app.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
