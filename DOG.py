import discord
import asyncio
token = 'token'
id = 666

class Dog(discord.Client):

    async def on_ready(self):
        print('ready')
        self.voice = None
        self.lock = asyncio.Lock()

    async def on_voice_state_update(self, member, after, before):
        async with self.lock:
            if member.id == id:
                print('[> member changed voice state]')
                if self.voice and not self.voice.is_connected():
                    self.voice = None
                if member.voice:
                    print('>> member in voice')
                    if self.voice and self.voice.is_playing():
                        self.voice.stop()
                    if not self.voice:
                        print('>>> bot connecting to voice')
                        self.voice = await member.voice.channel.connect()
                    elif self.voice.channel.id != member.voice.channel.id:
                        print('>>> bot changing voice')
                        await self.voice.move_to(member.voice.channel)
                        await asyncio.sleep(1)
                    print('>> bot playing audio')
                    self.voice.play(discord.FFmpegPCMAudio('sempl.mp3'))

                else:
                    print('> member disconnected from voice')
                    if self.voice:
                        print('>> disconnecting from voice')
                        if self.voice.is_playing():
                            self.voice.stop()
                        await self.voice.disconnect()
                        self.voice = None
                print("[> END]")
dog = Dog()
dog.run(token, bot=False)
