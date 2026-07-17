from fastapi import APIRouter, Depends, HTTPException
from database.models import CartItem
from database.schema import CartItemInputSchema, CartItemOutSchema
from database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session
from api.jwt_handler import get_current_user
from api.product_client import get_product


cart_item_router = APIRouter(prefix='/cart_items', tags=['Cart Items'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cart_item_router.post('/', response_model=CartItemOutSchema)
async def create_cart_item(cart_item: CartItemInputSchema, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    await get_product(cart_item.product)
    cart_item_db = CartItem(**cart_item.dict())
    db.add(cart_item_db)
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db


@cart_item_router.get('/', response_model=List[CartItemOutSchema])
async def list_cart_item(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


@cart_item_router.get('/{cart_item_id}/', response_model=CartItemOutSchema)
async def detail_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)
    return cart_item_db


@cart_item_router.put('/{cart_item_id}/', response_model=dict)
async def update_cart(cart_item_id: int, cart: CartItemInputSchema,
                          db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)
    for cart_key, cart_value in cart.dict().items():
        setattr(cart_item_db, cart_key, cart_value)
    db.commit()
    db.refresh(cart_item_db)
    return {'massage': 'Корзина успешно изменена!'}


@cart_item_router.delete('/{cart_item_id}/', response_model=dict)
async def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)
    db.delete(cart_item_db)
    db.commit()
    return {'massage': 'Категория успешно удалена!'}