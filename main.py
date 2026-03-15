import os
import time
import asyncio
from keep_alive import keep_alive
try:
    import discord
    from discord.ext import tasks
except:
    from setup import install
    install()
    import discord
    from discord.ext import tasks

print("""\
**Voicecord 24/7 - Auto Reconnect Version**
""")
time.sleep(0.5)

client = discord.Client(intents=discord.Intents.default())

Token = os.environ.get("DISCORD_TOKEN")
Id = int(os.environ.get("CHANNEL_ID"))

# Fitur Auto-Reconnect setiap 15 detik
@tasks.loop(seconds=15)
async def maintain_vc():
    voice_channel = client.get_channel(Id)
    if voice_channel:
        is_connected = False
        # Mengecek apakah akun sedang terhubung ke VC yang benar
        for vc in client.voice_clients:
            if vc.channel.id == Id and vc.is_connected():
                is_connected = True
                break
        
        # Jika tidak terhubung, paksa masuk kembali
        if not is_connected:
            print("Terputus dari VC atau belum masuk. Mencoba menyambung...")
            try:
                # Bersihkan sisa koneksi lama (jika ada) sebelum masuk lagi
                for vc in client.voice_clients:
                    if vc.guild == voice_channel.guild:
                        await vc.disconnect()
                        
                await voice_channel.connect()
                print("-> Berhasil masuk ke VC!")
            except Exception as e:
                print(f"-> Gagal menyambung: {e}")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lofi"))
    
    # Menjalankan pengecekan VC otomatis saat bot menyala
    if not maintain_vc.is_running():
        maintain_vc.start()

keep_alive()
client.run(Token, bot=False)
