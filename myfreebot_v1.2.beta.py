#!/usr/bin/python3
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import JavascriptException
from time import sleep
import json

# PRAKTISCHE INFOS
# Ein Feld von Unkraut usw. befreien:
# var a = 1; while (a<121){raeumeFeld([FELDNUMMER], a); a++;}


def feld_ernten(driver, farm, feld, produkt):
    currentuserlevel = driver.execute_script('return currentuserlevel;')
    if int(currentuserlevel) < 4:
        script_string = 'return produkt_x[' + produkt + '] * produkt_y[' + produkt + ']'
        plant_size = driver.execute_script(script_string)
        steps = range(1, 121)
        skips = [13, 15, 17, 19, 21, 23, 37, 39, 41, 43, 45, 47, 61, 63, 65, 67, 69, 71, 85, 87, 89, 91, 93, 95, 109, 111, 113, 115, 117, 119]

        if int(plant_size) == 1:
            for i in range(1, 121):
                driver.execute_script('farmAction("garden_harvest", ' + str(farm) + ', ' + str(feld) + ', "pflanze[]=' + str(produkt) + '&feld[]=' + str(i) + '&felder[]=' + str(i) + '");')
            return

        if int(plant_size) == 2:
            for i in steps[::2]:
                driver.execute_script('farmAction("garden_harvest", ' + str(farm) + ', ' + str(feld) + ', "pflanze[]=' + str(produkt) + '&feld[]=' + str(i) + '&felder[]=' + str(i) + ',' + str(i + 1) + '");')
            return

        if int(plant_size) == 4:
            for i in steps[::2]:
                if i in skips:
                    continue
                driver.execute_script('farmAction("garden_harvest", ' + str(farm) + ', ' + str(feld) + ', "pflanze[]=' + str(produkt) + '&feld[]=' + str(i) + '&felder[]=' + str(i) + ',' + str(i + 1) + ',' + str(i + 12) + ',' + str(i + 13) + '");')
            return
    else:
        driver.execute_script('farmAction("cropgarden", ' + str(farm) + ', ' + str(feld) + ');')
    return


def feld_pflanzen(driver, farm, feld, saat_id):
    script_string = 'return produkt_x[' + saat_id + '] * produkt_y[' + saat_id + ']'
    plant_size = driver.execute_script(script_string)
    steps = range(1, 121)
    skips = [13, 15, 17, 19, 21, 23, 37, 39, 41, 43, 45, 47, 61, 63, 65, 67, 69, 71, 85, 87, 89, 91, 93, 95, 109, 111, 113, 115, 117, 119]

    if int(plant_size) == 1:
        for i in range(1, 121):
            driver.execute_script('farmAction("garden_plant", ' + str(farm) + ', ' + str(feld) + ', "pflanze[]=' + str(saat_id) + '&feld[]=' + str(i) + '&felder[]=' + str(i) + '", 5);')
        return

    if int(plant_size) == 2:
        for i in steps[::2]:
            driver.execute_script('farmAction("garden_plant", ' + str(farm) + ', ' + str(feld) + ', "pflanze[]=' + str(saat_id) + '&feld[]=' + str(i) + '&felder[]=' + str(i) + ',' + str(i+1) + '", 5);')
        return

    if int(plant_size) == 4:
        for i in steps[::2]:
            if i in skips:
                continue
            driver.execute_script('farmAction("garden_plant", ' + str(farm) + ', ' + str(feld) + ', "pflanze[]=' + str(saat_id) + '&feld[]=' + str(i) + '&felder[]=' + str(i) + ',' + str(i+1) + ',' + str(i+12) + ',' + str(i+13) + '", 5);')
        return


