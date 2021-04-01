
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import pymongo
import time

# Set Executable Path & Initialize Chrome Browser
from webdriver_manager.chrome import ChromeDriverManager


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.mars

def init_browser():
        executable_path = {'executable_path': ChromeDriverManager().install()}
        #return browser = Browser('chrome', **executable_path, headless=True)
        return Browser('chrome', **executable_path, headless=True)
def scrape():
        #dict to store info
        mars_data = {}

         # 1 NASA Mars News
        browser = init_browser()
        url =  "https://mars.nasa.gov/news/"
        browser.visit(url)
        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")


        # NASA Mars News
        news_title = soup.find("div", class_="list_text").get_text()
        #print(news_title)

        # news paragraph
        news_paragraph = soup.find("div", class_="article_teaser_body").get_text()
        #print(news_paragraph)

        # Close the browser after scraping
        browser.quit()

        mars_data["news_title"]  = news_title 
        mars_data["news_paragraph"] = news_paragraph

        ###########################################################################################
        ###########################################################################################



        # 2 Search for image source
        #JPL Mars Space Images - Featured Image
        # from webdriver_manager.chrome import ChromeDriverManager
        # executable_path = {'executable_path': ChromeDriverManager().install()}
        # #browser = Browser('chrome', **executable_path, headless=True)
        # return Browser('chrome', **executable_path, headless=True)

        browser = init_browser()
        url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
        browser.visit(url)
        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        image_soup = bs(html, "html.parser")


        # 2 Search for image source
        # Use splinter to navigate the site and find the image url for the current Featured Mars Image
        relative_img_path = image_soup.find_all('img')[1]["src"]
        url2 = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
        featured_img_url = url2 + relative_img_path
        #print(featured_img_url)

        # Close the browser after scraping
        browser.quit()

        mars_data["featured_img_url"] = featured_img_url

        # ###########################################################################################
        # ###########################################################################################





        #3 Mars Facts
        # use Pandas to scrape the table containing facts about the planet 
        fact_tables = pd.read_html('https://space-facts.com/mars/')
        df = fact_tables[0]
        df.columns=['Description', 'Values']
        df = df.set_index('Description', drop=True)

        #Use Pandas to convert the data to a HTML table string.
        #mars_facts_table = [df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]
        mars_facts_table = df.to_html()
        mars_facts_table.replace('\n', '')
        #save the table directly to a file.
        #df.to_html('table.html')
        #return df.to_html
        mars_data["mars_facts_table"] = mars_facts_table

        # ###########################################################################################
        # ###########################################################################################




        # 4 Mars Hemispheres
        # Visit the USGS Astrogeology and obtain high resolution images for each of Mar's hemispheres.
        browser = init_browser()
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        base_url = "https://astrogeology.usgs.gov"
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')

        results = soup.find_all('div', class_="item")
        dict_list = []

        for i in results:
                hemispheres_titles = i.find('h3').text
        
                target_url = base_url + i.find('a')['href']
                browser.visit(target_url)
                time.sleep(1)
        
                final_img_html = browser.html
                soup = bs( final_img_html, 'html.parser')
                hemispheres_urls = base_url + soup.find('img', class_='wide-image')['src']
        
        
                entity_dict = {"title":hemispheres_titles, "img_url":hemispheres_urls}
                dict_list.append(entity_dict)
        
        # Close the browser after scraping
        browser.quit()
        
        mars_data["hemisphere_imgs"] = dict_list

        return mars_data
        ###########################################################################################
        ###########################################################################################




