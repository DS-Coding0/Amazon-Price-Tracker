# Amazon Price Tracker
 Price Tracker for Amazon, written in Python



#INFORMATIONEN

Um das Programm unter Windows laufen zu lassen, benoetigt man einen installieren Google Chrome Browser!
Falls das Programm aufgrund der chromedriver.exe nicht startet, ueberprueft bitte die Version eures Chrome Browsers und besorgt euch die korrekte chromedriver.exe.



#VORBEREITUNG

In der Datei 'product_links.txt', koennt ihr eure Produkte die getrackt werden sollen einfuegen, dafuer bitte die Datei oeffnen.
Als erstes steht der Produktlink dort, diesen erhaltet ihr wenn ihr bei dem jeweiligen Amazon Produkt auf Teilen geht und Link kopieren.
Anschliessend muss ein ',' gesetzt werden und gebt dann euren Preis an, ab welchen ihr Benachrichtigt werden moechtet.
Anschliessend noch ein ',' und gibt den Produkttitel ein der euch bei einem Angebot mitgeteilt werden soll.

Oeffnet die .py-Datei mit Notepad++ oder einer IDE eurer Wahl wie zb Visual Studio Code.
Ihr benoetigt einen Telegram Bot fuer den Preistracker, Anleitungen dazu gibt es genuegend im Internet, ansonsten schreibt dem BotFather eine Nachricht per Telegram, alles weitere sollte selbsterklaerend sein.
Der BotFather gibt euch euren Token fuer den erstellten Bot, dieser muss in 'InsertYourBotTokenHere' eingefuegt werden.
Erstellt eine Gruppe und ladet den Bot dort ein.
Ihr benoetigt nun die ChatId aus der Gruppe, dieser erhaltet ihr wenn ihr euch per 'web.telegram.org' einloggt und eure Gruppe aufruft, in der Adresszeile findet ihr nun '#-xxxxxxxxxx',
kopiert das Minus und die Zahlen welche nach '#' kommen und fuegt diese bei 'InsertYourChatIdHere' ein.

Starte eine CMD in dem Ordner wo du diese .rar entpackst hast und fuege folgende ein 'pip install -r module.txt'



#NUTZUNG

Um das Programm zu starten bitte per CMD 'python AMZ_Price_Tracker.py' eingeben.
Das Programm fragt euch, alle wie viele Minuten der Preis ueberprueft werden soll, gebt dort bitte die Zeit in Minuten ein.
Im Anschluss prueft das Programm wie in der Textdatei und beim Start angegeben die Produkte und benachrichtigt euch in der Telegram Gruppe, wenn der Preis den von euch angegeben Preis erreicht.