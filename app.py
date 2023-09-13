from pyrogram import Client, filters, enums
import requests
import sqlite3
import os

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
api_url = os.getenv("API_URL")

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

conn = sqlite3.connect('settings.db')
c = conn.cursor()

# Create the settings table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        chat_id INTEGER PRIMARY KEY,
        blur_images BOOLEAN
    )
''')
conn.commit()

def send_image(file_path, api_url):
    with open(file_path, 'rb') as r:
        image = r.read()
    r.close()
    req = requests.post(api_url, image).json()
    if req['code'] != 200:
        return 'Error:', req['msg']
    else:
        reqData = req['data']
        if 'Hentai' in reqData and reqData['Hentai'] > 30:
            return 'pron'
        elif 'Porn' in reqData and reqData['Porn'] > 30:
            return 'pron'
        else:
            return None

@app.on_message(filters.command("toggle_spoiler"))
async def toggle_spoiler(client, message):
    admins = []
    async for m in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(m.user.id)
    
    if message.from_user.id not in admins:
        return

    c.execute('SELECT blur_images FROM settings WHERE chat_id = ?', (message.chat.id,))
    row = c.fetchone()
    if row is None:
        blur_images = True
        c.execute('INSERT INTO settings VALUES (?, ?)', (message.chat.id, blur_images))
    else:
        blur_images = not row[0]
        c.execute('UPDATE settings SET blur_images = ? WHERE chat_id = ?', (blur_images, message.chat.id))
    conn.commit()

    await message.reply(f"打码模式， {'开启' if blur_images else '关闭'}.")

@app.on_message(filters.photo)
async def download_photo(client, message):
    file_path = await message.download("downloads/")
    response = send_image(file_path, api_url)

    if response == "pron":    
        await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message.id,
            )
        
        c.execute('SELECT blur_images FROM settings WHERE chat_id = ?', (message.chat.id,))
        row = c.fetchone()
        blur_images = row[0] if row is not None else False

        try:
            if blur_images:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=file_path,
                    caption="内容可能是NSFW",
                    has_spoiler=True,
                )
        except Exception as e:
            await message.reply(f"Error: {e}")

app.run()