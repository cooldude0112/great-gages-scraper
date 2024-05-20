import os.path
import pymysql
import scrapy
from scrapy.cmdline import execute
from scrapy.utils.response import open_in_browser
import hashlib

from ics_v1 import db_config as db


class DownloadAssestSpider(scrapy.Spider):
    name = 'download_assest'
    assets_save = 'C:/Work/Actowiz/pages/ics/assets/'


    def __init__(self,start,end, name="Great Gages", vendor_id="ACT-B2-002", **kwargs):
        super().__init__(name, **kwargs)
        if not vendor_id:
            exit(-1)
        self.VENDOR_ID = vendor_id
        self.assets_save += vendor_id + "/"
        if not os.path.exists(self.assets_save):
            os.makedirs(self.assets_save)
        self.start = start
        self.end = end
        self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
        self.cursor = self.con.cursor()

    def start_requests(self):
        select_query = [
            f"select id, source, file_name, is_main_image, name, type from {db.asset_table} where",
            f"vendor_id = '{self.VENDOR_ID}'",
            f"and status = 'pending'",
            f"and id between {self.start} and {self.end}"
        ]

        self.cursor.execute(" ".join(select_query))

        for data in self.cursor.fetchall():
            if not data[1].strip():
                continue
            # print(data)
            yield scrapy.Request(
                url=data[1],
                cb_kwargs={
                    "id": data[0],
                    "file_name": data[2],
                    "main": data[3],
                    "name": "" if not data[4] else data[4],
                    "type": "" if not data[5] else data[5],
                },
                dont_filter=True
            )

    def parse(self, response, **kwargs):

        id = kwargs['id']

        if 'play.google.com' in response.url:
            print("invalid document url")
            update = f'update {db.asset_table} set status="invalid" where Id={id}'
            self.cursor.execute(update)
            self.con.commit()
            self.logger.info(f'{db.asset_table} Inserted...')
            self.con.commit()
            return None

        if self.VENDOR_ID == "ACT-B2-002" and ('.php' in response.url or '.asp' in response.url):
            if 'Content-Disposition' not in response.headers:
                if 'already_processed' not in kwargs:
                    kwargs['already_processed'] = True
                    yield scrapy.FormRequest.from_response(response, cb_kwargs=kwargs)
                    return None

        file_name = kwargs['file_name']
        if response.url.endswith(".exe"):
            file_name = response.url.split("/")[-1]
        if not file_name or file_name.endswith(".php") or file_name.endswith(".asp"):
            file_name = response.headers['content-disposition'].decode("utf-8").split("=")[-1].strip('"')

        file_type = kwargs['type']
        if not file_type:
            file_type = None
            if kwargs['main']:
                file_type = "image/product"
            elif ".zip" in file_name:
                file_type = "other"
            elif file_name.split(".")[-1].lower() in ['dxf', 'dwg', 'slddrw']:
                file_type = "cad/2D"
            elif file_name.split(".")[-1].lower() in ['step', 'iges', 'igs', 'sldprt', 'ipt', 'x_t', 'eprt', '.step']:
                file_type = "cad/3D"
            elif file_name.split(".")[-1].lower() in ['cert', 'crt']:
                file_type = "document/cert"

            if 'software' in kwargs['name'].lower():
                file_type = "other"

            if not file_type:
                if 'manual' in kwargs['name'].lower():
                    file_type = "document/manual"
                elif 'spec' in kwargs['name'].lower():
                    file_type = "document/spec"
                elif 'catalog' in kwargs['name'].lower():
                    file_type = "document/catalog"

            if not file_type and '.pdf' in file_name.lower():
                file_type = "document"

            if not file_type and file_name.split(".")[-1].lower() in ['png', 'jpg']:
                file_type = "image/product"

            if not file_type:
                file_type = "other"

        sha256 = hashlib.sha256(response.body).hexdigest()

        if 'Content-Length' in response.headers:
            length = response.headers['Content-Length'].decode("utf-8")
        else:
            length = response.body.__sizeof__()

        content_type = response.headers['Content-Type'].decode("utf-8")
        if ";" in content_type:
            content_type = content_type.split(";")[0].strip()

        item = dict()
        item['download_path'] = self.assets_save + str(sha256)
        item['media_type'] = content_type
        item['length'] = length
        item['type'] = file_type
        item['sha256'] = sha256
        item['file_name'] = file_name
        item['status'] = "Done"

        open(item['download_path'], "wb").write(response.body)

        try:
            field_list = []
            for field in item.items():
                field_list.append(f'{field[0]}="{field[1]}"')

            update = f'update {db.asset_table} set {", ".join(field_list)} where Id={id}'
            self.cursor.execute(update)

            self.con.commit()
            self.logger.info(f'{db.asset_table} Inserted...')
            self.con.commit()

        except Exception as e:
            self.logger.error(e)


if __name__ == '__main__':
    execute("scrapy crawl download_assest -a vendor_id=ACT-B2-002 -a start=1 -a end=15000".split())
