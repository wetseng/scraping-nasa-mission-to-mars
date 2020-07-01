from splinter import Browser
from bs4 import BeautifulSoup

import json 

import pandas as pd
import time
from pprint import pprint

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find('div', class_='article_teaser_body').text

    # JPL Featured Images
    img_url =  'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # img_link = soup.find('article', class_='carousel_item')
    img_herf = soup.find('a', class_='button fancybox')['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov{img_herf}'

    # Mars Weather
    weather_url = 'https://twitter.com/MarsWxReport'
    browser.visit(weather_url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html5lib')
    timeline = soup.find_all('article')
    mars_weather_list =[]
    for tweet in timeline:
        mars_weather = tweet.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[4].text
        mars_weather_list.append(mars_weather)
    mars_weather = mars_weather_list[1]

    # Mars Facts
    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)
    df = tables[0]
    df.columns=['description', 'value']
    df = df.set_index('description')
    facts_html = df.to_html()

    # Mars Hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemisphere_image_urls = []
    enhanced_url_list = []

    hemi_all = soup.find_all('div', class_='item')
    # print(hemi_all)
    for hemi_idv in hemi_all:
        title = hemi_idv.find('h3').text
        enhanced_url = hemi_idv.a['href']
        enhanced_url = f'https://astrogeology.usgs.gov{enhanced_url}'
        enhanced_url_list.append(enhanced_url)
        
    for each_enhanced_url in enhanced_url_list:
        
        browser.visit(each_enhanced_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        org_hemi_url = soup.find('div', class_='downloads').a['href']
        hemisphere_image_urls.append({"title": title, "img_url": org_hemi_url})


    scrape_data = {'news_title' : news_title,
                    'news_p' : news_p,
                    'featured_image_url' : featured_image_url,
                    'mars_weather' : mars_weather,
                    'facts_html' : facts_html,
                    'hemisphere_image_urls' : hemisphere_image_urls
                        }

    browser.quit()

    return scrape_data