def feld_giessen(driver, farm, feld, saat_id):
    script_string = 'return produkt_x[' + saat_id + '] * produkt_y[' + saat_id + ']'
    plant_size = driver.execute_script(script_string)
    steps = range(1, 121)
    skips = [13, 15, 17, 19, 21, 23, 37, 39, 41, 43, 45, 47, 61, 63, 65, 67, 69, 71, 85, 87, 89, 91, 93, 95, 109, 111, 113, 115, 117, 119]

    if int(plant_size) == 1:
        for i in range(1, 121):
            driver.execute_script('farmAction("garden_water", ' + str(farm) + ', ' + str(feld) + ', "feld[]=' + str(i) + '&felder[]=' + str(i) + '");')
        return

    if int(plant_size) == 2:
        for i in steps[::2]:
            driver.execute_script('farmAction("garden_water", ' + str(farm) + ', ' + str(feld) + ', "feld[]=' + str(i) + '&felder[]=' + str(i) + ',' + str(i + 1) + '");')
        return

    if int(plant_size) == 4:
        for i in steps[::2]:
            if i in skips:
                continue
            driver.execute_script('farmAction("garden_water", ' + str(farm) + ', ' + str(feld) + ', "feld[]=' + str(i) + '&felder[]=' + str(i) + ',' + str(i + 1) + ',' + str(i + 12) + ',' + str(i + 13) + '");')
        return


def tiere_fuettern(driver, farm, feld, futtermenge, buildingid):
    """
    buildingids
    2 = Hühner, 3 = Kühe, 4 = Schafe, 5 = Bienen, 11 = Fischzucht, 12 = Ziegen, 15 = Hasen
    """
    rack = driver.execute_script('return rackElement')
    if int(buildingid) == 2:  # Hühner
        if int(rack['1']['number']) >= int(rack['2']['number']):
            futtertyp = 1
        else:
            futtertyp = 2
    elif int(buildingid) == 3:  # Kühe
        if int(rack['3']['number']) >= int(rack['4']['number']):
            futtertyp = 3
        else:
            futtertyp = 4
    elif int(buildingid) == 4:  # Schafe
        if int(rack['5']['number']) >= int(rack['6']['number']):
            futtertyp = 5
        else:
            futtertyp = 6
    elif int(buildingid) == 5:  # Bienen
        if int(rack['7']['number']) >= int(rack['8']['number']):
            futtertyp = 7
        else:
            futtertyp = 8
    elif int(buildingid) == 11:  # Zierfische
        if int(rack['92']['number']) >= int(rack['93']['number']):
            futtertyp = 92
        else:
            futtertyp = 93
    else:
        print('FARM', farm, ', FELD', feld, ': Fehler beim auswählen des Futters. Produktion übersprungen!')
        return

    ajax_request = 'var myajax = createAjaxRequestObj(); myajax.open("GET", "ajax/farm.php?rid=" + rid'\
                   ' + "&mode=inner_feed&farm=' + str(farm) + '&position=' + str(feld) + '&pid=' + str(futtertyp) +\
                   '&amount=' + str(futtermenge) + '&guildjob=0", true);'\
                   ' myajax.setRequestHeader("If-Modified-Since", "Sat, 1 Jan 2000 00:00:00 GMT"); myajax.send(null)'
    driver.execute_script(ajax_request)
    return


def fabrik_starten(driver, farm, feld, buildingid, fabrik_produkte):
    """
    buildingids
    7 = Mayo-Ketchup, 8 = Käse, 9 = Wolle, 10 = Bonbons, 13 = Öl, 14 = Spezialöl, 16 = Strickerei
    """
    if int(buildingid) == 7:
        driver.execute_script('farmAction("setadvancedproduction", ' + str(farm) + ', ' + str(feld) + ', ' + str(fabrik_produkte[0]) + ', undefined)')
    elif int(buildingid) == 8:
        driver.execute_script('farmAction("setadvancedproduction", ' + str(farm) + ', ' + str(feld) + ', ' + str(fabrik_produkte[1]) + ', undefined)')
    elif int(buildingid) == 9:
        driver.execute_script('farmAction("setadvancedproduction", ' + str(farm) + ', ' + str(feld) + ', ' + str(fabrik_produkte[2]) + ', undefined)')
    elif int(buildingid) == 10:
        driver.execute_script('farmAction("setadvancedproduction", ' + str(farm) + ', ' + str(feld) + ', ' + str(fabrik_produkte[3]) + ', undefined)')
    elif int(buildingid) == 13:
        driver.execute_script('farmAction("setadvancedproduction", ' + str(farm) + ', ' + str(feld) + ', ' + str(fabrik_produkte[4]) + ', undefined)')
    elif int(buildingid) == 14:
        driver.execute_script('farmAction("setadvancedproduction", ' + str(farm) + ', ' + str(feld) + ', ' + str(fabrik_produkte[5]) + ', undefined)')
    elif int(buildingid) == 16:
        driver.execute_script('farmAction("setadvancedproduction", ' + str(farm) + ', ' + str(feld) + ', ' + str(fabrik_produkte[6]) + ', undefined)')
    else:
        print('FARM', farm, ', FELD', feld, ': Fehler beim starten der Fabrik. Produktion übersprungen!')
    return



