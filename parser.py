import requests
from bs4 import BeautifulSoup
import json

def get_atb_promotions():
    url = "https://www.atbmarket.com/promo/economy"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        # Актуальні селектори для АТБ
        items = soup.find_all('article', class_='promo-inventory-item')

        for item in items:
            try:
                name = item.find('a', class_='promo-inventory-item__title').get_text(strip=True)
                # Отримуємо ціну (основна частина + копійки)
                price_main = item.find('span', class_='price__main').get_text(strip=True)
                price_cents = item.find('span', class_='price__cents').get_text(strip=True)
                
                products.append({
                    "name": name,
                    "price": float(f"{price_main}.{price_cents}")
                })
            except:
                continue
        return products
    except Exception as e:
        print(f"Error: {e}")
        return []

promo_data = get_atb_promotions()
if promo_data:
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(promo_data, f, ensure_ascii=False, indent=4)
