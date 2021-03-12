import xlsxwriter
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json


 
url="https://www.zoopla.co.uk/find-agents/estate-agents/london/waterloo/?q=Waterloo%2C%20London&radius=40&search_source=find-agents%2Festate-agents"

urlPrincipal="https://www.zoopla.co.uk"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome("C:\CURSOS\pyhton raspa tela telegram bot\chromedriver.exe", options=options)
driver.get(url)

agentList=[]


        
class Agent(object):
    name = ""
    address = ""
    phone = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone
    def as_dict(self):
        return {'name': self.name, 'address': self.address, 'phone': self.phone}

def getAgentData():   
    name=driver.find_element_by_xpath("//div[@class='sidebar sbt']//p//strong").get_attribute('innerHTML')
  
    address=driver.find_element_by_xpath("//div[@class='sidebar sbt']//p//span").get_attribute('innerHTML')
  
    phone=driver.find_element_by_xpath("//div[@class='sidebar sbt']//p//span[@class='agent_phone']//a").get_attribute('href')
    
    agentList.append(Agent(name,address,phone))

def getListaAgents():
    page = requests.get('https://www.zoopla.co.uk/find-agents/estate-agents/london/waterloo/?q=Waterloo%2C%20London&radius=40&search_source=find-agents%2Festate-agents')    
    soup = BeautifulSoup(page.text, 'html.parser') 
    all_a = soup.select('.ui-text-t4 a')
  
    for i in range(2, 200):      
        page = requests.get('https://www.zoopla.co.uk/find-agents/estate-agents/london/waterloo/?q=Waterloo%2C+London&radius=40&search_source=find-agents%2Festate-agents&pn=2'+str(i))    
        soup = BeautifulSoup(page.text, 'html.parser')    
        all_a =all_a + soup.select('.ui-text-t4 a')
    
    return all_a
   
def accessListaAgents(listaAgents):
    for a in listaAgents:
        urlFoda=urlPrincipal + a['href']     
        print(urlFoda)
        driver.get(urlFoda)
        getAgentData()
        
accessListaAgents(getListaAgents())

df = pd.DataFrame([x.as_dict() for x in agentList])
df.to_excel(r'agooorafoi.xlsx', index = False)


driver.quit()
#print (getListaAgents())
