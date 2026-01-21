import requests
from bs4 import BeautifulSoup
import json
import time
import random

def get_atb_data():
    # Використовуємо пряме посилання на розділ акцій
    url = "https://www.atbmarket.com/promo/economy"
    
    # Створюємо сесію, щоб сайт думав, що ми людина
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://www.google.com/"
    }
    
    try:
        # Невелика випадкова пауза перед запитом
        time.sleep(random.uniform(2, 5))
        
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        # Шукаємо товари (АТБ використовує тег article з певним класом)
        items = soup.find_all('article', class_='promo-inventory-item')
        
        if not items:
            # Спроба знайти через інший селектор, якщо структура змінилась
            items = soup.select('article')

        for item in items:
            try:
                name_tag = item.find('a', class_='promo-inventory-item__title')
                price_main = item.find('span', class_='price__main')
                price_cents = item.find('span', class_='price__cents')

                if name_tag and price_main:
                    name = name_tag.get_text(strip=True)
                    # Видаляємо все крім цифр
                    p_main = "".join(filter(str.isdigit, price_main.get_text(strip=True)))
                    p_cents = "".join(filter(str.isdigit, price_cents.get_text(strip=True))) if price_cents else "00"
                    
                    products.append({
                        "name": name,
                        "price": float(f"{p_main}.{p_cents}")
                    })
            except:
                continue
        
        return products
    except Exception as e:
        print(f"Помилка: {e}")
        return []

# Отримуємо дані
data = get_atb_data()

# Якщо нічого не знайшли, спробуємо хоча б зберегти статус
if not data:
    print("Сайт АТБ повернув порожню сторінку. Можливо, блок за IP.")
    # Можна залишити старий файл, щоб не затирати дані порожнечею
else:
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Готово! Знайдено {len(data)} товарів.")
