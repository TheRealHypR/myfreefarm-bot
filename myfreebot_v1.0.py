#!/usr/bin/python3
from selenium import webdriver
from time import sleep
import json

# PRAKTISCHE INFOS
# Ein Feld von Unkraut usw. befreien:
# var a = 1; while (a<121){raeumeFeld([FELDNUMMER], a); a++;}


def ernten(driver, feld_counter):
    currentuserlevel = driver.execute_script('return currentuserlevel;')
    if int(currentuserlevel) < 4:
        driver.execute_script('selectMode(1);')
        driver.execute_script('jsTimeStamp = Zeit.Client - Zeit.Verschiebung;')
        counter = 1
        while counter < 121:
            driver.execute_script('parent.cache_me(' + str(feld_counter) + ',' + str(counter) + ',garten_prod[' +
                                  str(counter) + '],garten_kategorie[' + str(counter) + ']);')
            counter += 1
            sleep(0.1)
    else:
        driver.execute_script('farmAction("cropgarden", 1, ' + str(feld_counter) + ');')
    sleep(0.5)
    return


def pflanzen(driver, feld_counter, saat_id):
    driver.execute_script('selectRackItem(' + saat_id + ');')
    counter = 1
    while counter < 121:
        driver.execute_script('parent.cache_me(' + str(feld_counter) + ',' + str(counter) + ',garten_prod[' +
            str(counter) + '],garten_kategorie[' + str(counter) + ']);')
        counter += 1
        sleep(0.1)
    return


def giessen(driver, feld_counter):
    driver.execute_script('selectMode(2);')
    driver.execute_script('jsTimeStamp = Zeit.Client - Zeit.Verschiebung;')
    counter = 1
    while counter < 121:
        driver.execute_script('parent.cache_me(' + str(feld_counter) + ',' + str(counter) + ',garten_prod[' +
            str(counter) + '],garten_kategorie[' + str(counter) + ']);')
        counter += 1
        sleep(0.1)
    return


def huehner_sammeln(driver, feld_counter):
    driver.execute_script("buildingInnerAction('crop',1," + str(feld_counter) + ");")
    sleep(0.5)
    return


def huehner_fuettern(driver, feld_counter, huhn_futtertyp, huhn_futtermenge):
    ajax_request = 'var myajax = createAjaxRequestObj(); myajax.open("GET", "ajax/farm.php?rid=" + rid'\
                   ' + "&mode=inner_feed&farm=1&position=' + str(feld_counter) + '&pid=' + str(huhn_futtertyp) +\
                   '&amount=' + str(huhn_futtermenge) + '&guildjob=0", true);'\
                   ' myajax.setRequestHeader("If-Modified-Since", "Sat, 1 Jan 2000 00:00:00 GMT"); myajax.send(null)'
    driver.execute_script(ajax_request)
    sleep(0.5)
    return


def vertrag(driver, vertrag_partner, vertrag_daten):
    script_string = 'var c={name: "' + vertrag_partner + '",cart: "' + vertrag_daten + '"};' \
                    ' generalAction("contracts_send", c, "' + vertrag_partner + '");'
    driver.execute_script(script_string)
    sleep(0.5)
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


def getfeldstatus(driver, feld_counter):
    prod_string = 'farms_data.farms[1][' + str(feld_counter) + '].production[0].remain;'
    try:
        prod_status = driver.execute_script('return ' + prod_string)
    except:
        return 'nicht in Arbeit'
    if int(prod_status) <= 0:
        return 'Fertig!'
    return 'in Arbeit!'


def getfeldname(driver, feld_counter):
    exec_string = 'farms_data.farms[1][' + str(feld_counter) + '].name;'
    for attempt in range(5):
        try:
            feld_art = driver.execute_script('return ' + exec_string)
        except:
            continue
        else:
            break
    else:
        return 'Fehler!'

    if feld_art == '':
        return 'Leer'
    return feld_art


