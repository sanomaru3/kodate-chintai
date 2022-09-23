import datetime
import os
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
from time import sleep
import tool as tl

def get_result_dict_list(input_dic):
    url = 'https://myhome.nifty.com/rent/ct_house/'

    options = Options()

    options.add_argument('--incognito')
    # headlessモードで実行
    options.add_argument('--headless')

    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options) 

    exist_prefecture, exist_city = False, False

    for input_data in input_dic:
        # 結果となるデータ
        result_dic_list = []
        
        driver.get(url)
        sleep(random.uniform(2.5, 3.5))

        # 都道府県選択
        a_tags = driver.find_elements_by_tag_name('a')
        for a_tag in a_tags:
            if a_tag.text == input_data['prefecture']:
                exist_prefecture = True
                nextHref = a_tag.get_attribute('href')
                # 「市区町村から探す」タブを選択させる
                if nextHref[-5:] != '/city':
                    nextHref += 'city'  
                
                driver.get(nextHref)
                sleep(random.uniform(2, 3))
                break

        # 移動先で市区町村を選択
        a_tags = driver.find_elements_by_tag_name('a')
        for a_tag in a_tags:
            if a_tag.text == input_data['city']:
                exist_cit = True
                driver.get(a_tag.get_attribute('href'))
                sleep(random.uniform(2, 3))
                break
        
        prefecture = input_data['prefecture']
        city = input_data['city']

        print('{0}{1}のデータを取得します'.format(prefecture, city))

        count = 1
        exist_next = True
        while exist_next:
            # 物件情報が入っている要素を取得
            cards = driver.find_elements_by_class_name('card')
            cards = [card for card in cards if card.get_attribute('data-show-other-room') != None]

            for card in cards:
                sys.stdout.write('\r' + '{0}{1}の{2}件目のデータを取得中・・・'.format(prefecture, city, count))
                card_a_tags = card.find_elements_by_tag_name('a')

                # 1.タイトル
                title = card_a_tags[0].text

                # 2.駅からの距離
                distance_lists = card_a_tags[1].find_element_by_tag_name('ul').find_elements_by_tag_name('li')
                distance = ''

                for distance_list in distance_lists:
                    distance += distance_list.text

                # 3.住所
                address = card_a_tags[1].find_element_by_tag_name('p').text

                dl_list = card_a_tags[1].find_elements_by_tag_name('dl')
                # 4.総階数
                floors = dl_list[0].find_element_by_tag_name('dd').text
                # 5.築年数
                age = dl_list[1].find_element_by_tag_name('dd').text
                age = age.replace('年', '.').replace('ヶ月', '')
                # 6.建物構造
                construction = dl_list[2].find_element_by_tag_name('dd').text
                # 7.駐車場
                try:
                    badge = card_a_tags[1].find_element_by_class_name('badge')
                except:
                    badge = None
                if badge == None or badge.text != '駐車場あり':
                    parking = '-'
                else:
                    parking = '駐車場あり'

                card_tds = card.find_element_by_class_name('result-bukken-item').find_elements_by_tag_name('td')

                ps_layout_area =card_tds[2].find_elements_by_tag_name('p')
                # 8.間取り
                layout = ps_layout_area[0].text
                # 9.専有面積
                area = ps_layout_area[1].text
                area = area.replace('㎡', '')

                ps_rent_managementFee = card_tds[3].find_elements_by_tag_name('p')
                # 10.賃料
                rent = ps_rent_managementFee[0].text
                rent = rent.replace('万円', '')
                # 11.管理費等
                managementFee = ps_rent_managementFee[1].text
                managementFee = managementFee.replace('円', '').replace(',', '')

                dls_deposit_keyMoney = card_tds[4].find_elements_by_tag_name('dl')
                # 12.敷金
                deposit = dls_deposit_keyMoney[0].find_element_by_tag_name('dd').text
                deposit = deposit.replace('円', '').replace(',', '')
                # 敷金が「～ヶ月」表記だった場合に賃料との積にする
                if deposit[-2:] == 'ヶ月':
                    deposit = float(rent) * float(deposit.replace('ヶ月', '')) * 10000
                # 13.礼金
                keyMoney = dls_deposit_keyMoney[1].find_element_by_tag_name('dd').text
                keyMoney = keyMoney.replace('円', '').replace(',', '')
                # 礼金が「～ヶ月」表記だった場合に賃料との積にする
                if keyMoney[-2:] == 'ヶ月':
                    keyMoney = float(rent) * float(keyMoney.replace('ヶ月', '')) * 10000
                
                # 14.特徴
                ps_features = card_tds[5].find_elements_by_tag_name('p')
                features = ''
                for p_features in ps_features:
                    features += p_features.text
                # 15.検討中人数
                div_user_count = card.find_element_by_class_name('bukken-user-count')
                user_count = div_user_count.find_element_by_tag_name('span').find_element_by_tag_name('span').text
                if user_count == '':
                    user_count = '0'
                
                result_dic_list.append({
                    '物件タイトル':title,
                    '駅からの徒歩':distance,
                    '住所':address,
                    '総階数':floors,
                    '築年数':float(age) if tl.is_num(age) else 0,
                    '建物構造':construction,
                    '駐車場あり':parking,
                    '間取り':layout,
                    '専有面積[㎡]':float(area),
                    '賃料[万円]':float(rent),
                    '管理費等':int(managementFee) if tl.is_num(managementFee) else 0,
                    '敷金':int(deposit) if tl.is_num(deposit) else 0,
                    '礼金':int(keyMoney) if tl.is_num(keyMoney) else 0,
                    '特徴':features,
                    '検討中人数':int(user_count)
                })

                count += 1

            # '>'ボタンが有効なら次のページへ
            exist_next = False
            _next_buttons = driver.find_elements_by_class_name('button')
            for _next_button in _next_buttons:
                if _next_button.text == '>':
                    if _next_button.tag_name != 'a':
                        break
                    elif _next_button.is_enabled():
                        exist_next = True
                        _next_button.click()
                        sleep(random.uniform(2, 3))
                    break

    #    # CSVファイルに出力
    #    output_folder = 'output'
    #    if not os.path.exists(output_folder):
    #        os.mkdir(output_folder)
    #
    #    output_file = '{0}/{1}_{2}_{3}.csv'.format(
    #        output_folder,
    #        datetime.date.today().strftime(r'%Y%m%d'),
    #        input_data['prefecture'],
    #        input_data['city'])
    #    df = pd.DataFrame(result_dic_list)
    #    df.to_csv(output_file, index = False)
    #    print('{0}{1}のデータ取得が完了しました'.format(prefecture, city))

    # 終了
    driver.quit()
    print('全てのデータの取得が終了しました。')

    return result_dic_list