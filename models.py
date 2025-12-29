from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Product(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    price: float
    originalPrice: float
    discount: int
    image: str
    images: List[str]
    category: str
    sizes: List[str]
    colors: List[str]
    fabric: str
    rating: float
    reviews: int
    inStock: bool = True
    freeDelivery: bool = True
    deliveryDays: int
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: EmailStr
    password: str
    phone: str
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class CartItem(BaseModel):
    productId: str
    selectedSize: str
    quantity: int


class Cart(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    userId: str
    items: List[CartItem]
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class Wishlist(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    userId: str
    productIds: List[str]
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class ShippingAddress(BaseModel):
    fullName: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str


class OrderItem(BaseModel):
    productId: str
    productName: str
    productImage: str
    selectedSize: str
    quantity: int
    price: float


class Order(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    orderId: str
    userId: str
    items: List[OrderItem]
    shippingAddress: ShippingAddress
    paymentMethod: str
    subtotal: float
    deliveryCharge: float
    totalAmount: float
    status: str = "pending"
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


# Request/Response Models
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    user: dict


class AddToCartRequest(BaseModel):
    productId: str
    selectedSize: str
    quantity: int = 1


class UpdateCartRequest(BaseModel):
    productId: str
    selectedSize: str
    quantity: int


class RemoveFromCartRequest(BaseModel):
    productId: str
    selectedSize: str


class AddToWishlistRequest(BaseModel):
    productId: str


class CreateOrderRequest(BaseModel):
    items: List[OrderItem]
    shippingAddress: ShippingAddress
    paymentMethod: str
    subtotal: float
    deliveryCharge: float
    totalAmount: float
