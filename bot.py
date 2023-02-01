import discord, asyncio, tomllib
from discord import *
import paho.mqtt.client as paho
from paho import mqtt
import asyncio_mqtt as aiomqtt
import paho.mqtt as mqtt

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
servername = config["servername"]


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
tls_params = aiomqtt.TLSParameters(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

async def main():
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
                activity = discord.Game(name=config["status"], type=3)
                await client.change_presence(status=discord.Status.online, activity=activity)
                print(f"Logged in as {self.user}")
                global chan
                chan = client.get_channel(config["chanid"])

    client = aclient()
    tree = app_commands.CommandTree(client)
    
    @client.event
    async def on_message(message: discord.Message):
        if message.channel == chan:
            if message.author.id != config["botid"]:
                async with aiomqtt.Client(hostname=config["hostname"], port=config["port"], username=config["username"], password=config["password"], client_id="", protocol=paho.MQTTv5, tls_params=tls_params) as c:
                    reply = None
                    reply = message.reference 
                    msg = message.content + " "
                    for x in message.attachments:
                        msg += x.url
                    if config["broadcastserver"] is False:
                        if reply is not None:
                            message2 = reply.resolved
                            await c.publish(config["outtopic"], payload=f"{message2.author.name}: {message2.content} -> {message.author.name}: {msg}")
                        else:
                            await c.publish(config["outtopic"], payload=f"{message.author.name}: {msg}")
                    else:
                        if reply is not None:
                            message2 = reply.resolved
                            await c.publish(config["outtopic"], payload=f"[{servername}] {message2.author.name}: {message2.content} -> {message.author.name}: {msg}")
                        else:
                            await c.publish(config["outtopic"], payload=f"[{servername}] {message.author.name}: {msg}")

    async def subscriber():
        async with aiomqtt.Client(hostname=config["hostname"], port=config["port"], username=config["username"], password=config["password"], client_id="", protocol=paho.MQTTv5, tls_params=tls_params) as c:
            async with c.messages() as messages:
                for topic in config["intopics"]:
                    await c.subscribe(topic)
                async for message in messages:
                    msg = str(message.payload.decode("utf-8"))
                    if "@everyone" in msg:
                       continue
                    else:
                        await chan.send(msg)

    await asyncio.gather(asyncio.create_task(subscriber()), client.start(config["bottoken"]))

asyncio.run(main())