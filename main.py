from torrents import x1337, thepiratebay, torrentio
from downloader import Seedr


class Provider:
    def __init__(self) -> None:
        self.limit = 10
        self.provider_name = "Torrentio"
        self.provider = torrentio(limit=self.limit)
        self.download_provider = Seedr()

    def set_provider(self,provider_name):
        self.provider_name = provider_name
        self.provider = provider_list[provider_name]
    
    def set_limit(self,limit):
        self.limit = limit
        self.provider.LIMIT = limit
    
    def search_torrent(self,query):
        if self.provider_name == "Torrentio":
            _type = input("Select Search Type:\n1. Movie\n2. Series\n=> ")
            response = self.provider.search_library(query,_type)
            
            for i, m in enumerate(response):
                print(f"{i+1}. Title: {m['name']}")
                print(f"   Imdb: https://www.imdb.com/title/{m['imdb_id']}/ ")
                print()
                
            c = input("Select from the list (1,2...): ")
            _id = response[int(c)-1]["id"]

            if _type == "2":
                series_episodes = self.provider.get_series_details(_id)
                for i, m in enumerate(series_episodes):
                    print(f"{i+1}. Title: {m['name']}")
                    print(f"   Season: {m['season']} ")
                    print(f"   Episode: {m['episode']} ")
                    print()
                
                c = input("Select Episode from the list (1,2...) => ")
                _id = series_episodes[int(c)-1]["id"]
                
            torrents_list = self.provider.search_torrent(_id,_type)
        else:
            torrents_list = self.provider.search_torrent(query)
        
        return torrents_list

    def magnet_link(self,data):
        return self.provider.get_magnet_link(data)
    
    def download(self,magnet):
        self.download_provider.download(magnet)


api = Provider()

provider_list = {
    "Torrentio": torrentio(),
    "1337x": x1337(),
    "ThePirateBay": thepiratebay(),
}

while True:
    choice = input(f"1. Select Provider. (Current: {api.provider_name})\n2. Search and Download.\n3. Download Direct from Magnet Link.\n4. Change Torrent Showing Limit. (Current: {api.limit})\n=> ")

    if choice == "1":
        selected_provider = input("1. Torrentio (Default)\n2. 1337x\n3. ThePirateBay\n=> ")
        if selected_provider == "1" or selected_provider == "":
            api.set_provider("Torrentio")
        elif selected_provider == "2":
            api.set_provider("1337x")
        elif selected_provider == "3":
            api.set_provider("ThePirateBay")
        else:
            print("Invalid Selection!")

    elif choice == "2":
        query = input("Search Query =>  ")
        torrents_list = api.search_torrent(query)
        for i, torrent in enumerate(torrents_list):
            print(f"{i+1}. Title: {torrent['title']}")
            print(f"   Size: {torrent['size']} | Seeders: {torrent['seeders']} ")
            print(f"   Upload Date: {torrent['upload_date']} | Uploader: {torrent['uploader']}")
            print()

        user_input = int(input("Enter the index of the torrent you want to download => "))
        magnet = api.magnet_link(torrents_list[user_input-1])
        api.download(magnet)
    
    elif choice == "3":
        magnet = input("Enter the Magnet Link => ")
        api.download(magnet)
    
    elif choice == "4":
        api.set_limit(int(input("New Limit => ")))