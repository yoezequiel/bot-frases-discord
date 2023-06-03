import discord
import aiohttp
import schedule
import asyncio
from discord.ext import commands
from deep_translator import GoogleTranslator

# Configura el cliente del bot de Discord con las intenciones adecuadas
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)


# Función para obtener una frase de ZenQuotes
async def get_inspiring_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as response:
            data = await response.json()
            quote = data[0]['q'] + " - " + data[0]['a']
            return quote


# Función para traducir la frase al español
async def translate_to_spanish(text):
    translated_text = GoogleTranslator(source='auto',
                                    target='es').translate(text)
    return translated_text


# Función para enviar una frase inspiradora
async def send_inspiring_quote(channel):
    quote = await get_inspiring_quote()
    translated_quote = await translate_to_spanish(quote)
    await channel.send(translated_quote)


# Comando !frase para solicitar una frase inspiradora
@bot.command()
async def frase(ctx):
    quote = await get_inspiring_quote()
    translated_quote = await translate_to_spanish(quote)
    await ctx.send(translated_quote)


# Función para programar el envío de la frase inspiradora todos los días a una hora específica
def schedule_quote():
    asyncio.create_task(send_inspiring_quote(bot.get_channel(CHANNEL_ID)))
    schedule.every().day.at("08:00").do(schedule_quote)


# Evento cuando el bot se conecta al servidor de Discord
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")
    schedule_quote()

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


# Configura el token de tu bot de Discord y el ID del canal donde se enviarán las frases
TOKEN = "0000000000000"
# Reemplaza con el ID del canal donde deseas enviar las frases inspiradoras
CHANNEL_ID = 00000000000

# Inicia el bot
bot.run(TOKEN)
