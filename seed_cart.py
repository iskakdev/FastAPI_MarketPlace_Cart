import requests

AUTH_URL = 'http://127.0.0.1:8000/auth/login/'
PRODUCT_URL = 'http://127.0.0.1:8001'
CART_URL = 'http://127.0.0.1:8002'

USERNAME = 'testuser'
PASSWORD = '12345678'


def get_token():
    response = requests.post(AUTH_URL, json={'username': USERNAME, 'password': PASSWORD})
    response.raise_for_status()
    return response.json()['access_token']


def print_result(name, response):
    try:
        print(name, '->', response.status_code, response.json())
    except requests.exceptions.JSONDecodeError:
        print(name, '->', response.status_code, 'RAW:', response.text)


def get_products(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{PRODUCT_URL}/products/', headers=headers)
    return response.json()


def create_cart(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{CART_URL}/carts/', json={}, headers=headers)
    print_result('Создание корзины', response)
    return response.json()


def add_cart_items(token, cart_id, products):
    headers = {'Authorization': f'Bearer {token}'}
    for product in products[:5]:
        item = {'product': product['id'], 'quantity': 1, 'cart_id': cart_id}
        response = requests.post(f'{CART_URL}/cart_items/', json=item, headers=headers)
        print_result(f"{product['product_name']} (product_id={product['id']})", response)


if __name__ == '__main__':
    token = get_token()
    print('Токен получен')

    cart = create_cart(token)
    cart_id = cart['id']
    print(f'ID корзины: {cart_id}')

    products = get_products(token)
    print(f'Найдено товаров: {len(products)}')

    add_cart_items(token, cart_id, products)

    print('Готово!')