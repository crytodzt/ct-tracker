import discord
from discord.ext import tasks
import tweepy
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TWITTER_ACCOUNTS = os.getenv("TWITTER_ACCOUNTS").split(",")

# Configuração do bot Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Configuração do cliente Twitter
client_twitter = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# Função para buscar tweets recentes
def fetch_tweets():
    query = f"from:{' OR from:'.join(TWITTER_ACCOUNTS)} solana OR contrato"
    tweets = client_twitter.search_recent_tweets(query=query, max_results=5)
    return tweets.data if tweets.data else []

# Tarefa para monitorar tweets periodicamente
@tasks.loop(minutes=1)
async def check_tweets():
    channel = client.get_channel(CHANNEL_ID)
    tweets = fetch_tweets()
    for tweet in tweets:
        await channel.send(f"Novo tweet de @{tweet.author_id}: {tweet.text}")

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    check_tweets.start()

# Rodar o bot
client.run(DISCORD_TOKEN)
