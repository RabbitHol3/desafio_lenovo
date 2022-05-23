from playwright.sync_api import sync_playwright
import os, sys

# SET ENVIRONMENT VARIABLES
os.environ['PWDEBUG'] = '1'

def check_url(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            self = args[0]
            url = self.base_url + argument
            if self.page.url != url:
                self.page.goto(url)            
            return function(*args, **kwargs)
        return wrapper
    return decorator


class Laptops:  
    url = '/test-sites/e-commerce/allinone/computers/laptops'
             
    def __init__(self, page, *args, **kwargs):        
        self.page = page
    
    def get_details(self, url):
        details = {}
        self.page.goto(url)
                
        div_details = self.page.locator('//div[@class="caption"]/parent::div/parent::div[@class="row"]')        
        price_field = div_details.locator('//h4[@class="pull-right price"]')
        
        details['url'] = url
        details['name'] = div_details.locator('//h4[not(@*)]').element_handle().inner_text()
        details['description'] = div_details.locator('//p[@class="description"]').inner_text()
        details['memory'] = div_details.locator('//label[@class="memory"]').inner_text().replace(':','')
        details['ratings'] = div_details.locator('//div[@class="ratings"]').inner_text().replace('reviews','').strip()
        
        # Capture price details
        swatches = div_details.locator('//div[@class="swatches"]/button').element_handles()
        # Click swatches detail, and get prices
        details['swatches'] = { s.inner_text(): price_field.inner_text() for s in swatches if not s.click() }
           
        return details
    
    @check_url(url)
    def list_laptops(self):
        products = self.page.locator('//a[@class="title"]')
        if not products.count():
            return []
        urls = [ self.base_url + p.get_attribute('href') for p in products.element_handles() if p.get_attribute('href')]
        details = [ self.get_details(url) for url in urls ]
        laptops = [ type('Laptop', (object,), detail) for detail in details ]
        return laptops
   
class Store(Laptops):
    base_url = 'https://webscraper.io'
    store_url = 'test-sites/e-commerce/allinone/'
    def __init__(self, page, *args, **kwargs):        
        super().__init__(page, *args, **kwargs)
        self.page = page
    
    @property
    def laptops(self):
        return self.list_laptops()
               
    

class _Laptops(Store):
    laptops_url = 'computers/laptops'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.laptops_url = self.store_url + self.laptops_url
    
    @check_url(laptops_url)
    def go_to_laptops(self):
        ...

class Robot:
    def __init__(self, *args, **kwargs):
        self.browser = None
        self.store = None
    
        
    def start(self):
        with sync_playwright() as p:
            # Start Chrome
            self.browser = p.chromium.launch() 
            self.page = self.browser.new_page()          
            self.store = Store(self.page)
        ...
        
        

process =  Robot()
process.start()

x.products()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.pause()
    page.goto("http://playwright.dev")
    print(page.title())
    page.pause()
    browser.close()