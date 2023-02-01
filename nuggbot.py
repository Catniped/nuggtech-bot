import discord, typing, time, asyncio
from discord import *
import time, nuggbot, asyncio
import paho.mqtt.client as paho
from paho import mqtt
import asyncio_mqtt as aiomqtt
import paho.mqtt as mqtt

hostname = ""
username = ""
password = ""
botid = 
bottoken = ""
chanid = 
outtopic = 
intopic = 

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
                activity = discord.Game(name=":3", type=3)
                await client.change_presence(status=discord.Status.online, activity=activity)
                print(f"Logged in as {self.user}")
                global chan
                chan = client.get_channel(chanid)

    client = aclient()
    tree = app_commands.CommandTree(client)
    
    @client.event
    async def on_message(message: discord.Message):
        if message.channel == chan:
            if message.author.id != botid:
                async with aiomqtt.Client(hostname=hostname, port=8883, username=username, password=password, client_id="", protocol=paho.MQTTv5, tls_params=tls_params) as c:
                    reply = None
                    reply = message.reference
                    if reply is not None:
                        message2 = reply.resolved
                        await c.publish(outtopic, payload=f"{message.author.name}: {message.content} -> {message2.author.name}: {message2.content}")
                    else:
                        await c.publish(outtopic, payload=f"{message.author.name}: {message.content}")

    async def subscriber():
        async with aiomqtt.Client(hostname=hostname, port=8883, username=username, password=password, client_id="", protocol=paho.MQTTv5, tls_params=tls_params) as c:
            async with c.messages() as messages:
                await c.subscribe(intopic)
                async for message in messages:
                    msg = str(message.payload)
                    if msg.startswith("b\'@everyone"):
                       continue
                    else:
                        await chan.send(msg.strip("b\'"))

    await asyncio.gather(asyncio.create_task(subscriber()), client.start(bottoken))

asyncio.run(main())