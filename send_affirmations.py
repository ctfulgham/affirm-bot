import os, random, datetime, json, urllib.request, sys, pathlib

AFFIRMATIONS_FILE = "affirmations.txt"
LAST_FILE = ".last_affirmation.txt"

def log(msg): print(f"[affirm-bot] {msg}")

def load_affirmations():
    path = pathlib.Path(AFFIRMATIONS_FILE)
    if path.exists():
        log(f"Found {AFFIRMATIONS_FILE}")
        with path.open("r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        if lines:
            return lines
        log("affirmations.txt is empty; using fallback list.")
    else:
        log(f"{AFFIRMATIONS_FILE} not found; using fallback list.")
    # fallback: short built-in list
    return [
        "Done is kinder than perfect.",
        "Not every thought needs a counter-argument.",
        "A five-minute attempt beats a perfect plan.",
        "I can tolerate an open loop.",
        "Small progress today is enough.",
    ]

def pick_affirmation(lines):
    last = None
    if os.path.exists(LAST_FILE):
        try:
            last = open(LAST_FILE,"r",encoding="utf-8").read().strip() or None
            log(f"Last affirmation: {last!r}")
        except Exception as e:
            log(f"Could not read {LAST_FILE}: {e}")
    choices = [a for a in lines if a != last] or lines
    choice = random.choice(choices)
    try:
        open(LAST_FILE,"w",encoding="utf-8").write(choice)
        log(f"Wrote {LAST_FILE}")
    except Exception as e:
        log(f"Could not write {LAST_FILE}: {e}")
    return choice

def send_discord(webhook_url, content):
    payload = json.dumps({"content": content}).encode()
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req) as r:
        body = r.read().decode()
        log(f"Discord response: {body[:200]}...")

def main():
    log(f"Working directory: {os.getcwd()}")
    log(f"Repo contents: {os.listdir('.')}")
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        log("ERROR: DISCORD_WEBHOOK_URL secret is missing.")
        sys.exit(2)

    lines = load_affirmations()
    aff = pick_affirmation(lines)
    today = datetime.date.today().strftime("%a %b %d")
    msg = f"🧡 **{today}**\n{aff}\n\nTry a 4–7–8 breath: inhale 4, hold 7, exhale 8."

    send_discord(webhook_url, msg)
    log("Sent successfully.")

if __name__ == "__main__":
    main()
