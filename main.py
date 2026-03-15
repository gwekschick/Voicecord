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
**Voicecord 24/7 - Anti-Zombie Connection Version**
""")
time.sleep(0.5)

client = discord.Client(intents=discord.Intents.default())

Token = os.environ.get("DISCORD_TOKEN")
Id = int(os.environ.get("CHANNEL_ID"))

@tasks.loop(seconds=15)
async def maintain_vc():
    voice_channel = client.get_channel(Id)
    if voice_channel:
        vc = voice_channel.guild.voice_client
        
        if vc is not None:
            # Pengecekan denyut nadi: Apakah benar-benar masih terhubung ke server suara Discord?
            if not vc.is_connected():
                print("Koneksi 'zombie' terdeteksi (tersangkut). Membersihkan sisa koneksi...")
                try:
                    await vc.disconnect()
                except:
                    pass
                await asyncio.sleep(3) # Jeda agar Discord menghapus sesi lama
            else:
                # Jika benar-benar aktif tapi nyasar ke channel lain
                if vc.channel.id != Id:
                    await vc.move_to(voice_channel)
                    print(f"-> Memindahkan akun kembali ke VC target...")
                return # Sudah aman di dalam VC, keluar dari fungsi pengecekan
            
        print("Akun belum ada di VC. Mencoba menyambung...")
        try:
            await voice_channel.connect()
            print("-> Berhasil masuk ke VC secara stabil!")
        except Exception as e:
            print(f"-> Gagal menyambung: {e}")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lofi"))
    
    if not maintain_vc.is_running():
        maintain_vc.start()

keep_alive()
client.run(Token, bot=False)