def vertrag(driver, vertrag_partner, vertrag_daten):
    script_string = 'var c={name: "' + vertrag_partner + '",cart: "' + vertrag_daten + '"};' \
                    ' generalAction("contracts_send", c, "' + vertrag_partner + '");'
    driver.execute_script(script_string)
    return


def losabholen(driver):
    try:
        driver.execute_script('dailyLot();')
        driver.execute_script('lotGetPrize();')
    except:
        return False
    return True


def loginbonus(driver):
    try:
        driver.execute_script('loginbonus.getReward();')
    except:
        return False
    return True


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        sleep(1)
        t -= 1


def login(driver, login_user, login_server, login_pass):
    # (re)load the website
    driver.get('https://www.myfreefarm.de')

    # myfreefarm login routine
    server_string = '//*[@id="loginserver"]/option[' + login_server + ']'
    driver.find_element_by_xpath(server_string).click()
    driver.find_element_by_id('loginusername').send_keys(login_user)  # input username
    driver.find_element_by_id('loginpassword').send_keys(login_pass)  # input password
    driver.find_element_by_id('loginbutton').submit()  # click the login button
    sleep(1)

    server_string = 'http://s' + login_server + '.myfreefarm.de'
    driver.get(server_string)
    sleep(1)

    try:
        driver.execute_script('return farm')
    except JavascriptException:
        print('Beim Login ist ein Fehler aufgetreten!')
        exit(1)
    else:
        print('Login erfolgreich!')


