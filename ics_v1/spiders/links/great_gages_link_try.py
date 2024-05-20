import json
import pymysql, re
import scrapy
from scrapy.cmdline import execute
from ics_v1.items import IcsV1SiteMapLinksItem
import ics_v1.db_config as db

head={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }

def remove_extra_spaces(text):
    clean_text = re.sub('\s+', ' ', text)
    return clean_text.strip()

class WalkerIndustrialLinksSpider(scrapy.Spider):
    name ='great_links_try'

    start_urls = ['https://www.greatgages.com/']
    VENDOR_ID = "ACT-B2-002"
    VENDOR_NAME = "Great Gages"



    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        # DATABASE CONNECTION
        self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
        self.cursor = self.con.cursor()

    def start_requests(self):


        url = "https://www.greatgages.com/collections"

        payload = {}
        headers = {
            'Cookie': '_cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22merchant_geo%22%3A%22US%22%2C%22sale_of_data_region%22%3Afalse%7D; _landing_page=%2F; _orig_referrer=; _s=9d9b9b52-cb8c-4691-a2be-cd0e1a793d08; _shopify_s=9d9b9b52-cb8c-4691-a2be-cd0e1a793d08; _shopify_y=1144896c-48fa-4f67-b9a1-435d9cf4ef8d; _y=1144896c-48fa-4f67-b9a1-435d9cf4ef8d; cart_currency=USD; localization=US; secure_customer_sig='
        }
        # response = requests.request("POST", url, headers=headers, data=payload)
        yield scrapy.Request(url=url,callback=self.parse,headers=headers )

    def parse(self, response, **kwargs):
        main_cat_loop=response.xpath("(//div/ul/li/a[contains(@href,'collections')])[position()<6]")
        for main_cat in main_cat_loop:
            dict_main = {}
            main_list = []
            main_cat_url=main_cat.xpath("./@href").get()
            main_cat_name = remove_extra_spaces(" ".join(main_cat.xpath(".//text()").getall()))
            if not main_cat_url.startswith("http"):
                main_cat_url="https://www.greatgages.com"+main_cat_url
                dict_main["name"] = main_cat_name
                dict_main["url"] = main_cat_url
                main_list.append(dict_main)
            yield scrapy.Request(url=main_cat_url, headers=head, callback=self.parse2, cb_kwargs={"list_main":main_list,"dict":dict_main})

    def parse2(self, response, **kwargs):
        list_main=kwargs['list_main']
        print(list_main)
        inner_cat_loop=response.xpath("//a[contains(@href,'collections')]/img/parent::a")
        product_loop=response.xpath("//h3/a[contains(@href,'products')]")

        if inner_cat_loop and product_loop:
            for inner_cat in inner_cat_loop:
                dict_main_2 = {}
                path_list = []
                inner_cat_url=inner_cat.xpath("./@href").get()
                inner_cat_name=remove_extra_spaces(" ".join(inner_cat.xpath("./parent::div/parent::div/following-sibling::div//text()").getall()))
                if not inner_cat_url.startswith("http"):
                    inner_cat_url = "https://www.greatgages.com" + inner_cat_url
                    dict_main_2["name"]=inner_cat_name
                    dict_main_2["url"]=inner_cat_url
                    path_list.extend(list_main)
                    path_list.append(dict_main_2)
                else:
                    dict_main_2['name'] = inner_cat_name
                    dict_main_2['url'] = inner_cat_url
                    path_list.extend(list_main)
                    path_list.append(dict_main_2)
                yield scrapy.Request(url=inner_cat_url, callback=self.parse2,cb_kwargs={"list_main":path_list})
        else:
            for product in product_loop:
                product_url=product.xpath("./@href").get()
                if not product_url.startswith("http"):
                    product_url = "https://www.greatgages.com" + product_url
                item = IcsV1SiteMapLinksItem()
                item['product_urls'] = product_url
                item['vendor_id'] = self.VENDOR_ID
                item['vendor_name'] = self.VENDOR_NAME
                item['meta_data'] = json.dumps(list_main, ensure_ascii=False)
                # print(item)
                yield item
            next_page_url=response.xpath("//span[@class='next']/a/@href").get()
            if next_page_url:
                if not next_page_url.startswith("http"):
                    next_page_url = "https://www.greatgages.com" + next_page_url
                yield scrapy.Request(url=next_page_url, headers=head, callback=self.parse2,cb_kwargs={"list_main":list_main})


if __name__ == '__main__':
    execute("scrapy crawl great_links_try".split())



