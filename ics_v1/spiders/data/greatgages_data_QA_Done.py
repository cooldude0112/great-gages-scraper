import hashlib
import json
import os.path
from datetime import datetime
import pymysql
import scrapy
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst
# from lxml.html import open_in_browser
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser

import ics_v1.db_config as db
from ics_v1.items import IcsV1AssetItem, IcsV1PricingItem, IcsV1PDPItem

# Open the URL in the default web browser (usually Chrome)
# webbrowser.open(url)

# Function to check the status
def check_status(x):
    return True if x else False

# Spider class definition
class GreatgagesDataSpider(scrapy.Spider):
    name = "greatgages_data"
    allowed_domains = ["'greategages.com"]
    start_urls = ["https://www.greatgages.com/"]
    VENDOR_ID = "ACT-B2-002"
    VENDOR_NAME = "Great Gages"
    handle_httpstatus_list = [500,404]
    page_save = 'C:/Work/Actowiz/pages/ics/htmls/' + VENDOR_ID + "-" + VENDOR_NAME + "/"

    data = list()
    # Constructor
    def __init__(self, name=None, start=1, end=1,**kwargs):
        super().__init__(name, **kwargs)
        # DATABASE CONNECTION
        self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
        self.cursor = self.con.cursor()
        if not os.path.exists(self.page_save):
            os.makedirs(self.page_save)
        self.start=start
        self.end=end

    # Start requests method
    def start_requests(self):
        select_query = [
            f"select id, product_urls,meta_data from {db.sitemap_table} where",
            f"vendor_id = '{self.VENDOR_ID}' and ",
            f"status = 'pending' and ",
            f"id between {self.start} and {self.end}"
        ]
        self.cursor.execute(" ".join(select_query))
        for data in self.cursor.fetchall():
            meta_data=json.loads(data[2])
            # Yielding requests with metadata
            yield scrapy.Request(
                url=data[1],
                meta={'meta_data':meta_data},
                cb_kwargs={
                    "id": data[0],
                    "url" : data[1]
                }
            )

    def parse(self, response,**kwargs):
        # Check if the response status is 404 (Page Not Found)
        if response.status == 404:
            # Update status in the database to "NOT FOUND" for the URL that returned 404
            qry = f'update {db.sitemap_table} set status = "NOT FOUND" where product_urls ="{response.url}"'
            self.cursor.execute(qry)
            self.con.commit()
        # Extract metadata from the response
        meta_data = response.meta.get("meta_data")
        qty = 1
        # open_in_browser(response)
        # Get the response body as text
        res_text = response.text
        # Extract relevant JSON data from the response text
        json_search = res_text.split("var meta = ")[-1]
        json_find = json_search.split(";")[0]
        json_Data = json.loads(json_find)
        # Iterate over product variants in the JSON data
        for data in json_Data['product']['variants']:
            id = kwargs['id']
            product_loader = ItemLoader(item=IcsV1PDPItem(), selector=response)
            product_loader.default_output_processor = TakeFirst()
            # Add common attributes to the product loader
            product_loader.add_value('id', id)
            product_loader.add_value('vendor_id', self.VENDOR_ID)
            product_loader.add_value('vendor_name', self.VENDOR_NAME)
            # Extract in-stock and available-to-checkout information from the response
            product_loader.add_xpath('in_stock',"//div[@class='module-wrap']//button[@type='submit']/span[@class='AddToCartText']//text()",check_status)
            product_loader.add_xpath('available_to_checkout',"//div[@class='module-wrap']//button[@type='submit']/span[@class='AddToCartText']//text()",check_status)
            # Extract in-stock and available-to-checkout information from the response
            des_p = response.xpath("//div[@class='module']//div[contains(@class,'gf_product-desc gf_gs-text-paragraph-1')]//text()").getall()
            product_loader.add_value('description', " ".join(des_p).strip())
            des_h = response.xpath("//div[@class='module']//div[contains(@class,'gf_product-desc gf_gs-text-paragraph-1')]").getall()
            product_loader.add_value('description_html', " ".join(des_h).strip())
            # Extract product details from the variant
            sku = data['sku']
            varint = data['id']
            p_name = data['name']
            price = data['price']
            v_name = data['public_title']
            # Determine the product name and URL based on variant information
            if v_name:
                if v_name not in p_name:
                    product_name = p_name + v_name
                    product_url = response.url + "?variant=" + str(varint)
                    product_loader.add_value('pdp_url', product_url)
                else:
                    product_name = p_name
                    product_url = response.url + "?variant=" + str(varint)
                    product_loader.add_value('pdp_url', product_url)
            else:
                product_name = p_name
                product_url = response.url
                product_loader.add_value('pdp_url', product_url)
            product_loader.replace_value('name', product_name)

            # product_url = response.url + "?variant=" + str(varint)
            # the hash key for the product URL
            hash_key = hashlib.sha256(product_url.encode()).hexdigest()
            open(self.page_save + str(hash_key) + ".html", "wb").write(response.body)

            product_loader.add_value('hash_key', hash_key)
            product_loader.add_value('sku', sku)

            # Create metadata for the product
            scrape_metadata = dict()
            scrape_metadata['url'] = response.url
            scrape_metadata['date_visited'] = str(datetime.now()).replace(" ", "T")[:-3] + "Z"
            # Construct breadcrumbs for the product
            breadcrumbs = list()
            dic_home = {"url": "https://www.greatgages.com/",
                        "name": "Home"
                        }
