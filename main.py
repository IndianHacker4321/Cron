import requests

from f import Cookie, detect, jschallenge

cookie = Cookie()
current_cookie = cookie.get()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'cookie': current_cookie,
}
url = "http://fantasyera.great-site.net/karm.php"
response = requests.get(url,headers=headers)
html = response.text


if detect(html) or (current_cookie == "" and detect(html)):
    new_cookie = jschallenge(html)
    cookie.set(new_cookie)  # Save the new cookie
    headers['cookie'] = new_cookie  # Update headers with the new cookie
    print("Cookie Updated")
    print(html)
else:
    print(html)
    
