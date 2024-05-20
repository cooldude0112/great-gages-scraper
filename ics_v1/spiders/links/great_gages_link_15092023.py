# import json
# import pymysql
# import scrapy
# from scrapy.cmdline import execute
#
# from ics_v1.items import IcsV1SiteMapLinksItem
# import ics_v1.db_config as db
#
# head={
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#         }
#
# class WalkerIndustrialLinksSpider(scrapy.Spider):
#     name ='great_links_new_1509'
#
#     start_urls = ['https://www.greatgages.com/']
#     VENDOR_ID = "ACT-B2-002"
#     VENDOR_NAME = "Great Gages"
#
#
#
#
#     def __init__(self, name=None, **kwargs):
#         super().__init__(name, **kwargs)
#         # DATABASE CONNECTION
#         self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
#         self.cursor = self.con.cursor()
#
#     def start_requests(self):
#
#
#         url = "https://www.greatgages.com/collections/gages"
#
#         payload = {}
#         headers = {
#             'Cookie': '_cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22merchant_geo%22%3A%22US%22%2C%22sale_of_data_region%22%3Afalse%7D; _landing_page=%2F; _orig_referrer=; _s=9d9b9b52-cb8c-4691-a2be-cd0e1a793d08; _shopify_s=9d9b9b52-cb8c-4691-a2be-cd0e1a793d08; _shopify_y=1144896c-48fa-4f67-b9a1-435d9cf4ef8d; _y=1144896c-48fa-4f67-b9a1-435d9cf4ef8d; cart_currency=USD; localization=US; secure_customer_sig='
#         }
#         # response = requests.request("POST", url, headers=headers, data=payload)
#         yield scrapy.Request(url=url,callback=self.parse,headers=headers )
#
#     def parse(self, response, **kwargs):
#         cat_loop=response.xpath("//div[@class='wrapper']//ul[contains(@id,'AccessibleNav')]/li[contains(@class,'site-nav--has-dropdown')]")
#         cat_number = 1
#         for ij in cat_loop:
#             cat_number += 1
#             path_dict1={}
#             lev_1_name=ij.xpath('./a/text()').get('').strip()
#             lev_1_url=ij.xpath('./a/@href').get()
#             print("*********LEVEL 1*********",lev_1_url)
#             if lev_1_url:
#                 if 'http' not in lev_1_url:
#                     lev_1_url = 'https://www.greatgages.com' + lev_1_url
#                 else:
#                     lev_1_url =  lev_1_url
#             path_dict1['name']=lev_1_name
#             path_dict1['url']=lev_1_url
#             cat_loop2 = ij.xpath("./ul[contains(@id,'MenuParent')]/li")
#             if cat_loop2:
#                 last_cat = 0
#                 for cat_list2 in cat_loop2:
#                     cat_list_second = []
#                     cat_list = []
#                     cat_list.append(path_dict1)
#
#                     last_cat += 1
#                     path_dict2 = {}
#                     lev_2_name = cat_list2.xpath('.//a/text()').get('').strip()
#                     lev_2_url = cat_list2.xpath('.//a/@href').get()
#                     if lev_2_url:
#                         if 'http' not in lev_2_url:
#                             lev_2_url = 'https://www.greatgages.com' + lev_2_url
#                         else:
#                             lev_2_url = lev_2_url
#                         path_dict2['name'] = lev_2_name
#                         path_dict2['url'] = lev_2_url
#                         cat_list_second.append(path_dict1)
#                         cat_list_second.append(path_dict2)
#                         print("2",path_dict2)
#                         req_url_1 = cat_list_second[-1]['url']
#                         ab = f"{str(cat_number)}-{str(last_cat)}"
#                         cat_loop3 = cat_loop2.xpath(f"./ul[@id='MenuChildren-{ab}']/li")
#                         if cat_loop3:
#                             for cat_list3 in cat_loop3:
#                                 cat_list_final= []
#                                 path_dict3 = {}
#                                 lev_3_name = cat_list3.xpath('.//a/text()').get('').strip()
#                                 lev_3_url = cat_list3.xpath('.//a/@href').get()
#                                 if lev_3_url:
#                                     if 'http' not in lev_3_url:
#                                         lev_3_url = 'https://www.greatgages.com' + lev_3_url
#                                     else:
#                                         lev_3_url = lev_3_url
#                                     path_dict3['name'] = lev_3_name
#                                     path_dict3['url'] = lev_3_url
#                                     print(path_dict3)
#                                     cat_list_final.append(path_dict1)
#                                     cat_list_final.append(path_dict2)
#                                     cat_list_final.append(path_dict3)
#                                     req_url = cat_list_final[-1]['url']
#                                     # print("^^^^^",req_url)
#                                     yield scrapy.Request(url=req_url, headers=head, callback=self.product_url,
#                                                          meta={'cat_list': cat_list_final})
#                         else:
#                             # print("%%%%%",req_url_1)
#                             yield scrapy.Request(url=req_url_1, headers=head, callback=self.product_url,
#                                                  meta={'cat_list': cat_list_second})
#
#     def product_url(self, response, **kwargs):
#         cat_list = response.meta['cat_list']
#         p_page_he = response.xpath("//div[@data-label='Collection Toolbar']//div[@class='gf_collection-tool gf_product-quantity-wrapper']")
#         # print("!!!!!",p_page_he)
#         if p_page_he:
#             product_xpath = response.xpath("//div[@data-label='Product List']//div[@data-label='Product']//div[@class='module-wrap']//h3//a")
#             # print(product_xpath)
#             for product in product_xpath:
#                 item = IcsV1SiteMapLinksItem()
#                 product_link = product.xpath(".//@href").get()
#                 item['product_urls'] = 'https://www.greatgages.com' + product_link
#                 # print("#$$$$",item['product_urls'])
#                 item['meta_data'] = json.dumps(cat_list, ensure_ascii=False)
#                 item['vendor_id'] = self.VENDOR_ID
#                 item['vendor_name'] = self.VENDOR_NAME
#                 yield item
#             next_page_path = response.xpath("//div[@class='gf_collection-paginator-wrapper']//span[@class='next']/a/@href").get()
#             if next_page_path:
#                 if "https://www.greatgages.com/" not in next_page_path:
#                     next_page_path = "https://www.greatgages.com/" + next_page_path
#                 yield scrapy.Request(url=next_page_path, callback=self.product_url, meta={'cat_list': cat_list})
#
#
# if __name__ == '__main__':
#     execute("scrapy crawl great_links_new_1509".split())
#
#
#
