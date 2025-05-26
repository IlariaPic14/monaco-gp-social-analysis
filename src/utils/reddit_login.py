import praw
import webbrowser
from urllib.parse import urlparse, parse_qs



CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
USER_AGENT = "your-user-agent"
REDIRECT_URI = "url"



reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    user_agent=USER_AGENT
)

# STEP 1: Autenticazione via browser
state = "monaco"
url = reddit.auth.url(["read"], state=state, duration="permanent")
print(" Apri il browser per l'autenticazione...")
webbrowser.open(url)

# STEP 2: Inserisci il codice ricevuto nel redirect URL
code = input("Inserisci il codice 'code' dell'URL di callback: ").strip()
refresh_token = reddit.auth.authorize(code)

# STEP 3: Salvataggio
print("\n Refresh Token ricevuto!")
print(refresh_token)
