# MyFreeBot
<b>English:</b> a python script to automate processes in myfreefarm.  
<b>German:</b> ein python skript um Prozesse in MyFreeFarm zu automatisieren.
## Installation
### Linux
##### 1. Install the needed packages
```
sudo apt-get install screen git nano python3 python3-pip firefox-esr
pip3 install selenium
```
Please note, that Firefox is the recommended browser to use this script with.

##### 2. Download the latest Geckodriver from here
```
https://github.com/mozilla/geckodriver/releases
```
##### 3. Clone this repository
```
git clone https://github.com/TheRealHypR/myfreefarm-bot.git
```
##### 4. Rename `accounts_example_v1.X.json` to `accounts.json` and edit as you need
##### 5. Start the Bot in a screen or something...
### Windows
##### 1. Download the latest release from the release section over [here](https://github.com/TheRealHypR/myfreefarm-bot/releases)
##### 2. Download the latest Geckodriver from here
```
https://github.com/mozilla/geckodriver/releases
```
##### 3. Download `accounts_example_v1.X.json` from source, rename it to `accounts.json` and edit as you need
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
|Gebäude|Produkt 1|Produkt 2|
|---|---|---|
|Mayo-Küche|9 (Mayo)|21 (Ketchup)|
|Käserei|10 (Käse)|110 (Jogurt)|
|Wollspinnerei|11 (Wolle)| / |
|Bonbonküche|12 (Bonbons)| / |
|Ölpresse|||
|Spezialölmanufaktur|||
|Strickerei|||
