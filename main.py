import requests

from f import detect, jschallenge

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'cookie': '',
}
url = "http://fantasyera.great-site.net/karm.php"
response = requests.get(url,headers=headers)
html = response.text


if detect(html):
    cookie = jschallenge(html)
    headers['cookie'] = cookie  # Update headers with the new cookie
    print("Cookie mil gayi")
    print(requests.get(url,headers=headers).text)
else:
    print(html)
    
