#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import JavascriptException
from time import sleep
import json

# PRAKTISCHE INFOS
# Ein Feld von Unkraut usw. befreien:
# var a = 1; while (a<121){raeumeFeld([FELDNUMMER], a); a++;}


def feld_ernten(driver, feld, saat_id):
    currentuserlevel = driver.execute_script('return currentuserlevel;')
    if int(currentuserlevel) < 4:
        driver.execute_script('var a=1;while(a<121){farmAction("garden_harvest", 1, ' + str(feld) + ', `pflanze[]=' + str(saat_id) + '&feld[]=${a}&felder[]=${a}`); a++;}')
    else:
        driver.execute_script('farmAction("cropgarden", 1, ' + str(feld) + ');')
    return


def feld_pflanzen(driver, feld, saat_id):
    driver.execute_script('var a=1; while (a<121){farmAction("garden_plant", 1, ' + str(feld) + ', `pflanze[]=' + str(saat_id) + '&feld[]=${a}&felder[]=${a}`, 5); a++;}')
    return


def feld_giessen(driver, feld):
    driver.execute_script('var a=1;while(a<121){farmAction("garden_water", 1, ' + str(feld) + ', `feld[]=${a}&felder[]=${a}`); a++;}')
    return


def tiere_sammeln(driver, farm, feld):
    driver.execute_script('buildingInnerAction("crop",' + str(farm) + ',' + str(feld) + ');')
    return


def tiere_fuettern(driver, farm, feld, futtermenge):
    rack = driver.execute_script('return rackElement')
    if int(rack[1]['number']) <= int(rack[2]['number']):
        huhn_food = 1
    else:
        huhn_food = 2
    huhn_food = max(int(rack[1]['number']), int(rack[2]['number']))
    kuh_food = max(int(rack[3]['number']), int(rack[4]['number']))
    schaf_food = max(int(rack[5]['number']), int(rack[6]['number']))
    bee_food = max(int(rack[7]['number']), int(rack[8]['number']))
    fisch_food = max(int(rack[92]['number']), int(rack[93]['number']))

    ajax_request = 'var myajax = createAjaxRequestObj(); myajax.open("GET", "ajax/farm.php?rid=" + rid'\
                   ' + "&mode=inner_feed&farm=' + str(farm) + '&position=' + str(feld) + '&pid=' + str(futtertyp) +\
                   '&amount=' + str(futtermenge) + '&guildjob=0", true);'\
                   ' myajax.setRequestHeader("If-Modified-Since", "Sat, 1 Jan 2000 00:00:00 GMT"); myajax.send(null)'
    driver.execute_script(ajax_request)
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

    """
    # login direkt mit request (geht noch nicht)
    ajax_request = 'new Ajax.Request("ajax/createtoken2.php?n=" + n, {method:"post",parameters:' \
                   '{server:"' + login_server + '", username:"' + login_user + '",' \
                   'password:"' + login_pass + '", ref:"", retid:"" }, onSuccess: function(transport)' \
                   '{var result = transport.responseText.evalJSON(); location.href = result[1]; }});'
    get_data = driver.execute_script(ajax_request)
    """
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
        sleep(1)


def main():

    # headless firefox options
    options = Options()
    options.headless = True
    
    # start the selenium webdriver
    driver = webdriver.Firefox(firefox_binary='C:/Users/pmadelmayer/AppData/Local/Mozilla Firefox/firefox.exe', options=options)

    while 1:
        # TODO: Möglichkeit verschiedene Account Files einlesen
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

            # dynamische Produkt Zeiten
            zeit_string = 'return produkt_zeit[' + saat_id + '];'
            wartezeit = driver.execute_script(zeit_string)

            if 'vertrag' in accounts['accounts'][account]:
                vertrag_senden = 1
                vertrag_partner = accounts['accounts'][account]['vertrag']['partner']
                vertrag_produkt = str(accounts['accounts'][account]['vertrag']['rackitem'])
                vertrag_daten = str(accounts['accounts'][account]['vertrag']['rackitem']) + '_' +\
                                str(accounts['accounts'][account]['vertrag']['itemcount']) + '_' +\
                                str(accounts['accounts'][account]['vertrag']['itemprice']) + '_0|'
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
                    feld_art = farminfo[str(feld)]['buildingid']
                    is_animal = farminfo[str(feld)]['animals']

                    if 'production' in farminfo[str(feld)]:
                        produkt = farminfo[str(feld)]['production'][0]['pid']
                        remain = farminfo[str(feld)]['production'][0]['remain']

                        if int(remain) <= 0 and int(feld_art) == 1:
                            print('Fertiger Acker wird neu bepflanzt!')
                            print('jetzt wird geerntet...')
                            feld_ernten(driver, feld, produkt)
                            print('jetzt wird gepflanzt...')
                            feld_pflanzen(driver, feld, saat_id)
                            print('jetzt wird gegossen...')
                            feld_giessen(driver, feld)
                            print('Feld fertig!')
                        elif int(remain) <= 0 and int(is_animal) > 0:
                            print('Fertige Tiere werden neu gefüttert!')
                            print('jetzt werden Tierprodukte gesammelt...')
                            tiere_sammeln(driver, farm, feld)
                            print('jetzt werden Tiere gefüttert...')
                            tiere_fuettern(driver, farm, feld, futtermenge)
                            print('Tiere fertig!')
                        else:
                            print('Feld/Tiere in Arbeit, übersprungen!')
                    else:
                        if int(feld_art) == 1:
                            print('Leerer Acker wird bepflanzt!')
                            print('jetzt wird gepflanzt...')
                            feld_pflanzen(driver, feld, saat_id)
                            print('jetzt wird gegossen...')
                            feld_giessen(driver, feld)
                            print('Feld fertig!')
                        elif int(is_animal) > 0:
                            print('Untätige Tiere werden gefüttert!')
                            print('jetzt werden Tiere gefüttert...')
                            tiere_fuettern(driver, farm, feld, futtermenge)
                            print('Tiere fertig!')
                        else:
                            print('Bauplatz nicht freigeschaltet oder leer!')

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
