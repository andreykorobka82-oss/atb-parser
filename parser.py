import requests
from bs4 import BeautifulSoup
import json

def get_atb_data():
    url = "https://www.atbmarket.com/promo/economy"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        # Пошук карток товарів
        items = soup.find_all('article', class_='promo-inventory-item')

        for item in items:
            try:
                name_tag = item.find('a', class_='promo-inventory-item__title')
                price_main = item.find('span', class_='price__main')
                price_cents = item.find('span', class_='price__cents')

                if name_tag and price_main:
                    name = name_tag.get_text(strip=True)
                    p_main = price_main.get_text(strip=True)
                    p_cents = price_cents.get_text(strip=True) if price_cents else "00"
                    
                    products.append({
                        "name": name,
                        "price": float(f"{p_main}.{p_cents}")
                    })
            except Exception:
                continue
        
        return products
    except Exception as e:
        print(f"Критична помилка: {e}")
        return []

data = get_atb_data()
if data:
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Знайдено {len(data)} товарів.")
else:
    print("Дані не знайдено.")
