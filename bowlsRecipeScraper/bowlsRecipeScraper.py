#selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
#webdriver imports
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager   
#to set timeout between requests
import time
#for scraping the summary
import requests
from bs4 import BeautifulSoup
#for scraping other data from recipe
from recipe_scrapers import scrape_me

# connect to website using selenium and web driver
def connect(url):
    """
    create chrome driver
    :param url: url to connect: str
    :return: chrome driver: obj
    """
    options = Options()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = options)
    try:
        driver.get(url)
        time.sleep(5)
    except TimeoutException:
        #print("new connection try")
        driver.get(url)
        time.sleep(5)
        
    return driver

# get all recipe links from one page
def get_links_from_one_page(my_webpage):
    """
    To collect links for each recipe from one page
    :param my_webpage: link to page for scrapping: selenium obj
    :return: links from one page: list[str]
    """
    recipe_links = []
    #on bowlofdelicious.com there are 24 links per page
    for i in range(1, 25):
        try:
            recipe = my_webpage.find_element(By.XPATH, f'/html/body/div/div[3]/div/main/article[{i}]/header/h2/a')
        except:
            continue
        recipe_links.append(recipe.get_attribute('href'))
    return recipe_links

# get all recipe links from all pages on the website
def get_links_from_site(recipe_driver, num_pages):
    """
    To list pages on website and collect links into list
    :param recipe_driver: obj  chrome driver
    :param num_pages: int number of pages to scrap / default 0
    :return: list of links: list[str]
    """
    all_pages_links = []
    for i in range(1, num_pages):
        # get links from one page
        page = get_links_from_one_page(recipe_driver)
        all_pages_links.extend(page)

        try:
            # go to next page
            recipe_driver.find_element(By.CLASS_NAME, 'pagination-next').find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)
            #print(f'page {i} is collected')
        except NoSuchElementException:
            continue
        
    return all_pages_links

# get all links based on a category
def get_links_site_by_category(category):
    """
    Get recipe links from bowl of delicious website based on category
    Args:
        category: str category to scrap (breakfast, lunch or dinner)
    Return:
        list[str]: list of links
    """
    #determine url and number of pages
    url = f'https://www.bowlofdelicious.com/category/{category}/'
    if category == 'breakfast':
        num_pages = 5
    elif category == 'lunch':
        num_pages = 6
    elif category == 'dinner':
        num_pages = 13
    else:
        num_pages = 1
        
    #create a driver
    driver = connect(url)
    
    #collect links
    try: 
        links = get_links_from_site(driver, num_pages)
    except:
        links = []
    
    return links

# scrap recipe summary from a specific recipe link
def get_summary(link):
    """
    Get recipe summary from bowl of delicious link
    
    Args:
        link (str): link to recipe
    Return:
        str: recipe summary
    
    """
    req = requests.get(link)
    html = BeautifulSoup(req.text, 'html.parser')
    summary = html.find('div', {'class': 'wprm-recipe-summary'}).find('span').get_text()
    return summary

# to get all data from a recipe based on specific recipe link
def get_recipe(link):
    """
    Get recipe data from a link
    
    Args:
        link (str): list of links to scrap 
    Return:
        dict: Dictionary with recipe data (name, image, 
        ingredients, price, instructions, summary)
    """
    
    scraper = scrape_me(link)
    name = scraper.title()
    image = scraper.image()
    ingredients = scraper.ingredients()
    instructions = scraper.instructions_list()
    try: 
        price = scraper.total_time()
    except: 
        price = ''
    
    try:
        time.sleep(5) 
        summary = get_summary(link)
    except:
        summary = 'Oops, no summary available'
        
    recipe = {
        "name" : name,
        "image": image,
        "ingredients": ingredients,
        "price": price,
        "instructions": instructions,
        "summary": summary
    }
    
    return recipe

# to get all recipes and their information from a category
def get_recipe_data_by_interval(category, links, start, end):
    """
    Extract recipes from links of a certain category from bowlsofdelicius.com.

    Args:
        category (str): type of recipes (breakfast, lunch or dinner)
        links (list[str]): list of links to scrap
        start (int): start index of links to scrap recipe data
        end (int): end index of links to scrap recipe data
    Return:
        list[dicts]: List of recipes
    """
    recipes = []
    
    for link in links[start:end]:
        recipe = get_recipe(link)
        recipe['category'] = category
        recipes.append(recipe)
        time.sleep(5)
        
    return recipes

