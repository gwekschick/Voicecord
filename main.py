import os
import time
import asyncio
from keep_alive import keep_alive

try:
    import discord
except ImportError:
    from setup import install
    install()
    import discord

print("""\
**Voicecord 24/7 - Stable Async Version**
""")
time.sleep(0.5)

client = discord.Client(intents=discord.Intents.default())

Token = os.environ.get("DISCORD_TOKEN")
Id = int(os.environ.get("CHANNEL_ID"))

# Fungsi Loop Mandiri (Lebih stabil dari ext.tasks)
async def maintain_vc():
    await client.wait_until_ready()
    voice_channel = client.get_channel(Id)
    
    if not voice_channel:
        print("ERROR: Channel tidak ditemukan. Cek kembali ID-nya!")
        return

    while not client.is_closed():
        try:
            vc = voice_channel.guild.voice_client
            
            if vc is not None:
                # Jika nyangkut (zombie), paksa putus
                if not vc.is_connected():
                    print("Membersihkan koneksi yang tersangkut...")
                    await vc.disconnect(force=True)
                    await asyncio.sleep(3)
                # Jika nyasar, pindahkan
                elif vc.channel.id != Id:
                    print("Memindahkan akun ke VC target...")
                    await vc.move_to(voice_channel)
            else:
                # Jika belum masuk, coba masuk dengan batas waktu (timeout) aman
                print("Akun belum ada di VC. Mencoba menyambung...")
                await voice_channel.connect(timeout=30.0, reconnect=True)
                print("-> Berhasil masuk ke VC secara stabil!")
                
        except Exception as e:
            print(f"-> Peringatan jaringan/koneksi: {e}")
            
        # Tunggu 15 detik sebelum mengecek ulang (tidak membebani server)
        await asyncio.sleep(15)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lofi"))
    
    # Memulai fungsi loop mandiri ke dalam sistem background
    client.loop.create_task(maintain_vc())

keep_alive()
client.run(Token, bot=False)
