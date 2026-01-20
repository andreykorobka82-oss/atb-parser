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

# Оновлений блок пошуку в parser.py
items = soup.find_all('div', class_='promo-inventory-item') # спробуйте div замість article

for item in items:
    try:
        # Більш гнучкий пошук назви та ціни
        name_tag = item.find('a', class_='promo-inventory-item__title') or item.find('div', class_='title')
        price_int_tag = item.find('span', class_='price__main')
        price_frac_tag = item.find('span', class_='price__cents')

        if name_tag and price_int_tag:
            name = name_tag.text.strip()
            price = f"{price_int_tag.text.strip()}.{price_frac_tag.text.strip() if price_frac_tag else '00'}"
            products.append({"name": name, "price": float(price)})
    except Exception as e:
        print(f"Помилка при обробці товару: {e}")

# Зберігаємо результат у JSON файл, який зможе прочитати ваш HTML
promo_data = get_atb_promotions()
with open('atb_data.json', 'w', encoding='utf-8') as f:
    json.dump(promo_data, f, ensure_ascii=False, indent=4)

print(f"Знайдено {len(promo_data)} акційних товарів. Дані оновлено!")

import time
# ... у циклі додайте:

time.sleep(1) # пауза 1 секунда між сторінками
