import os
import time
import requests
from _thread import*
from bs4 import BeautifulSoup
from WebScraper import WebCrawler
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


web = WebCrawler()
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
""""
try:
    gauth.LoadCredentialsFile("my_credentials.txt")
except Exception as e:
"""
#gauth.LocalWebserverAuth()
#gauth.SaveCredentialsFile("my_credentials.txt")

gauth.LoadCredentialsFile("my_credentials.txt")
    
    
with open("used-links.txt","a+") as _:
	pass
	
def _create_folder(folder_name):
    f = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    folders = [folder['title'] for folder in f]
    if folder_name not in folders:
        # Create folder
        folder = drive.CreateFile({'title': f'{folder_name}', "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()

def _save_data(folder_name,data):
    # Upload file to folder
    folders = drive.ListFile({'q': "title='" +folder_name+ "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folders:
        if folder['title'] == folder_name:
            file = drive.CreateFile({'parents': [{'id': folder['id']}],'title': f'{data[0]}.txt'})
            file.SetContentString(data[1])
            file.Upload()
    

def Get_BBC_data(folder_name,url):
    i = 0
    USED_LINKS = [i.strip() for i in open("used-links.txt")]
    html = web.open_url(url)
    BASE_URL = "https://www.bbc.com/"
    if folder_name != "english":pattern = f"/{folder_name}/"
    else:pattern = "/"
    
    print(f"Starting to crawl :{folder_name}")

    _create_folder(folder_name)
    links = web.crawl_link(html,pattern=pattern)
    
    for link in links:
        
        if link.startswith("/"):link = BASE_URL+link
        else:pass
        if link not in USED_LINKS:
            print(f"length of USED LINKS : {len(USED_LINKS)}\n")
            
            print(f"{folder_name} :: {link}")
            print("\n"*4)
            try:
                html = web.open_url(link)
                links.extend(list(set(web.crawl_link(html,pattern=pattern))))
                data = web.gather_text(html)
                _save_data(folder_name,data)
                with open("used-links.txt","a+") as used:
                    used.write(link+"\n")
                    
                if i == 25:
                    i = 0
                    time.sleep(30)
                    print("Going to sleep now")
                i+=1
            except Exception as e:
                print(e)
        else:
            pass
        USED_LINKS = [i.strip() for i in open("used-links.txt")]
        
        

URL_DATA =	[("pidgin","https://www.bbc.com/pidgin"),("igbo","https://www.bbc.com/igbo"),
("english","https://www.bbc.com/"),("hausa","https://www.bbc.com/hausa"),
("yoruba","https://www.bbc.com/yoruba")]
 

for folder_name,entry_url in URL_DATA:
    try:
        start_new_thread(Get_BBC_data,(folder_name,entry_url,))
    except Exception as e:
        print(e)

while 1:
    pass


