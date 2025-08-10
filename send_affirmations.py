import os, random, datetime, json, urllib.request

AFFIRMATIONS_FILE = "affirmations.txt"
LAST_FILE = ".last_affirmation.txt"

def pick_affirmation():
    with open(AFFIRMATIONS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    last = open(LAST_FILE,"r",encoding="utf-8").read().strip() if os.path.exists(LAST_FILE) else None
    choices = [a for a in lines if a != last] or lines
    choice = random.choice(choices)
    open(LAST_FILE,"w",encoding="utf-8").write(choice)
    return choice

def main():
    url = os.environ["DISCORD_WEBHOOK_URL"]
    today = datetime.date.today().strftime("%a %b %d")
    aff = pick_affirmation()
    content = f"🧡 **{today}**\n{aff}\n\nTry a 4–7–8 breath: inhale 4, hold 7, exhale 8."
    payload = json.dumps({"content": content}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type":"application/json"})
    urllib.request.urlopen(req).read()

if __name__ == "__main__":
    main()
