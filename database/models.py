from database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from typing import List


class Cart(Base):
    __tablename__ = 'marketplace_cart'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(Integer, nullable=False)

    cart_item: Mapped[List['CartItem']] = relationship(back_populates='cart',
                                                       cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'marketplace_cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product: Mapped[int] = mapped_column(Integer, nullable=False)  # аналогично
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('marketplace_cart.id'))
    cart: Mapped["Cart"] = relationship(Cart, back_populates='cart_item')
