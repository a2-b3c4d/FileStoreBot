import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from database.database import *
from config import *

@Client.on_message(filters.private & filters.incoming)
async def forcesub(c, m):
    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
               await m.reply_text("**Oooops! Looks like you've been banned from our channel. Contact an admin to sort it out. 😜**", quote=True)
               return
        except UserNotParticipant:
            buttons = [[InlineKeyboardButton(text='Join Updates Channel 🔖', url=f"https://t.me/{UPDATE_CHANNEL}")]]
            if m.text:
                if (len(m.text.split(' ')) > 1) & ('start' in m.text):
                    chat_id, msg_id = m.text.split(' ')[1].split('_')
                    buttons.append([InlineKeyboardButton('🔄 Refresh', callback_data=f'refresh+{chat_id}+{msg_id}')])
            await m.reply_text(
                f"Hey {m.from_user.mention(style='md')}! Looks like you need to join my updates channel to continue using me 😉\n\n"
                "__Press the button below to join now 👇__",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
            return
        except Exception as e:
            print(e)
            await m.reply_text(f"Something went wrong! Please try again later or contact {owner.mention(style='md')} 😅", quote=True)
            return
    await m.continue_propagation()


@Client.on_callback_query(filters.regex('^refresh'))
async def refresh_cb(c, m):
    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
               try:
                   await m.message.edit("**Uh-oh! You're banned from our updates channel. Contact the admin to resolve it. 😜**")
               except:
                   pass
               return
        except UserNotParticipant:
            await m.answer('You need to join our updates channel first. 😏 Join and then click the refresh button. 🤤', show_alert=True)
            return
        except Exception as e:
            print(e)
            await m.message.edit(f"Something went wrong! Please try again later or contact {owner.mention(style='md')} 😅")
            return

    cmd, chat_id, msg_id = m.data.split("+")
    msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))
    if msg.empty:
        return await m.reply_text(f"🥴 Oops! Looks like your file is missing. Please contact my owner 👉 {owner.mention(style='md')}")

    caption = msg.caption.markdown
    as_uploadername = (await get_data(str(chat_id))).up_name
    if as_uploadername:
        if chat_id.startswith('-100'):  # if file from channel
            channel = await c.get_chat(int(chat_id))
            caption += "\n\n\n**--Uploader Details:--**\n\n"
            caption += f"**📢 Channel Name:** __{channel.title}__\n\n"
            caption += f"**🗣 Username:** @{channel.username}\n\n" if channel.username else ""
            caption += f"**👤 Channel ID:** __{channel.id}__\n\n"
        
        else:  # if file not from channel
            user = await c.get_users(int(chat_id))
            caption += "\n\n\n**--Uploader Details:--**\n\n"
            caption += f"**🍁 Name:** [{user.from_user.first_name}](tg://user?id={user.from_user.id})\n\n"
            caption += f"**🖋 Username:** @{user.username}\n\n" if user.username else ""

    await msg.copy(m.from_user.id, caption=caption)
    await m.message.delete()
