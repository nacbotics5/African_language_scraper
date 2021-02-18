import requests,re
from bs4 import BeautifulSoup
 
class WebCrawler(object):
    def __init__(self):
        self.browser = requests.session()
        self.user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    
    def open_url(self,url):
        html = self.browser.get(url,headers = self.user_agent,allow_redirects=False).content
        return(html)
    
    def gather_text(self,html):
        soup = BeautifulSoup(html, features="html.parser")
        Title = soup.title.text
        
        for tags in soup(["script", "style","head","sidebar","title","a"]):
        	tags.decompose()
        text = " ".join(list(soup.stripped_strings))
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return(Title,text)
 
   
    def crawl_link(self,html,pattern="(.*?)"):
        pages = []
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile(pattern)):
            if "href" in link.attrs:
                try:
                    file_link = link.attrs['href']
                    pages.append(file_link)
                except Exception as e:print(str(e))
        return(pages)
