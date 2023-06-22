import discord
import os
import openai
import time
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

token = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_KEY")

last_usage_time = 0
activated = False

@client.event
async def on_ready():
    print("{0.user} chegou!".format(client))

@client.event
async def on_message(message):
    global last_usage_time, activated
    current_time = time.time()
    if current_time - last_usage_time > 10 * 60:
        activated = False

    if message.content == "Oh espertalhão!":
        activated = True
        await message.channel.send("Diz o que queres oh burro!")
        last_usage_time = current_time
        return

    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel_name = message.channel.name

    print(username + " perguntou " + user_message.lower() + " ao espertalhão!")

    if message.author == client.user:
        return

    if message.channel.name == "espertalhão":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": 'Responde, em Português de Portugal, como que se fosses um comediante a dar roast nas pessoas que perguntam: ' + user_message}],
            max_tokens=3000,
        )

        print(response['choices'][0]['message']['content'])
        await message.channel.send(response['choices'][0]['message']['content'])
        last_usage_time = current_time

client.run(token)
