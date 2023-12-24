import urllib.parse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re



def convert_bytes_to_gb_mb(byte_size):
    gb_size = byte_size / (1024 ** 3)
    
    if gb_size >= 1:
        return f"{gb_size:.2f} GB"

    mb_size = byte_size / (1024 ** 2)
    return f"{mb_size:.2f} MB"


class x1337:
    def __init__(self, limit=10):
        self.BASE_URL = "https://1337x.unblockit.ing"
        self.LIMIT = limit
        self.session = requests.Session()
        self.session.headers  = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
    

    def get_magnet_link(self,data):
        response = self.session.get(data["url"])
        magnet_link = 'magnet:?' + response.text.split('href="magnet:?')[1].split("\"")[0].strip()
        return magnet_link

    def search_torrent(self,query):
        torrents_list = []
        page = 0
        while len(torrents_list) < self.LIMIT:

            page += 1
            formated_query = query.replace(" ","+")
            page_url = f"{self.BASE_URL}/search/{formated_query}/{page}/"
            response = self.session.get(page_url)
            soup = BeautifulSoup(response.text,"lxml")

            rows = soup.findAll("tr")

            if len(rows) == 0:
                break

            for row in rows:
                temp_dict = {}
                for col in row.findAll("td"):
                    class_name = col.get("class")[-1]
                    if not class_name:
                        continue

                    if "name" in class_name:
                        temp_dict["title"] =  col.text.strip("â\xad\x90")
                        link = col.findAll("a")[-1].get("href")
                        if link != None:
                            temp_dict["url"] = self.BASE_URL+col.findAll("a")[-1].get("href")
                    elif "seeds" in class_name:
                        temp_dict["seeders"] =  int(col.text.strip())
                    elif "leeches" in class_name:
                        temp_dict["leechers"] =  int(col.text.strip())
                    elif "date" in class_name:
                        temp_dict["upload_date"] =  col.text.strip()
                    elif "mob-trial-uploader" in class_name or "mob-user" in class_name or "mob-vip" in class_name or "mob-uploader" in class_name:
                        size = col.text.strip()
                        if "GB" in size:
                            temp_dict["size"] = size.split("GB")[0].strip() + " GB"
                        elif "MB" in size:
                            temp_dict["size"] = size.split("MB")[0].strip() + " MB"
                        else:
                            temp_dict["size"] = size
                    elif "trial-uploader" in class_name or "user" in class_name or "vip" in class_name or "uploader" in class_name:
                        temp_dict["uploader"] = col.text.strip()
            
                if temp_dict.get("url"):
                    torrents_list.append(temp_dict)

                if len(torrents_list) == self.LIMIT:
                    break
        return torrents_list



class thepiratebay:
    def __init__(self, limit=10):
        self.BASE_URL = "https://thepiratebaye.org"
        self.LIMIT = limit
        self.session = requests.Session()
        self.session.headers  = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        
    def get_magnet_link(self,data):
        trackers = [
            'udp://tracker.coppersurfer.tk:6969/announce',
            'udp://tracker.openbittorrent.com:6969/announce',
            'udp://tracker.opentrackr.org:1337',
            'udp://movies.zsw.ca:6969/announce',
            'udp://tracker.dler.org:6969/announce',
            'udp://opentracker.i2p.rocks:6969/announce',
            'udp://open.stealth.si:80/announce',
            'udp://tracker.0x.tf:6969/announce'
        ]

        name =  urllib.parse.quote(data["title"])
        ih = data["info_hash"]


        magnet_link = f'magnet:?xt=urn:btih:{ih}&dn={name}'

        for tracker in trackers:
            magnet_link += '&tr=' + urllib.parse.quote(tracker)
    
        return magnet_link

    def search_torrent(self,query):
        torrents_list = []

        formated_query = query.replace(" ","+")
        page_url = f"{self.BASE_URL}/api.php?url=/q.php?q={formated_query}&cat="
        response = self.session.get(page_url)
    
        for result in response.json():
            temp_dict = {
                "title": result["name"],
                "info_hash": result["info_hash"],
                "seeders": result["seeders"],
                "leechers": result["leechers"],
                "upload_date": datetime.utcfromtimestamp(int(result["added"])).strftime('%Y-%m-%d'),
                "size": convert_bytes_to_gb_mb(int(result["size"])),
                "uploader": result["username"]
                }
            
            torrents_list.append(temp_dict)

            if len(torrents_list) == self.LIMIT:
                break
        return torrents_list


class torrentio:
    def __init__(self, limit=10):
        self.BASE_URL = "https://v3-cinemeta.strem.io"
        self.TORRENT_URL = "https://torrentio.strem.fun"
        self.LIMIT = limit
        self.session = requests.Session()
        self.session.headers  = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        self.pattern = r"(?P<title>.*?)\n👤 (?P<seeders>\d+) 💾 (?P<size>[\d.]+ \w+) ⚙️ (?P<uploader>\w+)"
        
    def get_magnet_link(self,data):
        magnet_link = 'magnet:?xt=urn:btih:' + data['infoHash']
        return magnet_link

    def search_library(self,query,_type):
        formated_query = query.replace(" ","+")
        if _type == "1":
            res = self.session.get(self.BASE_URL+"/catalog/movie/top/search="+formated_query+".json").json()
        elif _type == "2":
            res = self.session.get(self.BASE_URL+"/catalog/series/top/search="+formated_query+".json").json()
        
        return res["metas"][:10]

    def get_series_details(self,_id):
        res = self.session.get(self.BASE_URL+"/meta/series/"+_id+".json").json()
        
        return res["meta"]["videos"]


    def search_torrent(self,_id,_type):
        torrents_list = []
        if _type == "1":
            res = self.session.get(self.TORRENT_URL+"/stream/movie/"+_id+".json").json()
        elif _type == "2":
            res = self.session.get(self.TORRENT_URL+"/stream/series/"+_id+".json").json()

        for i in res["streams"]:
            temp = re.match(self.pattern, i['title']).groupdict()
            temp["upload_date"] = "N/A"
            temp["infoHash"] = i["infoHash"]
            torrents_list.append(temp)

            if len(torrents_list) == self.LIMIT:
                break
        

        return torrents_list