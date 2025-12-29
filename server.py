from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
import logging
import uuid
from bson import ObjectId

from models import (
    Product, User, Cart, Wishlist, Order,
    SignupRequest, LoginRequest, AuthResponse,
    AddToCartRequest, UpdateCartRequest, RemoveFromCartRequest,
    AddToWishlistRequest, CreateOrderRequest
)
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)

# ==============================
# Logging
# ==============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vstore-backend")

# ==============================
# Environment Variables (Render)
# ==============================
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URL or not DB_NAME:
    raise RuntimeError("Missing required environment variables (MONGO_URL, DB_NAME)")

# ==============================
# MongoDB
# ==============================
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

products_collection = db.products
users_collection = db.users
cart_collection = db.cart
wishlist_collection = db.wishlist
orders_collection = db.orders

# ==============================
# FastAPI App
# ==============================
app = FastAPI(title="vstore club API")

# ==============================
# CORS (Allow frontend for now)
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Router
# ==============================
api_router = APIRouter(prefix="/api")

# ==============================
# Helpers
# ==============================
def product_helper(product: dict) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "originalPrice": product["originalPrice"],
        "discount": product["discount"],
        "image": product["image"],
        "images": product["images"],
        "category": product["category"],
        "sizes": product["sizes"],
        "colors": product["colors"],
        "fabric": product["fabric"],
        "rating": product["rating"],
        "reviews": product["reviews"],
        "inStock": product.get("inStock", True),
        "freeDelivery": product.get("freeDelivery", True),
        "deliveryDays": product["deliveryDays"],
    }


def user_helper(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
    }

# ==============================
# Health Check
# ==============================
@app.get("/")
async def root():
    return {"status": "Backend running"}

# ==============================
# Products
# ==============================
@api_router.get("/products")
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
):
    query = {}

    if category and category != "All":
        query["category"] = category

    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
        ]

    products = await products_collection.find(query).to_list(100)
    return [product_helper(p) for p in products]


@api_router.get("/products/{product_id}")
async def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_helper(product)

# ==============================
# Auth
# ==============================
@api_router.post("/auth/signup", response_model=AuthResponse)
async def signup(data: SignupRequest):
    if await users_collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = {
        "name": data.name,
        "email": data.email,
        "password": get_password_hash(data.password),
        "phone": data.phone,
    }

    result = await users_collection.insert_one(user)
    user["_id"] = result.inserted_id

    token = create_access_token({"sub": str(user["_id"])})
    return {"token": token, "user": user_helper(user)}


@api_router.post("/auth/login", response_model=AuthResponse)
async def login(data: LoginRequest):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})
    return {"token": token, "user": user_helper(user)}


@api_router.get("/auth/profile")
async def profile(user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

# ==============================
# Cart
# ==============================
@api_router.get("/cart")
async def get_cart(user_id: str = Depends(get_current_user)):
    cart = await cart_collection.find_one({"userId": user_id})
    return cart or {"items": []}


@api_router.post("/cart/add")
async def add_to_cart(data: AddToCartRequest, user_id: str = Depends(get_current_user)):
    await cart_collection.update_one(
        {"userId": user_id},
        {"$push": {"items": data.dict()}},
        upsert=True,
    )
    return {"message": "Item added to cart"}

# ==============================
# Wishlist
# ==============================
@api_router.post("/wishlist/add")
async def add_to_wishlist(data: AddToWishlistRequest, user_id: str = Depends(get_current_user)):
    await wishlist_collection.update_one(
        {"userId": user_id},
        {"$addToSet": {"productIds": data.productId}},
        upsert=True,
    )
    return {"message": "Wishlist updated"}

# ==============================
# Orders
# ==============================
@api_router.post("/orders")
async def create_order(data: CreateOrderRequest, user_id: str = Depends(get_current_user)):
    order_id = f"ORD{uuid.uuid4().hex[:8].upper()}"
    order = data.dict()
    order.update({"orderId": order_id, "userId": user_id, "status": "confirmed"})
    await orders_collection.insert_one(order)
    await cart_collection.update_one({"userId": user_id}, {"$set": {"items": []}})
    return {"orderId": order_id}

# ==============================
# Register Router
# ==============================
app.include_router(api_router)

# ==============================
# Startup / Shutdown
# ==============================
@app.on_event("startup")
async def startup():
    try:
        count = await products_collection.count_documents({})
        if count == 0:
            from seed_data import seed_products
            await seed_products(products_collection)
            logger.info("Database seeded")
    except Exception as e:
        logger.error(f"Startup error: {e}")


@app.on_event("shutdown")
async def shutdown():
    client.close()
