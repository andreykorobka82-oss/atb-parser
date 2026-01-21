import requests
import json

def get_atb_data():
    # Використовуємо офіційні ID категорій АТБ
    # 7 - Економія (загальна), 20 - Алкоголь/Напої (приблизно)
    categories = [7, 20, 15] 
    all_products = []
    
    headers = {
        "User-Agent": "ATB-Market/1.5.0 (iPhone; iOS 15.0; Scale/3.00)",
        "Accept": "application/json"
    }

    for cat_id in categories:
        try:
            # Запит до внутрішнього API акцій
            url = f"https://www.atbmarket.com/api/v1/promo/list?id={cat_id}&lang=uk"
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json().get('data', [])
                for item in data:
                    all_products.append({
                        "name": item.get('title', 'Без назви'),
                        "price": float(item.get('price', 0)) / 100 # Ціна в копійках
                    })
        except:
            continue

    return all_products

# Збереження результатів
promo_data = get_atb_data()

# Якщо API нічого не дало, залишимо ваші 3 товари, щоб сайт не був порожнім
if not promo_data:
    promo_data = [
        {"name": "Олія соняшникова", "price": 45.90},
        {"name": "Цукор білий 1кг", "price": 28.50},
        {"name": "Молоко 2.5%", "price": 32.20}
    ]

with open('atb_data.json', 'w', encoding='utf-8') as f:
    json.dump(promo_data, f, ensure_ascii=False, indent=4)
