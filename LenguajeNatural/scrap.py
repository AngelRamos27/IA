import snscrape.modules.twitter as sntwitter
import ssl

# Deshabilitar verificación SSL (no recomendado para producción)
ssl._create_default_https_context = ssl._create_unverified_context

# Define la consulta
query = "ley del poder judicial"

tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > 10:
        break
    tweets.append((tweet.user.username, tweet.content))

for user, content in tweets:
    print(f"Usuario: {user}")
    print(f"Texto: {content}\n")
