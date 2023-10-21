import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from requests.exceptions import RequestException
from time import sleep

url_one = 'https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9-laptop/'
# print(url == url_t)
headerss = {
            # "Accept-Encoding": "en-US,en;q=0.9,fa;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
            # 'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'}

response = requests.get(url_one, headers=headerss)
# print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
sss = soup.find('div', {'class': 'jsx-149d835e1ecfb944 left-container'})
sss1 = sss.find('div', {'class': 'jsx-fadcb1a11849c1b4 cards'})
# print(sss1.text)
laps = sss1.find_all('div', {'class': 'jsx-2514672dc9197d80'})
url_mark = pd.read_json('api_num.json', orient='records')
url_mark = url_mark['num_of_forward'][0]


ab_urls = []
urls = []
# for lap in laps:
#     uli = lap.find('a', href=True)
#     if uli != None:
#         urls.append('https://torob.com' + uli['href'])

# print(len(urls))
# 42709
rec = 0
for numm in range(url_mark, 301):
  if numm%50 == 0:
    sleep(1.5)
    print('1')
  if numm == 1:
    url_pattern = f'https://api.torob.com/v4/base-product/search/?page={numm}&sort=popularity&size=24&category_name=%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9-laptop&category_id=99&category=99&source=next_desktop&suid=652a4aa60cca9980fcfe7e02&_bt__experiment=&suid=652a5990a9b7173bcb892bc7'
  else:
    url_pattern = f'https://api.torob.com/v4/base-product/search/?page={numm}&sort=popularity&size=24&category_name=%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9-laptop&category_id=99&category=99&source=next_desktop&suid=652a4aa60cca9980fcfe7e02&_bt__experiment='

  try:
    response = requests.get(url_pattern, headers=headerss, timeout=7)
  except RequestException as e:
    print("Error: {}".format(e))
    ab_urls.append(url_pattern)
    # reasone.append('Conncection Error')
    sleep(1)
    continue

  # response = requests.get(url_pattern, headers=headerss)
  info_js = json.loads(response.text)
  results = info_js['results']
  for res in results:
    urls.append('https://torob.com' + res['web_client_absolute_url'])
  rec = numm

print(urls)
df_links = pd.DataFrame({'links': urls})
df_links.to_csv('links.csv', mode='a', header=False)

abondoned_lap = pd.DataFrame({'abondoned': ab_urls})
abondoned_lap.to_csv('ab_api.csv', mode='a', header=False)

mark_u = pd.DataFrame([{'num_of_forward': rec}]).to_json('api_num.json')