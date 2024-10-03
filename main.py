import requests

from f import Cookie, detect, jschallenge

cookie = Cookie()
Cookie = cookie.get()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'cookie': Cookie,
}
url = "http://fantasyera.great-site.net/karm.php"
response = requests.get(url,headers=headers)
html = response.text


if detect(html) or (cookie == "" and detect(html)):
    cookie.set(jschallenge(html))
    print("Cookie Updated")
else:
    re = requests.get(url,headers=headers)
    html = response.text
    print(html)
    
