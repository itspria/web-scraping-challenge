from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_Data = {}     
    news = scrapeNews("https://redplanetscience.com/", browser)
    mars_Data["news_title"] = news["title"]
    mars_Data["news_details"] = news["details"]
    mars_Data["image_url"] = scrapeImage("https://spaceimages-mars.com/", browser)
    mars_Data["hemispheres"] = scrapeHemispheres("https://marshemispheres.com/", browser)
    mars_Data["factsTable"] = scrapeFacts("https://galaxyfacts-mars.com/")   

    # Quit the browser
    browser.quit()

    return mars_Data


# Scrape for latest mars news and return title and detailed news
def scrapeNews(url, browser):    
    news = {}
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_='content_title').text
    details = soup.find('div', class_='article_teaser_body').text
    news["title"] = title
    news["details"] = details
    return news

# Scrape for featured image of Mars and return the url
def scrapeImage(url, browser):    
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.find('img', class_='headerimage')['src']
    featured_image_url = url + image_url
    return featured_image_url

# Scrape for the different hemispheres and its respective image URLs
def scrapeHemispheres(url, browser):
    
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    items = image_url = soup.find_all('div', class_='description')
    for item in items:
        title = item.find('h3').text
        link = item.find('a')['href']
      
        browser.visit(url+link)
        soup = BeautifulSoup(browser.html, 'html.parser')

        divDownload = soup.find("div", class_="downloads")
        imageLink = url + divDownload.find('a')['href']       
        hemisphere_image_urls.append({"title": title, "image_url": imageLink})
        browser.back()
    
    return hemisphere_image_urls

def scrapeFacts(url):
    tables = pd.read_html(url)
    facts_table = tables[1].copy()
    facts_table.columns = ['Indicator', 'Value']
    return facts_table.to_html(index=False, classes="table table-striped table-bordered")

