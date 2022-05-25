from playwright.sync_api import sync_playwright
import os, sys, django
from api.models import *
from django.utils import timezone


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
        print('Getting details for:', url)
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
        swatches = { s.inner_text(): price_field.inner_text() for s in swatches if not s.click() }
        
        # create product based on swatches
        
        products = []
        for k, v in swatches.items():            
            p = details.copy()
            p['size'] = k
            p['value'] = v
            products.append(p)
        
        return products
    
    @check_url(url)
    def list_laptops(self):
        products = self.page.locator('//a[@class="title"]')
        if not products.count():
            print('No products found')
            return []
        urls = [ self.base_url + p.get_attribute('href') for p in products.element_handles() if p.get_attribute('href')]
        print('Found {} products'.format(len(urls)))
        products = []
        for url in urls[:3]:
            products += self.get_details(url)               
        return products
   
class Store(Laptops):
    base_url = 'https://webscraper.io'
    store_url = 'test-sites/e-commerce/allinone/'
    def __init__(self, page, *args, **kwargs):        
        super().__init__(page, *args, **kwargs)
        self.page = page
    
    @property
    def laptops(self):
        return self.list_laptops()

class Robot:
    def __init__(self,robot_name, *args, **kwargs):
        self.browser = None
        self.store = None
        self.products = Product.objects        
        
    def start(self):
        
        with sync_playwright() as p:
            print('Starting browser')                    
            self.browser = p.chromium.launch()             
            self.page = self.browser.new_page()                      
            self.store = Store(self.page)      
            print('Getting laptops')      
            products = self.store.laptops
        
        prodcuts = [ Product(**p) for p in products ] 
        products_save = []       
        products_update = []
        #check products to be updated
        for p in prodcuts:
            try:
                products_update.append(
                    Product.objects.get(name=p.name, size=p.size, value=p.value)
                )                
            except Product.DoesNotExist:
                p.updated_at = timezone.now()
                products_save.append(p)
            except Product.MultipleObjectsReturned:
                print('Multiple objects returned: {}'.format(p.name))
        
        
        print('Saving {} products'.format(len(products_save)))
        Product.objects.bulk_create(products_save)
        print('Updating {} products'.format(len(products_update)))
        Product.objects.bulk_update(products_update, ['ratings', 'memory', 'description', 'url'])
        print('Done')
        
            

