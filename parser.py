import requests
from bs4 import BeautifulSoup
import json

def get_atb_promotions():
    # URL сторінки акцій "Економія"
    url = "https://www.atbmarket.com/promo/economy"
    
    # Розширені заголовки, щоб сайт не зрозумів, що ми бот
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.atbmarket.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Помилка запиту: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    # АТБ часто змінює класи. Спробуємо знайти всі контейнери, що схожі на товари
    # Шукаємо за загальним класом товару
    items = soup.find_all(['article', 'div'], class_='promo-inventory-item')

    for item in items:
        try:
            # Пошук назви
            name_tag = item.find('a', class_='promo-inventory-item__title')
            if not name_tag:
                name_tag = item.find('span', class_='title')
            
            # Пошук ціни (основна частина та копійки)
            price_main = item.find('span', class_='price__main')
            price_cents = item.find('span', class_='price__cents')

            if name_tag and price_main:
                name = name_tag.get_text(strip=True)
                # Чистимо ціну від зайвих символів
                p_main = price_main.get_text(strip=True)
                p_cents = price_cents.get_text(strip=True) if price_cents else "00"
                
                full_price = float(f"{p_main}.{p_cents}")
                
                products.append({
                    "name": name,
                    "price": full_price
                })
        except Exception as e:
            continue

    return products

# Зберігаємо результат
promo_data = get_atb_promotions()

# Додаємо перевірку: якщо список порожній, не перезаписуємо файл повністю або виводимо помилку
if promo_data:
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(promo_data, f, ensure_ascii=False, indent=4)
    print(f"Успішно оновлено! Знайдено товарів: {len(promo_data)}")
else:
    print("Помилка: Товари не знайдені. Перевірте структуру сайту.")