# ---------------------------------------------------
            breadcrumbs.append(dic_home)
            for cat_b in meta_data:
                breadcrumbs.append(cat_b)
            # Extract category information from breadcrumbs
            category = []
            for i in breadcrumbs[1:]:
                category.append(i['name'])
            # category.pop()
            product_loader.add_value('category', category)
            product_loader.replace_value('category', json.dumps(product_loader.get_collected_values('category')),
                                         ensure_ascii=False)

            scrape_metadata['breadcrumbs'] = breadcrumbs
            product_loader.add_value('_scrape_metadata', json.dumps(scrape_metadata))
            product_loader.add_value('status', 'Done')
            yield product_loader.load_item()

            # EXTRACTING PRICES
            # Assign the SKU value to a variable (already commented)
            sku=sku
            # Create a new ItemLoader for pricing information
            pricing_loaders = ItemLoader(item=IcsV1PricingItem(), selector=response)
            pricing_loaders.default_output_processor = TakeFirst()
            # Add values to the pricing loader
            pricing_loaders.add_value('vendor_id', self.VENDOR_ID)
            pricing_loaders.add_value('sku', sku)
            pricing_loaders.add_value('hash_key', hash_key)
            pricing_loaders.add_value('currency', "USD")
            pricing_loaders.add_value('min_qty', qty)
            # Convert price to decimal format (assuming price is in cents)
            price = price/100
            price = str(price)
            # Add the price to the pricing loader
            pricing_loaders.add_value('price', price)
            # Add the price to the pricing loader
            yield pricing_loaders.load_item()


            # ASSET STORING
            # Create a new instance of IcsV1AssetItem
            item = IcsV1AssetItem()
            item['vendor_id'] = self.VENDOR_ID # Set vendor ID for the item
            item['hash_key'] = hash_key # Set hash key for the item
            item['sku']=sku # Set SKU for the item

            # Extract product images from the response
            product_image = response.xpath("//div[contains(@class,'module gf_module-left gf_module-left-lg gf_module--md gf_module--sm gf_module--xs  style-slider')]//div//img/@src").getall()
            # Process product images
            try:
                if len(product_image)>0:
                    for index, images in enumerate(product_image):
                        # Create a copy of the item for each image
                        image_item = item.copy()
                        # Determine if the image is the main image
                        if not index:
                            image_item['is_main_image'] = True
                        # Check if the image URL starts with 'https:'
                        if 'https:' not in images:
                            image_item['source'] = 'https:' + images
                        else:
                            image_item['source'] = images
                        # Extract the file name from the image URL
                        image_item['file_name'] = image_item['source'].split("?")[0].split("/")[-1]
                        # Set the type of the item as 'image/product'
                        image_item['type'] = 'image/product'
                        # Yield the image item
                        yield image_item
            except:
                print('---------')

            # Extract product-related images from the description
            d_img = response.xpath("//div[@class='module']//div[contains(@class,'gf_product-desc gf_gs-text-paragraph-1')]//img/@src").getall()
            # Process product-related images
            if len(d_img)>0:
                for index, images in enumerate(d_img):
                    # Check if the image URL starts with 'https:'
                    if 'https:' not in images:
                        source_c = 'https:' + images
                    else:
                        source_c = images
                    # Check if the image is a document or regular image
                    if '//cdn.shopify.com/s/files/1/0891/2526/files/pdf' in source_c:
                        # Extract the PDF link and its name from the description
                        assets = response.xpath("//div[@class='module']//div[contains(@class,'gf_product-desc gf_gs-text-paragraph-1')]//a/@href").get()
                        asstes_name = response.xpath("//div[@class='module']//div[contains(@class,'gf_product-desc gf_gs-text-paragraph-1')]//a/@title").get().strip()
                        # Check if the asset URL starts with 'https:'
                        if 'https:' not in assets:
                            asset_url = 'https:' + assets
                        # Set attributes for the document item
                        image_item['source'] = asset_url
                        image_item['file_name'] = asstes_name
                        image_item['type'] = 'document'
                        image_item['is_main_image'] = False
                    else:
                        # Set attributes for regular images
                        image_item['source']=source_c
                        image_item['file_name'] = source_c.split('?')[1]
                        image_item['type'] = 'document'
                        image_item['is_main_image'] = False

                    yield image_item

if __name__ == '__main__':
    execute("scrapy crawl greatgages_data -a start=1 -a end=5900".split())