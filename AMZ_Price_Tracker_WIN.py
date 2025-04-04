import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import telegram
from datetime import datetime, timedelta

# Telegram bot setup
TELEGRAM_TOKEN = "InsertYourBotTokenHere"
CHAT_ID = "InsertYourChatIdHere"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Selenium setup
CHROME_DRIVER_PATH = "chromedriver.exe"  # Replace with your ChromeDriver path
options = Options()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,1024")  # Set a virtual screen size
service = Service(CHROME_DRIVER_PATH)

# Funktion zur Extraktion des Preises
def get_price(url):
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Find the price element
        price_element = driver.find_element(By.CSS_SELECTOR, "span.a-declarative span.a-price span.a-offscreen")
        price_element_big = driver.find_element(By.CSS_SELECTOR, "span.a-declarative span.a-price span.a-price-whole")
        price_element_small = driver.find_element(By.CSS_SELECTOR, "span.a-declarative span.a-price span.a-price-fraction")
        if price_element and not price_element_big and not price_element_small:
            price_text = price_element.get_attribute("textContent")
            print(f"Extrahierter Text: {price_text}")  # Debugging: Zeige den extrahierten Text an
            
            # Bereinige den Preistext
            price_text = price_text.replace("\u00a0", "").replace("€", "").strip()
            
            # Umwandlung in Float (Dezimaltrennzeichen: Punkt)
            price = float(price_text.replace(",", "."))
            return price
        elif price_element_big and price_element_small:
            price_text_big = price_element_big.get_attribute("textContent")
            price_text_small = price_element_small.get_attribute("textContent")
            print(f"Extrahierter Text: {price_text_big}.{price_text_small}")  # Debugging: Zeige den extrahierten Text an

            price_text_2 = price_text_big + '.' + price_text_small
            
            return float(price_text_2.replace(",", ""))
        else:
            print("Preis konnte nicht gefunden werden.")
            return None
    except Exception as e:
        print(f"Fehler beim Abrufen des Preises: {e}")
        return None
    finally:
        if driver:
            driver.quit()

# Laden der Links und Zielpreise aus der Datei
def load_links(file_path):
    products = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3:
                url, target_price, produktname = parts
                try:
                    target_price = float(target_price)
                    products.append((url, target_price, produktname))  # Produktname hinzufügen
                except ValueError:
                    print(f"Ungültiger Zielpreis in Zeile: {line}")
    return products

# Hauptfunktion
async def main():
    file_path = "product_links.txt"
    products = load_links(file_path)

    # Dictionary zur Verfolgung der letzten Benachrichtigung für jedes Produkt
    last_notification_time = {}

    while True:
        for url, target_price, produktname in products:
            # Wenn das Produkt kürzlich überprüft wurde, überspringen
            if url in last_notification_time:
                time_since_last_check = datetime.now() - last_notification_time[url]
                # Wenn weniger als 'wait_time' seit der letzten Benachrichtigung vergangen ist, überspringen
                if time_since_last_check < timedelta(minutes=720):  # Beispiel: 30 Minuten warten
                    print(f"Produkt {produktname} wurde kürzlich überprüft. Überspringen...")
                    continue

            print(f"Prüfe {url}...")
            price = get_price(url)
            if price is not None:
                print(f"Aktueller Preis: {price} EUR, Zielpreis: {target_price} EUR\nFuer das Produkt: {produktname}")
                if price <= target_price:
                    message = f"Das Produkt {produktname} unter {url} ist im Angebot! Aktueller Preis: {price} EUR"
                    await bot.send_message(chat_id=CHAT_ID, text=message)  # Asynchron senden
                    print("Benachrichtigung gesendet.")

                    # Zeitpunkt der letzten Benachrichtigung speichern
                    last_notification_time[url] = datetime.now()

            time.sleep(5)  # Wartezeit zwischen den Anfragen, um Überlastung zu vermeiden

        time.sleep(refresh)  # Warte x Sekunden, bevor die Überprüfung erneut startet


if __name__ == "__main__":
    refresh = input(f"Wann soll der Preis ueberprueft werden? Gebe die Anzahl in Minuten ein!\n")
    try:
        refresh = int(refresh)  # Konvertiere die Eingabe in eine Ganzzahl
        refresh = refresh*60
    except ValueError:
        print("Bitte gib eine gültige Zahl ein.")
        exit(1)
    
    asyncio.run(main())  # Starte die asynchrone Hauptfunktion
