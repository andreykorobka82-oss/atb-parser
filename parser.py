import requests
from bs4 import BeautifulSoup
import json

def get_atb_data():
    # Сторінка з усіма акційними товарами "Економія"
    url = "https://www.atbmarket.com/promo/economy"
    
    # Заголовки, щоб сайт бачив у нас звичайний браузер
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        # Шукаємо всі блоки, які можуть бути картками товарів
        # Ми шукаємо за тегом 'article', який АТБ використовує для товарів
        items = soup.find_all('article', class_='promo-inventory-item')
        
        # Якщо нічого не знайшли за 'article', шукаємо будь-які блоки з ціною
        if not items:
            items = soup.select('.promo-inventory-item, .product-card')

        for item in items:
            try:
                # Шукаємо назву (вона зазвичай у посиланні або заголовку)
                name_tag = item.find('a', class_='promo-inventory-item__title') or item.find('div', class_='title')
                
                # Шукаємо ціну (основна частина та копійки окремо)
                price_main_tag = item.find('span', class_='price__main')
                price_cents_tag = item.find('span', class_='price__cents')

                if name_tag and price_main_tag:
                    name = name_tag.get_text(strip=True)
                    p_main = price_main_tag.get_text(strip=True)
                    p_cents = price_cents_tag.get_text(strip=True) if price_cents_tag else "00"
                    
                    # Чистимо ціну від зайвих пробілів чи символів
                    p_main = "".join(filter(str.isdigit, p_main))
                    p_cents = "".join(filter(str.isdigit, p_cents))

                    products.append({
                        "name": name,
                        "price": float(f"{p_main}.{p_cents}")
                    })
            except Exception:
                continue
        
        return products
    except Exception as e:
        print(f"Помилка: {e}")
        return []

# Отримуємо дані
data = get_atb_data()

# Записуємо лише якщо ми реально щось знайшли
if data:
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Успіх! Знайдено {len(data)} товарів.")
else:
    # Якщо пусто, запишемо тестовий товар, щоб перевірити чи працює сайт
    test_data = [{"name": "Перевірка: Товари не знайдені, оновіть парсер", "price": 0.01}]
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    print("Товари на сайті не знайдено.")
