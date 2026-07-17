from pydantic import BaseModel


class CartInputSchema(BaseModel):
    pass


class CartOutSchema(BaseModel):
    id: int
    user: int


class CartItemInputSchema(BaseModel):
    product: int
    quantity: int
    cart_id: int


class CartItemOutSchema(BaseModel):
    product: int
    quantity: int
    cart_id: int