# MyFreeBot
Ein Python Skript um Prozesse in <a href="https://www.myfreefarm.de" target="_blank">Myfreefarm</a> zu automatisieren.
## Installation
### Linux
##### 1. Benötige Software installieren  
```
sudo apt-get install screen git nano python3 python3-pip firefox-esr
pip3 install selenium
```
##### 2. Lade den benötigten Driver runter
GeckoDriver wenn du Firefox benutzt:
```
https://github.com/mozilla/geckodriver/releases
```
ChromeDriver wenn du Chrome benutzt:
```
https://sites.google.com/a/chromium.org/chromedriver/downloads
```
##### 3. Lade dieses Repository
```
git clone https://github.com/TheRealHypR/myfreefarm-bot.git
```
##### 4. Die Datei `accounts_example_v1.X.json` zu `accounts.json` umbenennen und Accounts hinzufügen
##### 5. Starte den Bot in einem Screen oder im Hintergrund
### Windows
##### 1. Lade den letzten Release von [Hier](https://github.com/TheRealHypR/myfreefarm-bot/releases)
##### 2. Lade den benötigten Driver runter
GeckoDriver wenn du Firefox benutzt:
```
https://github.com/mozilla/geckodriver/releases
```
ChromeDriver wenn du Chrome benutzt:
```
https://sites.google.com/a/chromium.org/chromedriver/downloads
```
##### 3. Die Datei `accounts_example_v1.X.json` zu `accounts.json` umbenennen und Accounts hinzufügen
## Hilfe zum Einstellen der accounts.json
```
{
  "accounts": {
    "accountname":{                 // Myfreefarm Login Name
      "active": "1",                // soll dieser Account beim Durchlauf beachtet werden? ( 1 = ja / 0 = nein )
      "server": "1",                // Myfreefarm Login Server
      "password": "secretpassword", // Myfreefarm Login Passwort
      "rackitem": "2",              // Nummer des Saatguts, dass auf den Feldern angepflanzt werden soll.
      "futtercount": "1",           // Wie viel Futter soll an die Tiere verfüttert werden?
      
      "fabrik_produkte": [9,110,11,12,0,0,0],   // siehe Extra Info
      
      "vertrag": {
        "partner": "accountname",   // Myfreefarm Login Name des Vertragpartners
        "rackitem": "9",            // Nummer der Ware, welche versendet werden soll.
        "menge": "8",               // wie viel der jeweiligen Ware versendet werden soll.
        "schwelle": "10",           // ab welchem Lagerbestand der Vertrag gesendet werden soll.
        "preis": "1.71"             // Preis pro Stück
      }
    }
  }
}
```
#### ```"fabrik_produkte"``` Extra Info:
Die einzelnen Zahlen sind die Zutaten für die Produkte der Produktionsgebäude.
```
[Mayo-Küche, Käserei, Wollspinnerei, Bonbonküche, Ölpresse, Spezialölmanufaktur, Strickerei]
```
> z.b.: Wenn in der Mayo-Küche Mayo hergestellt werden soll, kommt auf die erste Stelle 9 (siehe Beispiel-Konfig)  

|Gebäude|Produkt 1|Produkt 2|
|---|---|---|
|Mayo-Küche|9 (Mayo)|21 (Ketchup)|
|Käserei|10 (Käse)|110 (Jogurt)|
|Wollspinnerei|11 (Wolle)| / |
|Bonbonküche|12 (Bonbons)| / |
|Ölpresse|||
|Spezialölmanufaktur|||
|Strickerei|||
