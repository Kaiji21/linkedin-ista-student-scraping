from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time
import json

url = 'https://www.linkedin.com/search/results/people/?keywords=ista%20development%20informatique&origin=CLUSTER_EXPANSION&sid=V6d'
os.environ['PATH'] += os.pathsep + r'D:\Download File\roseta\chromdriver'
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=options)

def login():
    login = open('login.txt')
    line = login.readlines()

    email = line[0]
    password = line[1]

    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginbutton.click()
    time.sleep(3)


def getPersoneURLs():
    time.sleep(1)
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    source = BeautifulSoup(driver.page_source)

    Personnes = []
    visibleEmployees = source.find('ul', class_='reusable-search__entity-result-list list-style-none')
    #print(visibleEmployees)
    if visibleEmployees:
        li_elements = visibleEmployees.find_all('li', class_='reusable-search__result-container')
    for li in li_elements:
            # Extract information from each li element
            name_element = li.find('span', class_='entity-result__title-text')
            if name_element:
                name_link = name_element.find('a', class_='app-aware-link')
                profile_url = name_link.get('href', '')                  
                profile_url = profile_url.split('?')[0]
                if name_link:
                    name_span = name_link.find('span', {'dir': 'ltr'})
                    if name_span:
                        name = name_span.find('span', {'aria-hidden': 'true'}).text.strip()
                    else:
                        name = name_link.text.strip()
                else:
                    name = name_element.text.strip()
            else:
                name = 'N/A'
 
            occupation = li.find('div', class_='entity-result__primary-subtitle').text.strip() if li.find('div', class_='entity-result__primary-subtitle') else 'N/A'
            location = li.find('div', class_='entity-result__secondary-subtitle').text.strip() if li.find('div', class_='entity-result__secondary-subtitle') else 'N/A'
            
            person_info = {
                'name': name,
                'profile_url': profile_url,
                'occupation': occupation,
                'location': location
            }
            Personnes.append(person_info)
            save_to_csv(Personnes)
            save_to_json(Personnes)

        
    # print(f"Found {len(Personnes)} people:")


def save_to_csv(data):
    # Generate a filename with the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"linkedin_data_{timestamp}.csv"
    
    # Define the fieldnames for the CSV
    fieldnames = ['name', 'profile_url', 'occupation', 'location']
    
    # Write the data to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the data
        for person in data:
            writer.writerow(person)
    
    print(f"Data saved to {filename}")

def save_to_json(data):
    # Generate a filename with the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scrapeddata_{timestamp}.json"
    
    # Create a dictionary with a 'personnes' key containing the list of people
    data_to_save = {"personnes": data}
    
    # Write the data to the JSON file
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data_to_save, jsonfile, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {filename}")
   


login()
getPersoneURLs()
