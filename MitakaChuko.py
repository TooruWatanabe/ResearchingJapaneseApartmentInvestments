from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://suumo.jp/ms/chuko/tokyo/sc_mitaka/?page={}'

d_list =[]

for i in range(1,12):
    print('d_listの大きさ',len(d_list))
    target_url = url.format(i)

    print(target_url)

    r = requests.get(target_url)

    sleep(1)

    soup = BeautifulSoup(r.text, 'html.parser')  # 'html.parser'を指定

    contents = soup.find_all('div', class_='property_unit-content')
    # print(len(contents))

    for content in contents:
        table = content.find('div', class_='dottable dottable--cassette')
        tr_tags = table.find_all('dd')

        property_name = tr_tags[0].text.strip()
        price = tr_tags[1].text.strip()
        address = tr_tags[2].text.strip()
        station_info = tr_tags[3].text.strip()
        area = tr_tags[4].text.strip()
        room_type = tr_tags[5].text.strip()
        size = tr_tags[6].text.strip()
        built_date = tr_tags[7].text.strip()

        d = {
        "物件名": property_name,
        "価格": price,
        "住所": address,
        "最寄り駅情報": station_info,
        "面積": area,
        "間取り": room_type,
        "納戸サイズ": size,
        "築年月": built_date
        }

        d_list.append(d)

df = pd.DataFrame(d_list)
print(df.head())
print(df.shape)

df.to_csv('MitakaChuko.csv', index=None,encoding = 'utf-8-sig' )
