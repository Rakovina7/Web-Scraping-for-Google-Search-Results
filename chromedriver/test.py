import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()
driver.get("https://www.google.com/")

def scrape_google(query):
    # find the search box element
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    # clear any pre-filled text in the search box
    search_box.clear()
    # enter the query in the search box
    search_box.send_keys(query + '\n')
    # wait for the page to load
    time.sleep(5)
    # extract the search result links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    for div in soup.find_all("div", class_="yuRUbf"):
        link = div.a["href"]
        links.append(link)
    return links[:500]

queries = ["query1", "query2", "query3"]

with open("google_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # write the header row
    writer.writerow(["Query", "URL"])
    # scrape the results for each query and write to CSV file
    for query in queries:
        urls = scrape_google(query)
        for url in urls:
            writer.writerow([query, url])

driver.close()
