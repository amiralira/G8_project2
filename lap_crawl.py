import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.exceptions import RequestException
from tqdm import tqdm
from time import sleep

# urls = ["https://torob.com/p/9d81bca4-aa7f-4620-a75c-6c9f850a7d12/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D8%A7%D9%85-%D8%A7%D8%B3-%D8%A7%DB%8C-gf63-thin-11ucx-a/"]
# url = "https://torob.com/p/c9e081d5-cc85-4cd5-98d3-116aa2b9aba2/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%84%D9%86%D9%88%D9%88-ideapad-3-4gb-ram-1tb-hdd-n4020/"
headerss = {
            # "Accept-Encoding": "en-US,en;q=0.9,fa;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
            # 'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}

marker = pd.read_json('forwarded.json', orient='records')
marker = marker['num_of_fw'][0]
urls = pd.read_csv('links.csv')
urls = urls.loc[marker:, 'links']

ab_urls = []
reasone = []

data = {
  'model_name': [],
  'prices': [],
  'brands': [],
  'categories': [],
  'counteries': [],
  'sizes': [],
  'weight': [],
  'body_type': [],
  'colors': [],
  'cpu_com': [],
  'cpu_series': [],
#   'cpu_gen': [],
  'cpu_model': [],
  'freq_base': [],
  'freq_plus': [],
  'freq': [],
  'cache': [],
  'num_cores': [],
#   'num_v_cores': [],
#   'num_threads': [],
  'power_cpu': [],  # Power Needed CPU
  'resolution': [],
  'rams': [],
  'ram_type': [],
#   'ram_bus': [],
#   'ram_slots': [],
#   'ram_up': [],
  'storage_type': [],
  'storage': [],
#   'storage_connection': [],
#   'storage_slots': [],
#   'sec_storage_type': [],
  'sec_storage': [],
  'gpu_com': [],
#   'gpu_type': [],
  'gpu_model': [],
  'gpu_cap': [],
#   'gpu_ram': [],
#   'gpu_power': [],
#   'DirX': [],
#   'pcie': [],
  'panel_sizes': [],
#   'panel_type': [], # پنل تصویر یا نوع صفحه
  'clarity': [], # وضوح تصویر یا فرمت صفحه نمایش
  'framrate': [],
#   'response_time': [],
  'ratio_pic': [],
#   'sze': [],
  'nits': [],
#   'srgb': [],
#   'type_c': [],
  'usbs': [],
  'battery': [],
  'battery_type': [],
#   'charging': [],
  'adaptor_power': [],
#   'webcam': [],
#   'fingerprint': [],
  'keyboard_light': [],
  'speaker': [],
#   'jack': [],
#   'bt': [],
  'windows': []
}


counter = 0
for bar, url in zip(tqdm(range(marker, len(urls) + 1), colour="GREEN"), urls):
    # if counter == 300:
    #     break
    if counter % 25 == 0:
        sleep(.75)
    try:
        response = requests.get(url, headers=headerss, timeout=10)
    except RequestException as e:
        print("Error: {}".format(e))
        ab_urls.append(url)
        reasone.append('Conncection Error')
        sleep(1)
        continue
    # response = requests.get(url, headers=headerss)
    lap_soup = BeautifulSoup(response.text, 'html.parser')
    miane = lap_soup.find('div', {'id': 'layout-wrapp'})
    both = miane.find('div', {'class': 'jsx-ec6258a0ede3ee2d jsx-260973103 grid-container grid-container-with-seller'})
    if both == None:
        continue
    all_lap = both.find('div', {'class': 'jsx-e4c635b60934fea7 product-sector'})
    product_info = both.find('div', {'class': 'jsx-5b5c456cc255c2dc sub-section'})
    if product_info == None:
        continue
    target = all_lap.find_next('div', {'class': 'jsx-528815776 shop-card seller-element'}).find_next('div', {'class': 'jsx-528815776 shop-card seller-element'})
    if target != None:
        toman = target.find('div', {'class': 'jsx-528815776 purchase-info seller-element'}).find('a')
        if toman.text[-1] == 'ن':
            r_toman = int(toman.text.replace('تومان', '').replace('٫', ''))
        else:
            r_toman = toman.text
        main = both.find('div', {'class': 'jsx-63b317fab2efbae main-info'})
        model = main.find('h1', {'class': 'jsx-63b317fab2efbae'}).text
        data['model_name'].append(model)
    else:
        continue

    data['prices'].append(r_toman)

    informations = product_info.find_all('div', {'class': 'jsx-5b5c456cc255c2dc'})
    for info in informations:
        example = info.text

        if example[:6] == 'کاربری':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                category = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                category = category.split(',')
                data['categories'].append(category)
        elif example[:4] == 'برند':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                brand = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['brands'].append(brand)
        elif example[:14] == 'مقدار حافظه رم' or example[:15] == 'ظرفیت حافظه RAM':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                ram = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['rams'].append(ram)
        elif example[:6] == 'نوع رم' or example[:13] == 'نوع حافظه RAM':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                ram_t = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['ram_type'].append(ram_t)
        elif example[:15] == 'نوع حافظه داخلی':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                stor_t = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['storage_type'].append(stor_t)
        elif example[:9] == 'ظرفیت SSD' or example[:11] == 'ظرفیت حافظه' or example[:9] == 'هارد دیسک' or example[:17] == 'ظرفیت حافظه داخلی':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                stor = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['storage'].append(stor)
        elif example[:18] == 'شرکت سازنده گرافیک' or example[:23] == 'سازنده پردازنده گرافیکی':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                g_com = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['gpu_com'].append(g_com)
        elif example[:20] == 'مدل پردازنده گرافیکی' or example[:10] == 'مدل گرافیک':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                g_mod = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['gpu_model'].append(g_mod)
        elif example[:10] == 'حجم گرافیک' or example[:30] == 'حافظه اختصاصی پردازنده گرافیکی':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                g_cap = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['gpu_cap'].append(g_cap)
        elif example[:15] == 'سایز صفحه نمایش' or example[:17] == 'اندازه صفحه نمایش':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                p_size = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['panel_sizes'].append(p_size)
        elif example[:4] == 'کشور':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                countery = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                # category = category.split(',')
                data['counteries'].append(countery)
        elif example[:21] == 'ظرفیت حافظه داخلی دوم':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                sec_st = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['sec_storage'].append(sec_st)
        elif example[:5] == 'ابعاد':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                size = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                # category = category.split(',')
                data['sizes'].append(size)
        elif example[:3] == 'وزن':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                weigh = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                # category = category.split(',')
                data['weight'].append(weigh)
        elif example[:3] == 'رنگ':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                color = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['colors'].append(color)
        elif example[:8] == 'جنس بدنه' or example[:17] == 'ساختار و جنس بدنه':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                b_type = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['body_type'].append(b_type)
        elif example[:20] == 'شرکت سازنده پردازنده' or example[:15] == 'سازنده پردازنده':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                c_com = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['cpu_com'].append(c_com)
        elif example[:12] == 'سری پردازنده':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                c_ser = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['cpu_series'].append(c_ser)
        elif example[:3] == 'مدل' or example[:12] == 'مدل پردازنده':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                c_model = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['cpu_model'].append(c_model)
        elif example[:16] == 'تعداد هسته حقیقی' or example[:10] == 'تعداد هسته':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                n_core = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['num_cores'].append(n_core)
        # elif example[:16] == 'تعداد هسته مجازی':
        #     if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
        #         n_core = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
        #         data['num_v_cores'].append(n_core)
        elif example[:11] == 'حافظه Cache' or example[:8] == 'حافظه کش':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                cach = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['cache'].append(cach)
        elif example[:20] == 'محدوده سرعت پردازنده':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                fre = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['freq'].append(fre)
        elif example[:11] == 'فرکانس پایه':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                f_base = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                if "MHz" in f_base:
                    continue
                data['freq_base'].append(f_base)
        elif example[:14] == 'فرکانس افزایشی':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                f_ince = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                if "MHz" in f_ince:
                    continue
                data['freq_plus'].append(f_ince)
        elif example[:10] == 'تعداد رشته':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                n_thred = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['freq_plus'].append(n_thred)
        elif example[:17] == 'مصرف برق پردازنده':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                pow_c = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['power_cpu'].append(pow_c)
        elif example[:15] == 'فرمت صفحه نمایش' or example[:10] == 'وضوح تصویر':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                clar = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['clarity'].append(clar)
        elif example[:7] == 'رزولوشن':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                res = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['resolution'].append(res)
        elif example[:9] == 'نرخ تصویر':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                hz = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['framrate'].append(hz)
        # elif example[:13] == 'زمان پاسخگویی':
        #     if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
        #         r_time = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
        #         data['response_time'].append(r_time)
        elif example[:10] == 'نسبت تصویر':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                r_pic = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['ratio_pic'].append(r_pic)
        elif example[:11] == 'شدت روشنایی' or example[:13] == 'میزان روشنایی':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                bright = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['nits'].append(bright)
        # elif example[:6] == 'Type-C' or example[:10] == 'تعداد پورت':
        #     if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
        #         port_c = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
        #         data['type_c'].append(port_c)
        elif example[:5] == 'USB 3' or 'USB3 3.2' in example[:20]:
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                usb = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['usbs'].append(usb)
        elif example[:11] == 'ظرفیت و نوع' or example[:11] == 'ظرفیت باتری':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                cap = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['battery'].append(cap)
        elif example[:9] == 'جنس باتری' or example[:9] == 'نوع باتری':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                type_bat = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['battery_type'].append(type_bat)
        elif example[:9] == 'توان آداپتور':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                adap_pow = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['adaptor_power'].append(adap_pow)
        elif example[:20] == 'نوع نمایش نور کیبورد' or example[:22] == 'کیبورد با نور پس زمینه':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                key_light = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['keyboard_light'].append(key_light)
        elif example[:12] == 'تعداد اسپیکر':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                num_speak = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['speaker'].append(num_speak)
        elif example[:10] == 'سیستم عامل':
            if info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}) != None:
                win = info.find('div', {'class': 'jsx-5b5c456cc255c2dc detail-value'}).text
                data['windows'].append(win)
    for key, value in data.items():
        if len(value) < len(data['model_name']):
            data[key].append(None)
        elif len(value) > len(data['model_name']):
            data[key].pop(-1)

    counter += 1


for key, value in data.items():
    print(key, len(value))

dataframe = pd.DataFrame(data=data)
if marker > 0:
    dataframe.to_csv('torob_lap.csv', encoding='utf-8-sig', header=False, mode='a')
else:
    dataframe.to_csv('torob_lap.csv', encoding='utf-8-sig')

abondoned_lap = pd.DataFrame({'abondoned': ab_urls,
                              'reason': reasone})
abondoned_lap.to_csv('ab_laptop.csv', mode='a', header=False)
print(counter)
cn = pd.DataFrame([{'num_of_fw': counter + marker}])
cn.to_json('forwarded.json')