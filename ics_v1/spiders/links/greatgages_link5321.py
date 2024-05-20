# import json
#   #QA DONE link spider
# import pymysql
# import scrapy
# from scrapy.cmdline import execute
#
# from ics_v1.items import IcsV1SiteMapLinksItem
# import ics_v1.db_config as db
#
# head={
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#
#         }
#
# class WalkerIndustrialLinksSpider(scrapy.Spider):
#     name ='great_links'
#
#     start_urls = ['https://www.greatgages.com/']
#     VENDOR_ID = "ACT-B2-002"
#     VENDOR_NAME = "Great Gages"
#
#
#
#     def __init__(self, name=None, **kwargs):
#         super().__init__(name, **kwargs)
#         # DATABASE CONNECTION
#         self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
#         self.cursor = self.con.cursor()
#
#     def parse(self, response, **kwargs):
#
#         #cat_loop=response.xpath("//nav[@class='nav-bar']//ul/li[@class='site-nav--has-dropdown ' and @aria-haspopup='true'] | //nav[@class='nav-bar']//ul/li[@class='site-nav--has-dropdown' and @aria-haspopup='true'] |//nav[@class='nav-bar']//ul/li[@class='site-nav--has-dropdown site-nav--active' and @aria-haspopup='true']")
#         cat_loop=response.xpath("//ul[@class='site-nav']/li[contains(@class,'site-nav--has-dropdown') and not(contains(@id,'moreMenu'))] | //ul[contains(@id,'moreMenu--list')]/li[contains(@class,'site-nav--has-dropdown')]")
#         c=0
#         for ij in cat_loop:
#             path_dict1={}
#             lev_1_name=ij.xpath('./a/text()').get('').strip()
#             lev_1_url=ij.xpath('./a/@href').get()
#             print("*********LEVEL 1*********",lev_1_url)
#             if  lev_1_url:
#                 if 'http' not in lev_1_url:
#                     lev_1_url = 'https://www.greatgages.com' + lev_1_url
#                 else:
#                     lev_1_url =  lev_1_url
#             path_dict1['name']=lev_1_name
#             path_dict1['url']=lev_1_url
#             # level_2=ij.xpath('.//ul[@class="site-nav--dropdown site-nav--has-grandchildren"]//li[contains(@class,"site-nav--has-dropdown site-nav--has-dropdown-grandchild")] | //ul[@class="site-nav--dropdown site-nav--has-grandchildren"]/li')
#             level_2=ij.xpath("./ul[contains(@id,'MenuParent')]/li")
#             if level_2:
#                 for kk in level_2:
#                     path_list1=[]
#                     lev_2_name=kk.xpath('./a/text()').get('').strip()
#                     lev_2_url=kk.xpath('./a/@href').get()
#                     if  lev_2_url:
#                         if 'http' not in lev_2_url:
#                              lev_2_url = 'https://www.greatgages.com' + lev_2_url
#                         else:
#                             lev_2_url = lev_2_url
#                         # lev_2_url='https://www.greatgages.com'+lev_2_url
#                     if lev_2_name and lev_1_name and not path_list1:
#                         path_dict2={}
#                         path_dict2['name']=lev_2_name
#                         path_dict2['url']=lev_2_url
#                         path_list1.append(path_dict1)
#                         path_list1.append(path_dict2)
#                         #print(path_list1)
#                         print(c,"**************************",lev_2_url)
#                         c+=1
#                         yield scrapy.Request(url=lev_2_url,headers=head,callback=self.cat_parse,meta={'path_list1':path_list1})
#
#
#
#     def cat_parse(self, response, **kwargs):
#         path_list1 = response.meta.get("path_list1")
#         loop_var=response.xpath('//div[@class="rte rte--header"]//table//td')
#         # container_loop = response.xpath('//div[@class="rte rte--header"]//h3//a | //p[@style="text-align: center;"]/a | //div[@style="text-align: center;"]/a[contains(@href,"collections")]')
#         container_loop = response.xpath("//img/parent::a")
#         pl_loop=response.xpath('//div[@class="grid-uniform"]//div/a')
#         if container_loop:
#             # path_list1 = response.meta.get("path_list1")
#             for ij in container_loop:
#                 # path_list2=[]
#                 # cat_nm=ij.xpath('.//h3//text()').get('').strip()
#                 ct_url=ij.xpath('./@href').get()
#                 if '-' in ct_url:
#                     cat_nm = ct_url.split('/')[-1].strip().replace('-',' ')
#                 else:
#                     cat_nm =ct_url.split('/')[-1].strip()
#                 if  ct_url:
#                     if 'http' not in ct_url:
#                         ct_url = 'https://www.greatgages.com' + ct_url
#                     else:
#                         ct_url = ct_url
#                     # ct_url = 'https://www.greatgages.com' + ct_url
#                     path_dict={}
#                     path_dict['name']=cat_nm.replace('\r','').replace('\n','').replace('\t','').strip()
#                     path_dict['url']=ct_url
#                     path_list2=path_list1[:]
#                     path_list2.append(path_dict)
#                     # path_list1.extend(path_list2)
#                     #print(path_list2)
#                     yield scrapy.Request(url=ct_url,headers=head,callback=self.cat_parse,meta={'path_list1':path_list2})
#
#         # elif response.xpath('//p[@style="text-align: center;"]/a/@href'):
#         #     for ij in loop_var:
#         #         # path_list2=[]
#         #         cat_nm=ij.xpath('.//h3//text()').get('').strip()
#         #         ct_url=ij.xpath('.//h3//following-sibling::p//a/@href').get()
#         #         if  ct_url:
#         #             if 'http' not in ct_url:
#         #                 ct_url = 'https://www.greatgages.com' + ct_url
#         #             else:
#         #                 ct_url = ct_url
#         #             # ct_url = 'https://www.greatgages.com' + ct_url
#         #             path_dict={}
#         #             path_dict['name']=cat_nm.replace('\r','').replace('\n','').replace('\t','').strip()
#         #             path_dict['url']=ct_url
#         #             path_list2=path_list1[:]
#         #             path_list2.append(path_dict)
#         #             # path_list1.extend(path_list2)
#         #             #print(path_list2)
#         #             yield scrapy.Request(url=ct_url,headers=head,callback=self.cat_parse,meta={'path_list1':path_list2})
#
#
#
#         # elif container_loop:
#         #     for ij in container_loop:
#         #         # path_list2=[]
#         #         # cat_nm=ij.xpath('.//text()').get('').strip()
#         #         ct_url=ij.xpath('.//@href').get()
#         #         if '-' in ct_url:
#         #             cat_nm = ct_url.split('/')[-1].strip().replace('-',' ')
#         #         else:
#         #             cat_nm =ct_url.split('/')[-1].strip()
#         #         if  ct_url:
#         #             if 'http' not in ct_url:
#         #                 ct_url = 'https://www.greatgages.com' + ct_url
#         #             else:
#         #                 ct_url = ct_url
#         #             # ct_url = 'https://www.greatgages.com' + ct_url
#         #             path_dict={}
#         #             path_dict['name']=cat_nm.replace('\r','').replace('\n','').replace('\t','').strip()
#         #             path_dict['url']=ct_url
#         #             path_list2=path_list1[:]
#         #             path_list2.append(path_dict)
#         #             # path_list1.extend(path_list2)
#         #             #print(path_list2)
#         #             yield scrapy.Request(url=ct_url,headers=head,callback=self.cat_parse,meta={'path_list1':path_list2})
#
#         elif pl_loop:
#             for product in pl_loop:
#                 item = IcsV1SiteMapLinksItem()
#                 product_link=product.xpath(".//@href").get()
#                 item['product_urls'] = 'https://www.greatgages.com'+product_link
#                 item['meta_data']=json.dumps(path_list1,ensure_ascii=False)
#                 item['vendor_id'] = self.VENDOR_ID
#                 item['vendor_name'] = self.VENDOR_NAME
#                 yield item
#             next_page_path = response.xpath("//a[@title='Next »']/@href").get()
#             if next_page_path:
#                 if "https://www.greatgages.com/" not in next_page_path:
#                     next_page_path = "https://www.greatgages.com/" + next_page_path
#                 yield scrapy.Request(url=next_page_path, callback=self.cat_parse,meta={'path_list1':path_list1})
#
#             # #pagination,
#             # url=path_list1[-1].get("url")
#             # cat_num=url[(url.rindex('/'))+1:-4]
#             # last_page=response.xpath('//div[@class="pages_available_text"]/a[last()]/text()').get()
#             # if last_page:
#             #     for i in range(2,int(last_page)+1):
#             #         new_page_url=f'{url}?searching=Y&sort=7&cat={cat_num}&show=30&page={i}'
#             #         yield scrapy.Request(url=new_page_url,headers=head,callback=self.cat_parse,meta={'path_list1':path_list1})
#
#
#
#
#
#
# if __name__ == '__main__':
#     execute("scrapy crawl great_links".split())