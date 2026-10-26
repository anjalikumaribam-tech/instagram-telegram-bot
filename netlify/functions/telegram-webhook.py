import json
import os
import urllib.request
import yt_dlp

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

def tg(method, payload):
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode())

def handler(event, context):
    if event.get("httpMethod") != "POST":
        return {"statusCode": 200, "body": "Telegram webhook is running."}
    chat_id = None
    try:
        update = json.loads(event.get("body") or "{}")
        msg = update.get("message") or {}
        chat_id = (msg.get("chat") or {}).get("id")
        text = (msg.get("text") or "").strip()
        if not chat_id or not text:
            return {"statusCode": 200, "body": "OK"}
        if text.startswith("/start"):
            tg("sendMessage", {"chat_id": chat_id, "text": "Namaste! Public Instagram Reel/video ka link bhejiye."})
            return {"statusCode": 200, "body": "OK"}
        if "instagram.com/" not in text.lower():
            tg("sendMessage", {"chat_id": chat_id, "text": "Instagram Reel ya post ka link bhejiye."})
            return {"statusCode": 200, "body": "OK"}

        tg("sendMessage", {"chat_id": chat_id, "text": "Link check kar raha hoon..."})
        opts = {"quiet": True, "no_warnings": True, "skip_download": True, "noplaylist": True, "socket_timeout": 15}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(text, download=False)
        media_url = info.get("url")
        if not media_url:
            raise RuntimeError("No media URL returned")
        # Telegram fetches the media URL; Netlify does not store the video.
        tg("sendVideo", {"chat_id": chat_id, "video": media_url, "caption": (info.get("title") or "Instagram video")[:900]})
    except Exception as exc:
        print("DOWNLOAD ERROR:", repr(exc))
        try:
            if chat_id:
                tg("sendMessage", {"chat_id": chat_id, "text": "Download nahi hua. Instagram restrictions ya temporary media URL ki wajah se link fail ho sakta hai."})
        except Exception:
            pass
    return {"statusCode": 200, "body": "OK"}
