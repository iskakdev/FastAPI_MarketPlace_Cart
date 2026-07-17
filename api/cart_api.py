from fastapi import APIRouter, Depends, HTTPException
from database.models import Cart
from database.schema import CartInputSchema, CartOutSchema
from database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session
from api.jwt_handler import get_current_user


cart_router = APIRouter(prefix='/carts', tags=['Carts'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cart_router.post('/', response_model=CartOutSchema)
async def create_cart(cart: CartInputSchema, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    cart_db = Cart(user=user_id)
    db.add(cart_db)
    db.commit()
    db.refresh(cart_db)
    return cart_db


@cart_router.get('/', response_model=List[CartOutSchema])
async def list_cart(db: Session = Depends(get_db)):
    return db.query(Cart).all()


@cart_router.get('/{cart_id}/', response_model=CartOutSchema)
async def detail_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)
    return cart_db


@cart_router.put('/{cart_id}/', response_model=dict)
async def update_cart(cart_id: int, cart: CartInputSchema,
                          db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)
    db.commit()
    db.refresh(cart_db)
    return {'massage': 'Корзина успешно изменена!'}


@cart_router.delete('/{cart_id}/', response_model=dict)
async def delete_cart(cart_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(detail='Такого данного нету', status_code=400)
    db.delete(cart_db)
    db.commit()
    return {'massage': 'Категория успешно удалена!'}