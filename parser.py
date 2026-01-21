import requests
from bs4 import BeautifulSoup
import json
import time

def get_atb_data():
    session = requests.Session()
    # Крок 1: Заходимо на головну сторінку для отримання куків
    main_url = "https://www.atbmarket.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    try:
        session.get(main_url, headers=headers, timeout=15)
        
        # Крок 2: Збираємо дані з розділів "Акції" та "Спиртні напої"
        # Ми використовуємо API, оскільки воно містить повний перелік товарів
        urls = [
            "https://www.atbmarket.com/api/v1/promo/list?id=7&lang=uk", # Акції "Економія"
            "https://www.atbmarket.com/api/v1/promo/list?id=20&lang=uk" # Алкоголь та напої
        ]
        
        all_products = []
        
        for url in urls:
            response = session.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json().get('data', [])
                for item in data:
                    all_products.append({
                        "name": item.get('title'),
                        "price": float(item.get('price', 0)) / 100
                    })
            time.sleep(2) # Пауза, щоб не заблокували
            
        return all_products
    except Exception as e:
        print(f"Помилка: {e}")
        return []

# Отримуємо та зберігаємо дані
promo_data = get_atb_data()

# Якщо сайт все ще блокує, ми додамо трохи більше товарів у резерв, 
# щоб ви могли перевірити роботу сайту з алкоголем
if not promo_data:
    promo_data = [
        {"name": "Горілка 0.5л (Резерв)", "price": 89.40},
        {"name": "Вино червоне 0.75л (Резерв)", "price": 120.00},
        {"name": "Олія соняшникова", "price": 45.90},
        {"name": "Цукор 1кг", "price": 28.50}
    ]

with open('atb_data.json', 'w', encoding='utf-8') as f:
    json.dump(promo_data, f, ensure_ascii=False, indent=4)
