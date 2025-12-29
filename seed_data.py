from typing import List
import asyncio


async def seed_products(products_collection):
    """Seed the database with initial product data"""
    
    sample_products = [
        {
            "name": "Classic Cotton T-Shirt",
            "description": "Comfortable and breathable cotton t-shirt perfect for everyday wear. Made from 100% organic cotton with a relaxed fit.",
            "price": 599.0,
            "originalPrice": 799.0,
            "discount": 25,
            "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500",
            "images": [
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500",
                "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=500"
            ],
            "category": "T-Shirts",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["White", "Black", "Navy", "Gray"],
            "fabric": "Cotton",
            "rating": 4.5,
            "reviews": 128,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 3
        },
        {
            "name": "Denim Jacket",
            "description": "Stylish denim jacket with a vintage wash. Features classic button closure and multiple pockets.",
            "price": 2499.0,
            "originalPrice": 3499.0,
            "discount": 29,
            "image": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=500",
            "images": [
                "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=500",
                "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=500"
            ],
            "category": "Jackets",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Blue", "Black", "Light Blue"],
            "fabric": "Denim",
            "rating": 4.3,
            "reviews": 89,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 5
        },
        {
            "name": "Formal Dress Shirt",
            "description": "Crisp white dress shirt perfect for office wear and formal occasions. Non-iron fabric for easy care.",
            "price": 1299.0,
            "originalPrice": 1799.0,
            "discount": 28,
            "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500",
            "images": [
                "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500",
                "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500"
            ],
            "category": "Shirts",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["White", "Light Blue", "Pink"],
            "fabric": "Cotton Blend",
            "rating": 4.7,
            "reviews": 156,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 2
        },
        {
            "name": "Casual Chinos",
            "description": "Comfortable chino pants suitable for both casual and semi-formal occasions. Slim fit design.",
            "price": 1899.0,
            "originalPrice": 2499.0,
            "discount": 24,
            "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500",
            "images": [
                "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500",
                "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500"
            ],
            "category": "Pants",
            "sizes": ["28", "30", "32", "34", "36"],
            "colors": ["Khaki", "Navy", "Black", "Olive"],
            "fabric": "Cotton Twill",
            "rating": 4.4,
            "reviews": 203,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 4
        },
        {
            "name": "Wool Sweater",
            "description": "Cozy wool sweater perfect for winter. Features ribbed cuffs and hem with a classic crew neck design.",
            "price": 3299.0,
            "originalPrice": 4299.0,
            "discount": 23,
            "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500",
            "images": [
                "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500",
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500"
            ],
            "category": "Sweaters",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Gray", "Navy", "Burgundy", "Cream"],
            "fabric": "Wool",
            "rating": 4.6,
            "reviews": 94,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 6
        },
        {
            "name": "Summer Polo Shirt",
            "description": "Breathable polo shirt ideal for summer. Made with moisture-wicking fabric and classic collar design.",
            "price": 899.0,
            "originalPrice": 1299.0,
            "discount": 31,
            "image": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500",
            "images": [
                "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500",
                "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500"
            ],
            "category": "Polo",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["White", "Navy", "Red", "Green"],
            "fabric": "Pique Cotton",
            "rating": 4.2,
            "reviews": 167,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 3
        },
        {
            "name": "Leather Boots",
            "description": "Genuine leather boots with durable construction. Perfect for both casual and semi-formal wear.",
            "price": 4999.0,
            "originalPrice": 6999.0,
            "discount": 29,
            "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
            "images": [
                "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
                "https://images.unsplash.com/photo-1608256246200-53e8b47b2dc1?w=500"
            ],
            "category": "Footwear",
            "sizes": ["7", "8", "9", "10", "11"],
            "colors": ["Brown", "Black", "Tan"],
            "fabric": "Leather",
            "rating": 4.8,
            "reviews": 76,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 7
        },
        {
            "name": "Athletic Shorts",
            "description": "Lightweight athletic shorts with moisture-wicking technology. Perfect for workouts and sports activities.",
            "price": 799.0,
            "originalPrice": 999.0,
            "discount": 20,
            "image": "https://images.unsplash.com/photo-1506629905607-45c8e8e5b5b3?w=500",
            "images": [
                "https://images.unsplash.com/photo-1506629905607-45c8e8e5b5b3?w=500",
                "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500"
            ],
            "category": "Shorts",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Black", "Navy", "Gray", "Red"],
            "fabric": "Polyester Blend",
            "rating": 4.3,
            "reviews": 142,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 2
        },
        {
            "name": "Casual Hoodie",
            "description": "Comfortable pullover hoodie with kangaroo pocket. Made from soft cotton blend for ultimate comfort.",
            "price": 1799.0,
            "originalPrice": 2299.0,
            "discount": 22,
            "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500",
            "images": [
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500",
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500"
            ],
            "category": "Hoodies",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Gray", "Black", "Navy", "Maroon"],
            "fabric": "Cotton Blend",
            "rating": 4.5,
            "reviews": 198,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 4
        },
        {
            "name": "Formal Blazer",
            "description": "Elegant formal blazer suitable for business meetings and special occasions. Tailored fit with premium fabric.",
            "price": 5999.0,
            "originalPrice": 7999.0,
            "discount": 25,
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500",
            "images": [
                "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500",
                "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500"
            ],
            "category": "Blazers",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Navy", "Black", "Charcoal"],
            "fabric": "Wool Blend",
            "rating": 4.7,
            "reviews": 67,
            "inStock": True,
            "freeDelivery": True,
            "deliveryDays": 5
        }
    ]
    
    # Insert all products
    result = await products_collection.insert_many(sample_products)
    print(f"Inserted {len(result.inserted_ids)} products into the database")
    return result.inserted_ids


if __name__ == "__main__":
    # This can be used to run seeding independently if needed
    import os
    from motor.motor_asyncio import AsyncIOMotorClient
    from dotenv import load_dotenv
    from pathlib import Path
    
    ROOT_DIR = Path(__file__).parent
    load_dotenv(ROOT_DIR / '.env')
    
    async def main():
        mongo_url = os.environ['MONGO_URL']
        client = AsyncIOMotorClient(mongo_url)
        db = client[os.environ['DB_NAME']]
        products_collection = db.products
        
        await seed_products(products_collection)
        client.close()
    
    asyncio.run(main())