def main():

    # headless chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    # start the selenium webdriver
    driver = webdriver.Chrome(options=options)

    while 1:

        # TODO: Möglichkeit verschiedene Account Files einlesen
        with open('accounts.json') as f:
            accounts = json.load(f)

        wartezeit = 0
        for account in accounts['accounts']:

            # USERDATA
            login_user = account
            print('--> JETZT KOMMT USER: ' + login_user)

            if int(accounts['accounts'][account]['active']) == 0:
                continue
            login_server = accounts['accounts'][account]['server']
            login_pass = accounts['accounts'][account]['password']
            saat_id = accounts['accounts'][account]['rackitem']
            if 'huhn' in accounts['accounts'][account]:
                huhn_futtertyp = accounts['accounts'][account]['huhn']['futtertyp']
                huhn_futtermenge = accounts['accounts'][account]['huhn']['futtercount']
            if 'kuh' in accounts['accounts'][account]:
                kuh_futtertyp = accounts['accounts'][account]['kuh']['futtertyp']
                kuh_futtermenge = accounts['accounts'][account]['kuh']['futtercount']

            # dynamische Produkt Zeiten
            # zeit_string = 'produkt_zeit[' + saat_id + '];'
            # wartezeit = driver.execute_script('return ' + zeit_string)

            if (int(accounts['accounts'][account]['waittime']) < wartezeit) or wartezeit == 0:
                wartezeit = int(accounts['accounts'][account]['waittime'])
            if 'vertrag' in accounts['accounts'][account]:
                vertrag_senden = 1
                vertrag_partner = accounts['accounts'][account]['vertrag']['partner']
                vertrag_produkt = str(accounts['accounts'][account]['vertrag']['produkt'])
                vertrag_daten = str(accounts['accounts'][account]['vertrag']['produkt']) + '_' +\
                                str(accounts['accounts'][account]['vertrag']['itemcount']) + '_' +\
                                str(accounts['accounts'][account]['vertrag']['itemprice']) + '_0|'
                vertrag_schwelle = int(accounts['accounts'][account]['vertrag']['schwelle'])
            else:
                vertrag_senden = 0

            # (re)load the website
            driver.get('https://www.myfreefarm.de')

            # myfreefarm login routine
            server_string = '//*[@id="loginserver"]/option[' + login_server + ']'
            driver.find_element_by_xpath(server_string).click()
            driver.find_element_by_id('loginusername').send_keys(login_user)  # input username
            driver.find_element_by_id('loginpassword').send_keys(login_pass)  # input password
            driver.find_element_by_id('loginbutton').submit()  # click the login button
            sleep(2)

            server_string = 'http://s' + login_server + '.myfreefarm.de'
            driver.get(server_string)
            print('Login erfolgreich')
            sleep(1)

            # Taegliches Los abholen
            print('Taegliches Los wird abgeholt...')
            if losabholen(driver):
                print('Erfolgreich!')
            else:
                print('Fehler beim Los abholen!')

            # Login Bonus abholen
            print('Taeglicher Login-Bonus wird abgeholt...')
            if loginbonus(driver):
                print('Erfolgreich!')
            else:
                print('Fehler beim Login-Bonus abholen!')

            feld_counter = 1
            while feld_counter < 7:
                feld_art = getfeldname(driver, feld_counter)
                feld_status = getfeldstatus(driver, feld_counter)

                status = 'Feld ' + str(feld_counter) + ': ' + feld_art + ' && Status: ' + feld_status
                print(status)

                if (feld_art == 'Acker') and ((feld_status == 'Fertig!') or (feld_status == 'nicht in Arbeit')):
                    print('jetzt wird geerntet...')
                    ernten(driver, feld_counter)
                    print('jetzt wird gepflanzt...')
                    pflanzen(driver, feld_counter, saat_id)
                    print('jetzt wird gegossen...')
                    giessen(driver, feld_counter)
                    print('Feld fertig!')

                if (feld_art == 'Hühnerstall') and ((feld_status == 'Fertig!') or (feld_status == 'nicht in Arbeit')):
                    print('jetzt werden Eier gesammelt...')
                    huehner_sammeln(driver, feld_counter)
                    print('jetzt werden Hühner gefüttert...')
                    huehner_fuettern(driver, feld_counter, huhn_futtertyp, huhn_futtermenge)
                    print('Feld fertig!')

                sleep(1)
                feld_counter += 1

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
