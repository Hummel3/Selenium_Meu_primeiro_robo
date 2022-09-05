from urllib import response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as firefoxoptions
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import requests

def __firefoxoptions():
        options = firefoxoptions()
        # options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.helperApps.alwaysAsk.force", False)
        options.set_preference("browser.helperApps.neverAsk.openFile", "binary/octet-stream, application/zip, application/octet-stream, image/jpeg, application/vnd.ms-outlook, text/html, application/pdf, application/mp4, video/mp4")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "binary/octet-stream, application/zip, application/octet-stream, image/jpeg, application/vnd.ms-outlook, text/html, application/pdf, application/mp4, video/mp4")
        options.set_preference("browser.download.manager.focusWhenStarting",False)
        options.set_preference("browser.download.manager.useWindow", False)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        options.set_preference("browser.download.manager.closeWhenDone", False)
        options.set_preference("media.volume_scale", "0.0")
        options.set_preference("geo.enabled",True)
        return options
nav = webdriver.Firefox(executable_path="C:\\geckodriver.exe",firefox_profile=webdriver.FirefoxProfile("C:\\Users\\stefa\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\bh234w83.default-release"),options=__firefoxoptions())

nav.get("https://www.ifood.com.br/delivery/descobrir/lanches/16d7f283-cfff-49b6-9616-921fd7af4d8a?categories=BUR&features=superRestaurant&sort=user_rating%3Adesc")

time.sleep(1)

hambur=nav.find_elements(By.CLASS_NAME,"merchant-v2__link")
links=[]
for hamburguer in hambur:
    links.append(hamburguer.get_attribute("href"))


for link in links:
    nav.get(link)
    time.sleep(5)
    titulo = nav.find_element(By.CLASS_NAME,"merchant-info__title")
    nav.find_element(By.CLASS_NAME,"merchant-details__button").click()
    time.sleep(5)
    dados=nav.find_elements(By.CLASS_NAME,"merchant-details-about__info-data")
    print(" ",file=sys.stderr)
    print(titulo.get_attribute("innerText"),file=sys.stderr)
    for dado in dados:
        dado_str=dado.get_attribute("innerText")
        print(dado_str,file=sys.stderr)
        cnpj=""
        if "CNPJ" in dado_str:
            caracteres_remove=['.','-','/']
            cnpj=dado_str
            for x in caracteres_remove:
               cnpj=cnpj.replace(x,'')
            cnpj=cnpj.replace("CNPJ:",'')
            cnpj=cnpj.replace(" ",'')
            # print(cnpj,file=sys.stderr)
            api_url="https://publica.cnpj.ws/cnpj/"+cnpj
            response=requests.get(api_url)
            resposta=response.json()
            estabelecimento=resposta['estabelecimento']
            print("razao social: " +resposta['razao_social'],file=sys.stderr)
            print("telefone: ("+estabelecimento['ddd1']+") "+ estabelecimento['telefone1'],file=sys.stderr)
            print("email: "+estabelecimento['email'],file=sys.stderr)
        
    print(" ",file=sys.stderr)


        
nav.quit()

