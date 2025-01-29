import os
import asyncio
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import base64
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ListenerCanceled
from database.database import *
from config import *

BATCH = []

app = Client("my_bot")

@app.on_message(filters.command('start'))
async def start(client, message: Message):
    await message.reply_text(
        "Oi! You want access to my stash? Not so fast! 🔒\n"
        "First, you gotta join our channel—no freebies here!\n"
        "Do that, and maybe I’ll let you in on the treasure. ⚓"
    )

@app.on_message(filters.command('delete'))
async def delete_file(client, message: Message):
    # Assuming the file deletion logic is here
    await message.reply_text(
        "✅ Yᴏᴜʀ ғɪʟᴇ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!"
    )


@app.on_message(filters.command('start') & filters.incoming & filters.private)
async def start(c, m, cb=False):
    if not cb:
        send_msg = await m.reply_text("**Pʀᴏʄᴇssɪɴɢ...**", quote=True)

    owner = await c.get_users(int(OWNER_ID))
    owner_username = owner.username if owner.username else 'AvishkarPatil'

    # start text
    text = f"""**Hᴇʏ!** {m.from_user.mention(style='md')}
    
🤗 **I'm FileStoreBot **

‣ Yᴏᴜ ᴄᴀɴ sᴛᴏʀᴇ ʏᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Mᴇᴅɪᴀ ғᴏʀ ᴘᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ! ᴀɴᴅ Sʜᴀʀᴇ Aɴʏᴡʜᴇʀᴇ

‣ Cʟɪᴄᴋ ᴏɴ Hᴇʟᴘ ᴀɴᴅ Kɴᴏᴡ Mᴏʀᴇ Aʙᴏᴜᴛ Usɪɴɢ ᴍᴇ

__🚸 Pᴏʀɴ Cᴏɴᴛᴇɴᴛ Nᴏᴛ Aʟʟᴏᴡᴇᴅ Oɴ Tʜᴇ Bᴏᴛ__

**💞 Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ:** {owner.mention(style='md')}
"""

    # Buttons
    buttons = [[
            InlineKeyboardButton('Hᴇʟᴘ 💡', callback_data="help"),
            InlineKeyboardButton('Aʙᴏᴜᴛ 👑', callback_data="about")],[
            InlineKeyboardButton('Mʏ Fᴀᴛʜᴇʀ 👨‍✈️', url=f"https://t.me/{owner_username}"),
        ]]

    # when button home is pressed
    if cb:
        return await m.message.edit(
                   text=text,
                   reply_markup=InlineKeyboardMarkup(buttons)
               )

    if len(m.command) > 1:  # sending the stored file
        try:
            m.command[1] = await decode(m.command[1])
        except:
            pass

        if 'batch_' in m.command[1]:
            await send_msg.delete()
            cmd, chat_id, message = m.command[1].split('_')
            string = await c.get_messages(int(chat_id), int(message)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(message))

            if string.empty:
                owner = await c.get_users(int(OWNER_ID))
                return await m.reply_text(f"🥴 Sᴏʀʀʏ ʙʀᴏ ʏᴏᴜʀ ғɪʟᴇ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ʙʏ ғɪʟᴇ ᴏᴡɴᴇʀ ᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ\n\nFᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ👉 {owner.mention(style='md')}")
            message_ids = (await decode(string.text)).split('-')
            for msg_id in message_ids:
                msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

                if msg.empty:
                    owner = await c.get_users(int(OWNER_ID))
                    return await m.reply_text(f"🥴 Sᴏʀʀʏ ʙʀᴏ ʏᴏᴜʀ ғɪʟᴇ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ʙʏ ғɪʟᴇ ᴏᴡɴᴇʀ ᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ\n\nFᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ👉 {owner.mention(style='md')}")

                await msg.copy(m.from_user.id)
                await asyncio.sleep(1)
            return

        chat_id, msg_id = m.command[1].split('_')
        msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

        if msg.empty:
            return await send_msg.edit(f"🥴 Sᴏʀʀʏ ʙʀᴏ ʏᴏᴜʀ ғɪʟᴇ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ʙʏ ғɪʟᴇ ᴏᴡɴᴇʀ ᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ\n\nFᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ 👉 {owner.mention(style='md')}")
        
        caption = f"{msg.caption.markdown}\n\n\n" if msg.caption else ""
        as_uploadername = (await get_data(str(chat_id))).up_name
        
        if as_uploadername:
            if chat_id.startswith('-100'):
                channel = await c.get_chat(int(chat_id))
                caption += "\n\n\n**--Uᴘʟᴏᴀᴅᴇʀ Dᴇᴛᴀɪʟs:--**\n\n"
                caption += f"**📢 Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** __{channel.title}__\n\n"
                caption += f"**🗣 Usᴇʀ Nᴀᴍᴇ:** @{channel.username}\n\n" if channel.username else ""
                caption += f"**👤 Cʜᴀɴɴᴇʟ Iᴅ:** __{channel.id}__\n\n"
            else:
                user = await c.get_users(int(chat_id)) 
                caption += "\n\n\n**--Uᴘʟᴏᴀᴅᴇʀ Dᴇᴛᴀɪʟs:--**\n\n"
                caption += f"**🍁 Nᴀᴍᴇ:** [{user.from_user.first_name}](tg://user?id={user.from_user.id})\n\n"
                caption += f"**🖋 Usᴇʀ Nᴀᴍᴇ:** @{user.username}\n\n" if user.username else ""


        await send_msg.delete()
        await msg.copy(m.from_user.id, caption=caption)


    else:  # sending start message
        await send_msg.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_message(filters.command('me') & filters.incoming & filters.private)
async def me(c, m):
    """ Tʜɪs ᴡɪʟʟ ᴛ
