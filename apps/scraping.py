from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import pprint

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "Mars Hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
        }
    
    # Quit the browser & retrieve the data gathered:
    browser.quit()    
    return data
    
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # Set up the html parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()    
        # Begin Scraping
        slide_elem.find('div', class_='content_title')
        return news_title, news_p
    except AttributeError:
        return None, None

# '### Featured Images'
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&catagory=Mars'
    browser.visit(url)
    
    # Find and click the full image button using Splinter
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    
    # Find the more info button and click that using Splinter  
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    except AttributeError:
        return None
        

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url

    return img_url

def mars_facts():
    # Setting up code with DataFrame
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description','value']
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()
    
# Challenge Work - first define hemispheres variable
def mars_hemispheres(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Creating an empty dictinary in order to put information in
    hemisphere_final = []

    # Finding the pictures by tag function
    browser.is_element_present_by_css("thumb", wait_time=1)
    pictures = browser.find_by_tag('h3')

    # Loop the four pictures in order for them to render
    for x in range(0,4):
        
        # click each picture on the astrogeology.usgs.gov webpage
        pictures[x].click()

        # Parse
        html = browser.html
        hemisphere_beautifulsoup = BeautifulSoup(html, 'html.parser')

        # Finding image url
        img_url_rel = hemisphere_beautifulsoup.select_one('.wide-image').get('src')
        hemisphere_title = hemisphere_beautifulsoup.find('h2', class_='title').get_text()
        img_url = f'https://astrogeology.usgs.gov{img_url_rel}'

        # Now deliver the info into the new dictionary
        hemisphere_dict = {}
        hemisphere_dict['title'] = hemisphere_title 
        hemisphere_dict['img_url'] = img_url
        hemisphere_final.append(hemisphere_dict)

        browser.back()

        browser.is_element_present_by_css("thumb", wait_time=1)
        pictures = browser.find_by_tag('h3')

    # Return the completed list with all 4 hemispheres side by side on website
    return hemisphere_final

if __name__ == "__main__":

    print(scrape_all())