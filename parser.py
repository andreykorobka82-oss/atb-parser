import requests
from bs4 import BeautifulSoup
import json

def get_atb_promotions():
    url = "https://www.atbmarket.com/promo/economy"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Не вдалося отримати дані з сайту")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    # Шукаємо картки товарів (селектори можуть змінюватися залежно від коду сайту)
    items = soup.find_all('article', class_='promo-inventory-item')

    for item in items:
        try:
            name = item.find('a', class_='promo-inventory-item__title').text.strip()
            price_integer = item.find('span', class_='price__main').text.strip()
            price_fraction = item.find('span', class_='price__cents').text.strip()
            full_price = f"{price_integer}.{price_fraction}"
            
            products.append({
                "name": name,
                "price": float(full_price)
            })
        except AttributeError:
            continue

    return products

# Зберігаємо результат у JSON файл, який зможе прочитати ваш HTML
promo_data = get_atb_promotions()
with open('atb_data.json', 'w', encoding='utf-8') as f:
    json.dump(promo_data, f, ensure_ascii=False, indent=4)

print(f"Знайдено {len(promo_data)} акційних товарів. Дані оновлено!")

import time
# ... у циклі додайте:
time.sleep(1) # пауза 1 секунда між сторінками