def main():
    """
    # selenium - headless firefox options
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(firefox_binary='',options=firefox_options)
    """
    # selenium - headless chrome options
    chrome_options = Options()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)

    while 1:
        with open('accounts.json') as acc_file:
            accounts = json.load(acc_file)

        for account in accounts['accounts']:
            # ACCOUNT DATA
            login_user = account
            print('--> JETZT KOMMT USER: ' + login_user)

            if int(accounts['accounts'][account]['active']) == 0:
                continue
            login_server = accounts['accounts'][account]['server']
            login_pass = accounts['accounts'][account]['password']

            # LOGIN: so früh wie möglich
            login(driver, login_user, login_server, login_pass)

            saat_id = accounts['accounts'][account]['rackitem']
            futtermenge = accounts['accounts'][account]['futtermenge']
            if 'fabrik_produkte' in accounts['accounts'][account]:
                fabrik_produkte = accounts['accounts'][account]['fabrik_produkte']

            # dynamische Produkt Zeiten
            zeit_string = 'return produkt_zeit[' + saat_id + '];'
            wartezeit = driver.execute_script(zeit_string)

            if 'vertrag' in accounts['accounts'][account]:
                vertrag_senden = 1
                vertrag_partner = accounts['accounts'][account]['vertrag']['partner']
                vertrag_produkt = str(accounts['accounts'][account]['vertrag']['rackitem'])
                vertrag_daten = str(accounts['accounts'][account]['vertrag']['rackitem']) + '_' +\
                                str(accounts['accounts'][account]['vertrag']['menge']) + '_' +\
                                str(accounts['accounts'][account]['vertrag']['preis']) + '_0|'
                vertrag_schwelle = int(accounts['accounts'][account]['vertrag']['schwelle'])
            else:
                vertrag_senden = 0

            # Taegliches Los abholen
            print('Taegliches Los wird abgeholt...')
            if not losabholen(driver):
                print('Fehler beim Los abholen!')

            # Login Bonus abholen
            print('Taeglicher Login-Bonus wird abgeholt...')
            if not loginbonus(driver):
                print('Fehler beim Login-Bonus abholen!')

            # FARMEN

            farmamount = driver.execute_script('return farmamount')
            for farm in range(1, farmamount+1):
                farmstring = 'return farms_data.farms[' + str(farm) + ']'
                farminfo = driver.execute_script(farmstring)

                for feld in range(1, 7):
                    buildingid = farminfo[str(feld)]['buildingid']
                    buildingids_tiere = [2, 3, 4, 5, 11, 12, 15]
                    buildingids_fabrik = [7, 8, 9, 10, 13, 14, 16]
                    """
                    premiumfelder überspringen
                    try:
                        farminfo[str(feld)]['premium']
                    except KeyError:
                        pass
                    else:
                        continue
                    """
                    if 'production' in farminfo[str(feld)]:
                        produkt = farminfo[str(feld)]['production'][0]['pid']
                        remain = farminfo[str(feld)]['production'][0]['remain']

                        if int(remain) <= 0 and int(buildingid) == 1:
                            print('FARM', farm, ', FELD', feld, ': Fertiger Acker wird neu bepflanzt!')
                            print('jetzt wird geerntet...')
                            feld_ernten(driver, farm, feld, produkt)
                            sleep(0.1)
                            print('jetzt wird gepflanzt...')
                            feld_pflanzen(driver, farm, feld, saat_id)
                            sleep(0.1)
                            print('jetzt wird gegossen...')
                            feld_giessen(driver, farm, feld, saat_id)
                            sleep(0.1)
                            print('Feld fertig!')
                        elif int(remain) <= 0 and int(buildingid) in buildingids_tiere:
                            print('FARM', farm, ', FELD', feld, ': Fertige Tiere werden neu gefüttert!')
                            print('jetzt wird gesammelt...')
                            driver.execute_script('buildingInnerAction("crop",' + str(farm) + ',' + str(feld) + ');')
                            sleep(0.1)
                            print('jetzt wird gefüttert...')
                            tiere_fuettern(driver, farm, feld, futtermenge, buildingid)
                            sleep(0.1)
                            print('Tiere fertig!')
                        elif int(remain) <= 0 and int(buildingid) in buildingids_fabrik:
                            print('FARM', farm, ', FELD', feld, ': Fertige Fabrik wird neu gestartet!')
                            print('jetzt wird gesammelt...')
                            driver.execute_script('farmAction("harvestproduction",' + str(farm) + ', ' + str(feld) + ', 1);')
                            sleep(0.1)
                            print('jetzt wird gestartet...')
                            fabrik_starten(driver, farm, feld, buildingid, fabrik_produkte)
                            sleep(0.1)
                            print('Fabrik fertig!')
                        else:
                            print('FARM', farm, ', FELD', feld, ': Feld/Tiere/Fabrik in Arbeit, übersprungen!')
                    else:
                        if int(buildingid) == 1:
                            print('FARM', farm, ', FELD', feld, ': Leerer Acker wird bepflanzt!')
                            print('jetzt wird gepflanzt...')
                            feld_pflanzen(driver, farm, feld, saat_id)
                            sleep(0.1)
                            print('jetzt wird gegossen...')
                            feld_giessen(driver, farm, feld, saat_id)
                            sleep(0.1)
                            print('Feld fertig!')
                        elif int(buildingid) in buildingids_tiere:
                            print('FARM', farm, ', FELD', feld, ': Untätige Tiere werden gefüttert!')
                            print('jetzt wird gefüttert...')
                            tiere_fuettern(driver, farm, feld, futtermenge, buildingid)
                            sleep(0.1)
                            print('Tiere fertig!')
                        elif int(buildingid) in buildingids_fabrik:
                            print('FARM', farm, ', FELD', feld, ': Untätige Fabrik wird gestartet!')
                            print('jetzt wird gestartet...')
                            fabrik_starten(driver, farm, feld, buildingid, fabrik_produkte)
                            sleep(0.1)
                            print('Fabrik fertig!')
                        else:
                            print('FARM', farm, ', FELD', feld, ': Bauplatz nicht freigeschaltet oder leer!')

            if vertrag_senden == 1:
                anzahl_string = 'rackElement[' + vertrag_produkt + ']["number"];'

                try:
                    anzahl_value = driver.execute_script('return ' + anzahl_string)
                except:
                    anzahl_value = 0
                if int(anzahl_value) >= vertrag_schwelle:
                    print('Vertrag wird gesendet...')
                    vertrag(driver, vertrag_partner, vertrag_daten)

            sleep(1)
            driver.execute_script("location.href='main.php?page=logout&logoutbutton=1';")
            sleep(1)
        print('Bot wartet jetzt ' + str(wartezeit) + ' Sekunden:')
        countdown(wartezeit)


if __name__ == '__main__':
    main()
