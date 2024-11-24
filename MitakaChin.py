from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://suumo.jp/chintai/tokyo/sc_mitaka/mansion/?page={}'

d_list =[]

for i in range(1,41):
    print('d_listの大きさ',len(d_list))
    target_url = url.format(i)

    print(target_url)

    r = requests.get(target_url)

    sleep(1)

    soup = BeautifulSoup(r.text, 'html.parser')  # 'html.parser'を指定

    contents = soup.find_all('div', class_='cassetteitem')
    # print(len(contents))

    for content in contents:
        detail = content.find('div', class_='cassetteitem-detail')
        table = content.find('table', class_='cassetteitem_other')

        title = detail.find('div', class_='cassetteitem_content-title').text
        address = detail.find('li', class_='cassetteitem_detail-col1').text
        access = detail.find('li', class_='cassetteitem_detail-col2').text
        age = detail.find('li', class_='cassetteitem_detail-col3').text

        tr_tags = table.find_all('tr', class_='js-cassette_link')
        for tr_tag in tr_tags:

            floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]

            fee, management_fee = price.find_all('li')
            deposit, gratuity = first_fee.find_all('li')
            madori, menseki = capacity.find_all('li')

            d = {
              'title':title,
              'address':address,
              'access':access,
              'age':age,
              'floor':floor.text,
              'fee':fee.text,
              'management_fee':management_fee.text,
              'deposit':deposit.text,
              'gratuity':gratuity.text,
              'madori':madori.text,
              'menseki':menseki.text
            }

            d_list.append(d)

# print(d_list[:2])

df = pd.DataFrame(d_list)
print(df.head())
print(df.shape)
print(len(df.title.unique()))

df.to_csv('MitakaChin.csv', index=None,encoding = 'utf-8-sig' )
