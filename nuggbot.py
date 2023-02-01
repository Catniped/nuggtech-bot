import discord, typing, time, asyncio, mqtt_client
from discord import *


if __name__ == "__main__":
    class aclient(discord.Client):
        def __init__(self):
            super().__init__(intents=discord.Intents.all())
            self.synced = False
            self.added = False

        async def on_ready(self):
                await self.wait_until_ready()
                if not self.synced:
                    await tree.sync()
                    self.synced = True
                activity = discord.Game(name=":3", type=3)
                await client.change_presence(status=discord.Status.online, activity=activity)
                print(f"Logged in as {self.user}")
                global chan
                chan = client.get_channel(751052412957229138)

    client = aclient()
    tree = app_commands.CommandTree(client)

    @tree.command(name = "startbridge", description = "Starts the cross discord chatbridge.")
    async def self(interaction: discord.Interaction):
        await interaction.response.defer()
        await asyncio.create_subprocess_shell(f"py mqtt_client.py")
        embedVar = discord.Embed(title=f"started", color=0xBD783C)
        await interaction.followup.send(embed=embedVar)

    @client.event
    async def on_message(message: discord.Message):
        await mqtt_client.publish_mqtt(message.content)

    client.run("1")

async def publish_chan(msg: str):
    await chan.send(msg)