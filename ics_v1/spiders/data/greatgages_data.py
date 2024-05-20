# import hashlib
# import html
# import json
# import os.path
# import re
# from datetime import datetime
#
# import pymysql
# import scrapy
# from itemloaders import ItemLoader
# from itemloaders.processors import TakeFirst
# from parsel import Selector
# from scrapy.cmdline import execute
#
# import ics_v1.db_config as db
# from ics_v1.items import IcsV1AssetItem, IcsV1PricingItem, IcsV1PDPItem
#
# def check_status(x):
#     return True if x else False
#
# class GreatgagesDataSpider(scrapy.Spider):
#     name = "greatgages_data"
#     allowed_domains = ["'greategages.com"]
#     start_urls = ["https://www.greatgages.com/"]
#     VENDOR_ID = "ACT-B2-002"
#     VENDOR_NAME = "Great Gages"
#
#     page_save = 'D:/Work_great/Actowiz/pages/ics/htmls/' + VENDOR_ID + "-" + VENDOR_NAME + "/"
#
#     data = list()
#
#     def __init__(self, name=None, start=1, end=1,**kwargs):
#         super().__init__(name, **kwargs)
#         # DATABASE CONNECTION
#         self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
#         self.cursor = self.con.cursor()
#         if not os.path.exists(self.page_save):
#             os.makedirs(self.page_save)
#         self.start=start
#         self.end=end
#
#
#     def start_requests(self):
#
#         select_query = [
#             f"select id, product_urls,meta_data from {db.sitemap_table} where",
#             f"vendor_id = '{self.VENDOR_ID}' and ",
#             f"status = 'pending' and ",
#             f"id between {self.start} and {self.end}"
#         ]
#
#         self.cursor.execute(" ".join(select_query))
#
#         for data in self.cursor.fetchall():
#         # li1=["https://www.greatgages.com/collections/data-collection/products/500-171-30-caliper-to-pc-interface-package-usb-direct"]
#         # li1=["https://www.greatgages.com/collections/microridge-mobilecollect/products/mc-d-05cza662-x-mobile-collect-cable?variant=6030089475"]
#         # li1=["https://www.greatgages.com/collections/barcode-scanners/products/wireless-laser-barcode-scanner-1d"]
#         # for i in li1:
#         #     url=i
#             # url="https://www.greatgages.com/collections/data-collection/products/500-171-30-caliper-to-pc-interface-package-usb-direct"
#             # url = "https://www.greatgages.com/collections/microridge-mobilecollect/products/mc-d-05cza662-x-mobile-collect-cable?variant=6030089475"
#             # url="https://www.greatgages.com/collections/standard-metric-thread-plug-gages/products/vermont-standard-metric-thread-plug-gages-go-no-go-m22-0x1-50"
#             # url="https://www.greatgages.com/collections/barcode-scanners/products/wireless-laser-barcode-scanner-1d"
#             # url="https://www.greatgages.com/collections/microridge-mobilecollect/products/mc-d-05cza662-x-mobile-collect-cable?variant=6030089475"
#             meta_data=json.loads(data[2])
#             yield scrapy.Request(
#                 url=data[1],
#                 meta={'meta_data':meta_data},
#                 # url = 'https://www.greatgages.com/collections/mitutoyo-indicators-with-calibration-cert/products/2416scal-mitutoyo-dial-indicator-1-range-001-grad-with-cal-cert',
#                 # url="https://www.fastener-express.com/2-56x3/16FlatHeadCapScrews18-8StainlessBlackOxide6lobeQty.aspx",
#                 cb_kwargs={
#                     "id": data[0]
#                 }
#             )
#
#
#     def parse(self, response,**kwargs):
#         meta_data = response.meta.get("meta_data")
#         hash_key = hashlib.sha256(response.url.encode()).hexdigest()
#         # id = kwargs['id']
#         # open(self.page_save + str(id) + ".html", "wb").write(response.body)
#         # print(response.text)
#
#         # if vari:
#         #     for i in vari:
#         #
#         #         product_name = product_name + " " + i
#         #         break
#
#
#
#         qty = 1
#         uom = None
#
#         # product_loader = ItemLoader(item=IcsV1PDPItem(), selector=response)
#         # product_loader.default_output_processor = TakeFirst()
#
#         # SETTING VALUES
#         # product_name = response.xpath("//div[@class='grid-item large--three-fifths']/h1[@class='h2']/text()").get()
#         # vari = response.xpath("//div[@class='product-description rte']//ul//li/strong/text()").getall()
#
#
#         # product_loader.add_value('hash_key', hash_key)
#         # product_loader.add_value('pdp_url', response.url)
#
#         # product_loader.add_value('name', product_name)
#
#         # product_loader.add_value('sku', sku)
#         # category = []
#         # cat_01_name = response.xpath("//nav[@class='breadcrumb']//a[2]//text()").get()
#         # cat01_url=response.xpath("//nav[@class='breadcrumb']//a[2]/@href").get()
#         # cat_01_url="https://www.greatgages.com" + cat01_url
#         # category.append(cat_01_name)
#         # category.append(product_name)
#         # print(category)
#
#         # product_loader.add_value('category', category)
#         # product_loader.replace_value('category', json.dumps(product_loader.get_collected_values('category')),ensure_ascii = False)
#         # in_stock = response.xpath("//div[@class='payment-buttons payment-buttons--small']//span[@id='addToCartText-product-template']/text()")
#         # product_loader.add_xpath('in_stock', "//div[@class='payment-buttons payment-buttons--small']//span[@id='addToCartText-product-template']/text()", check_status)
#         # product_loader.add_xpath('available_to_checkout', "//div[@class='payment-buttons payment-buttons--small']//span[@id='addToCartText-product-template']/text()", check_status)
#
#         # product_loader.add_xpath('description', "//div[@class='product-description rte']/p/strong/text()")
#         # des_p = response.xpath("//div[@class='product-description rte']/p[not(./a)]//text()").getall()
#         # des_p = response.xpath("//div[@class='product-description rte']/p[not(./a)]//text()|//div[@class='product-description rte']//ul/li/text()|//div[@class='product-description rte']//h3//text()|//div[@class='product-description rte']//h4//text()").getall()
#
#
#         # product_loader.add_value('description'," ".join(des_p).strip())
#         # product_loader.replace_value(
#         #     'description', " ".join(product_loader.get_collected_values(des_p)).strip()
#         # )
#
#
#         # product_loader.add_xpath('description_html', "//div[@class='product-description rte']//p/strong")
#         # des_h = response.xpath("//div[@class='product-description rte']/p[not(./a)]").getall()
#         # des_h = response.xpath("//div[@class='product-description rte']/p[not(./a)]|//div[@class='product-description rte']//ul/li|//div[@class='product-description rte']//h3|//div[@class='product-description rte']//h4").getall()
#         #
#         #
#         #
#         # product_loader.add_value('description_html'," ".join(des_h).strip())
#
#         # product_loader.add_value('description_html', des_h)
#
#         # scrape_metadata = dict()
#         # scrape_metadata['url'] = response.url
#         # scrape_metadata['date_visited'] = str(datetime.now()).replace(" ", "T")[:-3] + "Z"
#         #
#         # breadcrumbs = list()
#         # dic_home={"name":"Home",
#         #           "url":"https://www.greatgages.com/"
#         # }
#         # # dic1={"name":cat_01_name,
#         # #       "url":cat_01_url}
#         # dic2={
#         #     "name":product_name,
#         #     "url":response.url}
#         # cat02_url="https://www.greatgages.com/" + response.xpath("//nav[@class='breadcrumb']/span/following-sibling::a/@href").get()
#         # cat02_name=response.xpath("//nav[@class='breadcrumb']/span/following-sibling::a/text()").get()
#         # dic02={
#         #     "name":cat02_name,
#         #     "url":cat02_url
#         # }
#         #
#         # breadcrumbs.append(dic_home)
#         # if len(meta_data)==2:
#         #     for i in meta_data[:1]:
#         #         breadcrumbs.append(i)
#         #     # breadcrumbs.append(dic1)
#         #     breadcrumbs.append(dic02)
#         #     breadcrumbs.append(dic2)
#         # else:
#         #     for i in meta_data[:2]:
#         #         breadcrumbs.append(i)
#         #     breadcrumbs.append(dic02)
#         #     breadcrumbs.append(dic2)
#         # category=[]
#         # for i in breadcrumbs[1:]:
#         #     category.append(i['name'])
#         # category.pop()
#         # product_loader.add_value('category', category)
#         # product_loader.replace_value('category', json.dumps(product_loader.get_collected_values('category')),ensure_ascii = False)
#         #
#         #
#         #
#         # scrape_metadata['breadcrumbs'] = breadcrumbs
#         # product_loader.add_value('_scrape_metadata', json.dumps(scrape_metadata))
#         # product_loader.add_value('status', 'Done')
#
#         # yield product_loader.load_item()
#
#         # data_extra = ItemLoader(item=IcsV1PDPItem(), selector=response)
#         # data_extra.default_output_processor = TakeFirst()
#         ab = response.text
#
#         abc = ab.split("var meta = ")[-1]
#         abcd = abc.split(";")[0]
#         Data = json.loads(abcd)
#         for i in Data['product']['variants']:
#             id = kwargs['id']
#             product_loader = ItemLoader(item=IcsV1PDPItem(), selector=response)
#             product_loader.default_output_processor = TakeFirst()
#             product_loader.add_value('id', id)
#             product_loader.add_value('vendor_id', self.VENDOR_ID)
#             product_loader.add_value('vendor_name', self.VENDOR_NAME)
#             product_loader.add_xpath('in_stock',
#                                      "//div[@class='payment-buttons payment-buttons--small']//span[@id='addToCartText-product-template']/text()",
#                                      check_status)
#             product_loader.add_xpath('available_to_checkout',
#                                      "//div[@class='payment-buttons payment-buttons--small']//span[@id='addToCartText-product-template']/text()",
#                                      check_status)
#             # this is only 5 url not get des---------------
#             # des_p = response.xpath(
#             #     "//div[@class='product-description rte']/p[not(./a)]//text()|//div[@class='product-description rte']//ul/li/text()|//div[@class='product-description rte']//h3//text()|//div[@class='product-description rte']//h4//text()").getall()
#             des_p = response.xpath("//div[@class='product-description rte']//text()").getall()
#
#             # -------------------------------------------------
#             # des_p = response.xpath("//div[@class='product-description rte']/text()").getall()
#             product_loader.add_value('description', " ".join(des_p).strip())
# # --------------------------------------------------------------------des_h only 5 url error
# #             des_h = response.xpath(
# #                 "//div[@class='product-description rte']/p[not(./a)]|//div[@class='product-description rte']//ul/li|//div[@class='product-description rte']//h3|//div[@class='product-description rte']//h4").getall()
#             des_h = response.xpath("//div[@class='product-description rte']").getall()
# # -----------------------------------------------------------------
#             # des_h = response.xpath("//div[@class='product-description rte']").getall()
#             product_loader.add_value('description_html', " ".join(des_h).strip())
#             sku = i['sku']
#             varint = i['id']
#             p_name = i['name']
#             price = i['price']
#             # print(price)
#             v_name = i['public_title']
#             if v_name:
#                 if v_name not in p_name:
#                     product_name = p_name + v_name
#                     product_url = response.url + "?variant=" + str(varint)
#                     product_loader.add_value('pdp_url', product_url)
#                 else:
#                     product_name = p_name
#                     product_url = response.url + "?variant=" + str(varint)
#                     product_loader.add_value('pdp_url', product_url)
#
#
#
#             else:
#                 product_name = p_name
#                 product_url = response.url
#                 product_loader.add_value('pdp_url', product_url)
#
#             product_loader.replace_value('name', product_name)
#
#             # product_url = response.url + "?variant=" + str(varint)
#             hash_key = hashlib.sha256(product_url.encode()).hexdigest()
#             open(self.page_save + str(hash_key) + ".html", "wb").write(response.body)
#
#             product_loader.add_value('hash_key', hash_key)
#
#             product_loader.add_value('sku', sku)
#
#             scrape_metadata = dict()
#             scrape_metadata['url'] = response.url
#             scrape_metadata['date_visited'] = str(datetime.now()).replace(" ", "T")[:-3] + "Z"
#
#             breadcrumbs = list()
#             dic_home = {"url": "https://www.greatgages.com/",
#                         "name": "Home"
#
#                         }
#             # dic1={"name":cat_01_name,
#             #       "url":cat_01_url}
#             # --------------------------------------------------
#             # dic2 = {
#             #     "name": product_name,
#             #     "url": response.url}
#             # cat02_url = "https://www.greatgages.com/" + response.xpath("//nav[@class='breadcrumb']/span/following-sibling::a/@href").get()
#             # cat02_name = response.xpath("//nav[@class='breadcrumb']/span/following-sibling::a/text()").get()
#             # dic02 = {
#             #     "name": cat02_name,
#             #     "url": cat02_url
#             # }
# # ---------------------------------------------------
#             breadcrumbs.append(dic_home)
#             for cat_b in meta_data:
#                 breadcrumbs.append(cat_b)
#
#             # if len(meta_data) == 2:
#             #     for i in meta_data[:1]:
#             #         breadcrumbs.append(i)
#             #     # breadcrumbs.append(dic1)
#             #     breadcrumbs.append(dic02)
#             #     breadcrumbs.append(dic2)
#             # else:
#             #     for i in meta_data[:2]:
#             #         breadcrumbs.append(i)
#             #     breadcrumbs.append(dic02)
#             #     breadcrumbs.append(dic2)
#             category = []
#             for i in breadcrumbs[1:]:
#                 category.append(i['name'])
#             # category.pop()
#             product_loader.add_value('category', category)
#             product_loader.replace_value('category', json.dumps(product_loader.get_collected_values('category')),
#                                          ensure_ascii=False)
#
#             scrape_metadata['breadcrumbs'] = breadcrumbs
#             product_loader.add_value('_scrape_metadata', json.dumps(scrape_metadata))
#
#
#             # product_loader.add_value('_scrape_metadata', json.dumps(scrape_metadata))
#             product_loader.add_value('status', 'Done')
#             yield product_loader.load_item()
#
#             # print(product_url)
#             # print(sku)
#         # if vari:
#         #     for i in vari:
#         #         # product_item=ItemLoader.copy()
#         #         product_name = product_name + " " + i
#         #         product_loader.replace_value('name', product_name)
#         #         yield product_loader.load_item()
#         # else:
#         #     product_name=product_name
#         #     product_loader.replace_value('name', product_name)
#         #     yield product_loader.load_item()
#
#
#
#         # EXTRACTING PRICES
#         #
#             sku=sku
#             pricing_loaders = ItemLoader(item=IcsV1PricingItem(), selector=response)
#             pricing_loaders.default_output_processor = TakeFirst()
#             pricing_loaders.add_value('vendor_id', self.VENDOR_ID)
#             pricing_loaders.add_value('sku', sku)
#             pricing_loaders.add_value('hash_key', hash_key)
#             pricing_loaders.add_value('currency', "USD")
#             pricing_loaders.add_value('min_qty', qty)
#             #
#             # price_m=response.xpath("//span[@id='productPrice-product-template']//span[@aria-hidden='true']/text()").get()
#             # if not price_m:
#             #     price_m = response.xpath("//span[@id='productPrice-product-template']//small[@aria-hidden='true']/text()").get()
#             # #
#             # price_b=response.xpath("//span[@id='productPrice-product-template']//span[@aria-hidden='true']/sup/text()").get()
#             # if not price_b:
#             #     price_b=response.xpath("//span[@id='productPrice-product-template']//small[@aria-hidden='true']/sup/text()").get()
#             # price_a=price_m[1:]
#             # ab_price= price_a + "." + price_b
#             # price = (ab_price)
#             price = price/100
#             price = str(price)
#             pricing_loaders.add_value('price', price)
#
#             yield pricing_loaders.load_item()
#
#             #
#             # # ASSET STORING
#             item = IcsV1AssetItem()
#             item['vendor_id'] = self.VENDOR_ID
#             # item['sku'] = product_sku
#             item['hash_key'] = hash_key
#             item['sku']=sku
#
#             product_image = response.xpath("//div[@class='grid-item large--eleven-twelfths text-center']/ul/li/a/@href").getall()
#             # product_image01 = response.xpath("//div[@class='no-js product__image-wrapper image-zoom']/img[@class='zoomImg']/@src").getall()
#             product_image01 = response.xpath("//div[@class='no-js product__image-wrapper']/img/@src").get()
#             try:
#                 if len(product_image)>0:
#                     for index, images in enumerate(product_image):
#                         image_item = item.copy()
#                         if not index:
#                             image_item['is_main_image'] = True
#
#                         image_item['source'] = response.urljoin(images.replace("\\", "/"))
#                         image_item['file_name'] = image_item['source'].split("?")[0].split("/")[-1]
#                         image_item['type'] = 'image/product'
#
#
#
#                         yield image_item
#                 else:
#                     # product_image01=response.xpath("//div[@class='no-js product__image-wrapper image-zoom']/img[@class='zoomImg']/@src").getall()
#                     image_item = item.copy()
#                     image_item['is_main_image'] = True
#                     image_item['source'] = "https:"+ product_image01
#                     image_item['file_name'] = image_item['source'].split("?")[0].split("/")[-1]
#                     image_item['type'] = 'image/product'
#
#                     yield image_item
#             except:
#                 print('---------')
#             # pdf_link = response.xpath("//div[@class='product-description rte']//p/img/@src").get()
#             d_img = response.xpath("//div[@class='product-description rte']//img/@src").getall()
#             if len(d_img)>0:
#                 for index, images in enumerate(d_img):
#                     source_c = response.urljoin(images.replace("\\", "/"))
#                     if "pdf" in source_c:
#                         image_item['source']=response.xpath("//div[@class='product-description rte']//a/@href").get()
#                         image_item['file_name'] = response.xpath("//div[@class='product-description rte']//a/@href").get().split(".com/")[1]
#                         image_item['type'] = 'document'
#                         image_item['is_main_image'] = False
#                     else:
#                         image_item['source'] = response.urljoin(images.replace("\\", "/"))
#                         image_item['file_name'] = image_item['source'].split("?")[0].split("/")[-1]
#                         image_item['type'] = 'image'
#                         image_item['is_main_image'] = False
#
#                     yield image_item
#
#
#         #
#
#         # if product_image and product_image[0].endswith('FE-logo-small.jpg'):
#         #     return None
# if __name__ == '__main__':
#     execute("scrapy crawl greatgages_data -a start=1 -a end=10".split())