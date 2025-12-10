import threading
import time
from datetime import datetime, timedelta
import os
import re
import requests
import speech_recognition as sr
import pyttsx3

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or "<YOUR_OPENWEATHER_API_KEY>"
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY") or "<YOUR_NEWSAPI_KEY>"
ASR_LANGUAGE = "en-US"

tts = pyttsx3.init()
tts.setProperty("rate", 150)
r = sr.Recognizer()

def speak(text):
    tts.say(text)
    tts.runAndWait()

def listen_once(timeout=5, phrase_time_limit=6):
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                return None
    except OSError:
        return None
    try:
        return r.recognize_google(audio, language=ASR_LANGUAGE)
    except:
        return None

def set_reminder_minutes(minutes: int, message: str):
    def job():
        speak(f"Reminder: {message}")
        print(f"[REMINDER] {message}")
    t = threading.Timer(minutes * 60, job)
    t.daemon = True
    t.start()
    return datetime.now() + timedelta(minutes=minutes)

def get_weather(city: str):
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY.startswith("<"):
        return "Weather API key not set."
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        rreq = requests.get(url, params=params, timeout=8)
        rreq.raise_for_status()
        d = rreq.json()
        name = d.get("name", city)
        w = d.get("weather", [{}])[0].get("description", "")
        temp = d.get("main", {}).get("temp")
        feels = d.get("main", {}).get("feels_like")
        return f"Weather in {name}: {w}. Temperature {temp}°C, feels like {feels}°C."
    except:
        return "Couldn't fetch weather."

def get_top_news(country: str = "us", max_articles: int = 5):
    if not NEWSAPI_KEY or NEWSAPI_KEY.startswith("<"):
        return ["News API key not set."]
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {"apiKey": NEWSAPI_KEY, "country": country, "pageSize": max_articles}
        rreq = requests.get(url, params=params, timeout=8)
        rreq.raise_for_status()
        data = rreq.json()
        arts = data.get("articles", [])
        headlines = []
        for a in arts[:max_articles]:
            title = a.get("title")
            src = a.get("source", {}).get("name")
            headlines.append(f"{title} — {src}")
        return headlines if headlines else ["No headlines found."]
    except:
        return ["Couldn't fetch news."]

def handle(text: str):
    if not text:
        return True
    l = text.lower()
    print("You said:", l)
    if any(w in l for w in ("stop", "quit", "exit", "goodbye", "shutdown")):
        speak("Goodbye.")
        return False
    if "hello" in l or l.strip() in ("hi", "hey"):
        speak("Hello, how can I help?")
        return True
    if "time" in l:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True
    m = re.search(r"remind me in (\d+)\s*minute", l)
    if m:
        mins = int(m.group(1))
        parts = l.split("to", 1)
        msg = parts[1].strip() if len(parts) > 1 else "your reminder"
        when = set_reminder_minutes(mins, msg)
        speak(f"Okay, I'll remind you in {mins} minutes.")
        print(f"Scheduled reminder at {when} -> {msg}")
        return True
    if "weather" in l:
        mcity = re.search(r"in\s+([a-zA-Z ]+)", l)
        city = mcity.group(1).strip() if mcity else None
        if not city:
            speak("Which city?")
            resp = listen_once()
            if not resp:
                speak("No city heard.")
                return True
            city = resp
        summary = get_weather(city)
        speak(summary)
        print(summary)
        return True
    if "news" in l or "headlines" in l:
        speak("Fetching top headlines.")
        headlines = get_top_news(country="us", max_articles=5)
        for idx, h in enumerate(headlines, start=1):
            speak(f"Headline {idx}: {h}")
            time.sleep(0.6)
        return True
    speak("Sorry, I didn't get that.")
    return True

def main():
    speak("Hi, I am ready.")
    running = True
    while running:
        try:
            text = listen_once()
            running = handle(text)
        except Exception as e:
            print("Error:", e)
            speak("There was an error. Continuing.")
            time.sleep(1)
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye")