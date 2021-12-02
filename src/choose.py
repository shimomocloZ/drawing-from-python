# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import random

from migrations.models.buyer import Buyers
from migrations.models.product import Products
from migrations.models.reserved_product import ReservedProducts
from migrations.models.wishlist import Wishlists  # noqa E401
from migrations.setting import Session

log = logging.getLogger()


def main():
    # 購入者を取得
    buyers: list[Buyers] = Buyers.query.all()
    # 商品を取得
    products: list[Products] = Products.query.all()

    # 抽選処理
    # 商品ごとに購入優先度を設定する
    current_drawings: dict = create_current_drawings(buyers, products)
    # 商品購入者を決定する
    drawing_result: dict = create_drawing_result(current_drawings, products)
    # 確定枠を作成
    save_reserved_products(drawing_result)
    # 結果をファイルに出力する
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open(os.path.join('data', f'drawing_result_{now}.json'), 'w', encoding='utf8') as f:
        json.dump(drawing_result, f, ensure_ascii=False, indent=2)

    print('finish!')


def create_current_drawings(buyers: list[Buyers], products: list[Products]) -> dict:
    current_drawings = create_drawings_dict(products)
    for buyer in buyers:
        # 購入優先度を取得
        wishlist: Wishlists = buyer.wishlist
        priorities = convert_priority(wishlist.priority)
        numbers_of_buy = convert_number_of_buy(wishlist.number_of_buy)
        for product_name, num_of_buy in zip(priorities, numbers_of_buy):
            # バリデーション
            # 商品に存在しないものは弾く
            if not validate_product(product_name, products):
                log.warning(
                    f'選択した商品は存在しません。 購入者={buyer.name}, 商品名={product_name}')
                continue

            # 購入数が多いものは弾く
            if not validate_buy_of_num(num_of_buy):
                log.warning(
                    f'商品2つまでしか購入できません。購入者={buyer.name}, 購入数={num_of_buy}')
                continue

            current_drawings[product_name].append({
                'buyer': buyer.name,
                'number_of_buy': num_of_buy
            })

    return current_drawings


def create_drawing_result(current_drawings: dict, products: list[Products]):
    drawing_result: dict = create_drawings_dict(products)
    # 購入優先度順にソート
    for product_name in current_drawings.keys():
        # 商品の購入者がいない場合はスキップ
        if len(current_drawings[product_name]) == 0:
            # 結果からも消す
            del drawing_result[product_name]
            continue
        # 商品がすでに購入者が確定している場合、新規購入者を受け付けない
        reserved = fetch_reserved_product_by_product_name(product_name)
        if len(reserved) == 1:
            reserved_dict = {
                'buyer': reserved[0].buyer_name,
                'number_of_buy': reserved[0].number_of_buy
            }
            drawing_result[product_name] = reserved_dict
            continue

        confirm_buyer, only = choose_buyer(current_drawings, product_name)
        if only:
            drawing_result[product_name] = confirm_buyer[0]
            continue

        # 対象者が複数人いる場合は、ランダム選出
        drawing_result[product_name] = choose_random_buyer(confirm_buyer)

    return drawing_result


def create_drawings_dict(products: list[Products]) -> dict:
    return {product.name: [] for product in products}


def validate_product(product_name, product_models: list[Products]):
    result = [p.name for p in product_models if p.name == product_name]
    return len(result) != 0


def validate_buy_of_num(num_of_buy):
    return num_of_buy <= 2


def convert_priority(priority: str):
    return priority.split(';')


def convert_number_of_buy(number_of_buy: str):
    if ';' not in number_of_buy:
        return [int(number_of_buy)]

    return [int(num) for num in number_of_buy.split(';')]


def choose_buyer(current_drawings: dict, product_name: str):
    max_number = max(current_drawings[product_name], key=lambda x: x['number_of_buy'])[
        'number_of_buy']
    min_number = min(current_drawings[product_name], key=lambda x: x['number_of_buy'])[
        'number_of_buy']
    buyers_of_product = current_drawings[product_name]
    # 最大値と最小値が混在している場合は最大値をリストから除去する
    if max_number != min_number:
        buyers_of_product = [buyer for buyer in current_drawings[product_name]
                             if buyer['number_of_buy'] == min_number]

    # 一人に絞れたらTrue, 複数人の場合はFalse
    return buyers_of_product, len(buyers_of_product) == 1


def choose_random_buyer(confirm_buyer: list[dict]):
    # シャッフル
    random_buyers = random.sample(confirm_buyer, len(confirm_buyer))
    # 取得するインデックスもランダム
    return random_buyers[random.randrange(len(random_buyers))]


def fetch_reserved_product_by_product_name(product_name: str) -> list[ReservedProducts]:
    reserved = ReservedProducts.query.filter(
        ReservedProducts.product_name == product_name)
    rows: list[ReservedProducts] = [row for row in reserved]
    return rows


def save_reserved_products(drawing_result: dict) -> None:
    # 一回全部消す
    ReservedProducts.query.delete()
    reserved_products = []
    for product_name in drawing_result.keys():
        buyer_name = drawing_result[product_name]['buyer']
        number_of_buy = drawing_result[product_name]['number_of_buy']
        reserved_product = ReservedProducts()
        reserved_product.product_name = product_name
        reserved_product.buyer_name = buyer_name
        reserved_product.number_of_buy = number_of_buy
        reserved_products.append(reserved_product)

    Session.add_all(reserved_products)
    Session.commit()
