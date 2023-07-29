from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0", 
           "Referer": "https://www.google.com"}

# url = "https://relocate.me/search"

url = "https://relocate.me/denmark/billund/the-lego-group/lead-engineer-react-native-9321"

r = requests.get(url, headers=headers)

html = r.text

soup = BeautifulSoup(html, "html.parser")

job_url = soup.select_one(".job-sidebar a")
print(job_url.attrs['href'])
#print(job_urls.get(['href']))