from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from re import sub
import os


def get_categories():
    """
    Esta funcion hace un scrapping simple de la pagina de blog de Xepelin para obtener las categorias posibles

    Parameters:
    - None.

    Returns:
    - dict: cada key es una categoria con su url correspondiente.
    """
    url = "https://xepelin.com/blog"
    html = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    navbar = soup.find_all("ul", class_="Navbar_navbarList__S4cAF")[0]
    categories = {}
    for element in navbar:
        for sub in element:
            categories[sub.text.lower()] = sub['href']
    return categories


def scrape(url):
    """
    Esta funcion obtione el url de cada post en el blog y los visita uno a uno para hacer un scrapping de c/u.

    Parameters:
    - url (string): direccion web de la pagina del blog a scrappear.

    Returns:
    - list: lista de diccionarios con los valores obtenidos del scrapping.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    print('Loading...')
    driver.get(url)

    search_for_button = True
    wait = 5
    while search_for_button:
        print('Now we wait')
        time.sleep(wait)
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        print('We have the buttons :)')
        search_for_button = False
        for b in buttons:
            print(f"Button: {b.text}")
            if b.text.strip() == 'Cargar más':
                b.click()
                print('CLICK!')
                search_for_button = True
                time.sleep(wait)

    parent = driver.find_element(By.CLASS_NAME, 'BlogArticlesPagination_articlesGridNormal__CYdsq')
    children = parent.find_elements(By.TAG_NAME, 'a')
    urls = [child.get_attribute('href') for child in children]
    results = []
    for url in urls:
        print(url)
        driver.get(url)
        title_element = driver.find_element(By.TAG_NAME, 'h1')
        wrapper = driver.find_element(By.CLASS_NAME, 'ArticleSingle_wrapper__Mm4hH')
        divs = wrapper.find_elements(By.XPATH, './*')
        category_element = divs[0].find_element(By.TAG_NAME, 'div')
        author_element = driver.find_element(By.CSS_SELECTOR, '.sc-fe594033-0.ioYqnu.Text_bodySmall__wdsbZ')
        time_element = driver.find_element(By.CSS_SELECTOR, '.sc-fe594033-0.ioYqnu.text-grey-600.Text_body__ldD0k')
        content = {'title': title_element.text,
                   'category': category_element.text,
                   'author': author_element.text,
                   'time': sub(r'\D', '', time_element.text),
                   'url': url
                   }
        results.append(content)
    driver.quit()
    return results
