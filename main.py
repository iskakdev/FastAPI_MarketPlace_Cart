from fastapi import FastAPI
from api import cart_api, cart_item_api
import uvicorn

marketplace_app = FastAPI(title='MarketPLace FastAPI Cart')
marketplace_app.include_router(cart_api.cart_router)
marketplace_app.include_router(cart_item_api.cart_item_router)


if __name__ == '__main__':
    uvicorn.run(marketplace_app, host='127.0.0.1', port=8002)
