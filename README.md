<h1 align="center" id="title">Fast Torrent Downloader</h1>

<p align="center"><img src="https://cdn3.iconfinder.com/data/icons/strokeline/128/21_icons-256.png" alt="project-image"></p>

<p id="description">This is a simple Python script for searching and downloading torrents using various providers. The script currently supports three providers: <b>Torrentio, 1337x and ThePirateBay</b>. It utilizes the <b>Seedr</b> service for downloading torrents.</p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Provider Selection: Choose between Torrentio , 1337x and ThePirateBay as your torrent provider.
*   Search and Download: Search for torrents based on your query and download the selected one.
*   Direct Magnet Link Download: Enter a magnet link to download the corresponding torrent directly.
*   Torrent Showing Limit: Adjust the limit for the number of torrents displayed in the search results.

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository to your local machine:</p>

```
git clone https://github.com/Rounak40/Fast-Torrent-Downloader.git
```

<p>2. Install Modules:</p>

```
cd torrent-downloader
pip install -r requirements.txt
```

<p>3. Setup config.ini file:</p>

```
[seedr]
username = username/email
password = password
[storage]
output_path = output folder name
unzip = True/False
```


<h2>💻 Torrent Providers</h2>
<p id="description"><b>1. Torrentio</b> is a versatile torrent provider that aggregates torrents from various sources. It scrapes torrent data from popular torrent providers, ensuring a diverse range of content. Currently, Torrentio supports the following torrent providers</p>

* YTS(+)
* EZTV(+)
* RARBG(+)
* 1337x(+)
* ThePirateBay(+)
* KickassTorrents(+)
* TorrentGalaxy(+)
* MagnetDL(+)
* HorribleSubs(+)
* NyaaSi(+)
* TokyoTosho(+)
* AniDex(+)
* Rutor(+)
* Rutracker(+)
* Comando(+)
* BluDV(+)
* Torrent9(+)
* MejorTorrent(+)
* Cinecalidad(+)

<p id="description"><b>2. 1337x</b> is a well-known torrent provider that has been in the torrenting scene for a long time. It offers a user-friendly interface and a vast library of torrents across different categories. Users can find movies, TV shows, music, games, and more.</p>

<p id="description"><b>3. ThePirateBay</b>  is one of the most iconic and controversial torrent providers. It has been a go-to source for torrents for many users. The platform allows users to search for and download a wide range of content, including movies, TV shows, music, software, and more.</p>

<h2>🍰 Seedr:</h2>

Seedr is used as the download provider in this script. It offers a <b>faster</b> and more secure way to download torrents. It is important to note that free users on Seedr have a maximum download size limit of 2GB. Seedr enhances the torrenting experience by providing a convenient and efficient way to download content from the selected torrent providers.





<h2>🍰 Contribution Guidelines:</h2>

Feel free to contribute to the project by opening issues or submitting pull requests.

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python


<h2>🛡️ License:</h2>

This project is licensed under the This project is licensed under the MIT License - see the LICENSE file for details.
