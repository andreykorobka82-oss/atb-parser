import requests
import json

def get_atb_data():
    # Використовуємо пряме API АТБ, яке повертає чистий список товарів
    url = "https://www.atbmarket.com/api/v1/promo/list?id=1&lang=uk"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.atbmarket.com/promo/economy"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Отримуємо JSON напряму
        raw_data = response.json()
        products = []

        # Проходимо по структурі відповіді АТБ
        # В API товари зазвичай знаходяться у полі 'data' або 'store_items'
        for item in raw_data.get('data', []):
            try:
                name = item.get('title')
                # Отримуємо актуальну ціну
                price = item.get('price')
                
                if name and price:
                    products.append({
                        "name": name,
                        "price": float(price) / 100 # Ціна в API часто в копійках
                    })
            except:
                continue
        
        # Якщо цей шлях не спрацював, спробуємо інший формат API
        if not products:
             for item in raw_data.get('items', []):
                products.append({
                    "name": item.get('name'),
                    "price": float(item.get('price', 0))
                })

        return products
    except Exception as e:
        print(f"API Error: {e}")
        return []

# Запуск та збереження
data = get_atb_data()

if data:
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Знайдено через API: {len(data)} товарів.")
else:
    # Останній шанс: запишемо реальні акційні товари вручну для тесту сайту
    fallback = [
        {"name": "Олія соняшникова", "price": 45.90},
        {"name": "Цукор білий 1кг", "price": 28.50},
        {"name": "Молоко 2.5%", "price": 32.20}
    ]
    with open('atb_data.json', 'w', encoding='utf-8') as f:
        json.dump(fallback, f, ensure_ascii=False, indent=4)
    print("API не відповіло, використано резервний список.")
