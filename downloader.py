import zipfile
from configparser import ConfigParser 
import requests
import time
import os
from urllib.parse import urlparse
from tqdm import tqdm
import urllib.parse


config = ConfigParser() 
config.read("config.ini")


if config["seedr"]["username"] == None or config["seedr"]["password"] == None:
    raise ValueError("Please enter username and password in congif.ini")
if config["storage"]["output_path"] == None:
    raise ValueError("Please enter output directory for download")

class Seedr:
    def __init__(self):
        self.username = config["seedr"]["username"]
        self.password = config["seedr"]["password"]

        self.download_location = config["storage"]["output_path"]
        self.unzip = config["storage"]["unzip"]

        self.loggedin = False

        self.BASE_URL = "https://www.seedr.cc"

        self.session = requests.Session()
        self.session.headers  = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        self.login()

    def login(self):
    
        response = self.session.post(self.BASE_URL+'/auth/login', json={
            'username': self.username,
            'password': self.password,
            'g-recaptcha-response': '',
            'h-captcha-response': '',
            'rememberme': 'on',
        })

        if response.status_code == 400 :
            print(f"Login failed in seedr: {response.json()['reason_phrase']}")
        elif response.status_code == 200:
            print("Logged in successfully in Seedr.")
            self.loggedin = True
        else:
            print(f"Error: {response.json()}")
    
    def download(self,magnet_link):
        task_response = self.add_magnet_link(magnet_link)

        if task_response.get("reason_phrase") == "not_enough_space_added_to_wishlist":
            print("Failed Reason: not_enough_space")
        else:
            
            title = task_response["title"]

            tries = 0
            failed = False
            print("Please wait...")
            while self.is_downloading():

                if tries > 24:
                    failed = True
                    break

                tries += 1
                time.sleep(5)

            if failed:
                torrent_id = self.get_torrent_id(title)
                self.delete_torrent(torrent_id)
                print("Not able to download this try different torrent.")
            else:
                folder_id = self.get_folder_id(title)
                if folder_id == -1:
                    print("Failed to get download link..")
                    return
                link = self.get_download_link(folder_id)
                self.download_local(link)
                self.delete_folder(folder_id)

    def download_local(self,download_link):

        if os.path.exists(self.download_location) == False:
            os.mkdir(self.download_location)

        filename = urllib.parse.unquote(os.path.basename(urlparse(download_link).path))
        print("Saving File as :",filename)

        output_path = self.download_location + "/" + filename

        with requests.get(download_link, stream=True) as r:
            r.raise_for_status()
            total_size_in_bytes= int(r.headers.get('content-length', 0))
            block_size = 10 * 1024 * 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    progress_bar.update(len(chunk))
                    f.write(chunk)
            progress_bar.close()

        print("Downloaded.")

        if self.unzip:
            print("Unzippping...")
            extracted_dir = self.download_location
            os.makedirs(extracted_dir, exist_ok=True)
            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_dir)

            os.remove(output_path)

            print(f"Files extracted.")

    def delete_torrent(self,torrent_id):
        response = self.session.post(self.BASE_URL+'/fs/batch/delete', data={
            'delete_arr': '[{"type":"torrent","id":"'+torrent_id+'"}]'
            })
        return response

    def delete_folder(self,folder_id):
        response = self.session.post(self.BASE_URL+'/fs/batch/delete', data={
            'delete_arr': '[{"type":"folder","id":"'+folder_id+'"}]'
            })
        return response

    def get_torrent_id(self,title):
        items = self.get_items()
        for torrent in items["torrents"]:
            if torrent['name'] == title:
                return str(torrent['id'])
        try:
            return str(items["torrents"][-1]['id'])
        except:
            return -1


    def get_folder_id(self,title):
        items = self.get_items()
        for folder in items["folders"]:
            if folder['path'] == title:
                return str(folder['id'])
        return -1


    def get_download_link(self,folder_id):
        response = self.session.post(self.BASE_URL+'/download/archive', data={
            'archive_arr[0][type]': 'folder',
            'archive_arr[0][id]': folder_id
            })
        return response.json()["url"]
        

    def get_items(self):
        response = self.session.get(self.BASE_URL+'/fs/folder/0/items')
        return response.json()

    def is_downloading(self):
        return len(self.get_items()["torrents"]) != 0

    def add_magnet_link(self,magnet):
        response = self.session.post(self.BASE_URL+'/task', data={
        'folder_id': '0',
        'type': 'torrent',
        'torrent_magnet': magnet
        })

        return response.json()

        
