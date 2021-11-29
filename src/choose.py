# -*- coding: utf-8 -*-
import logging
import os.path as path
import random

from src.models.buyer import Buyer
from src.models.product import Product
from src.utils import file_util, get_wishlist

log = logging.getLogger()

DATA_PATH = path.join('data')


def main():
    # 購入者を取得
    buyers = file_util.read_csv(path.join(DATA_PATH, 'buyer.csv'))
    # 商品を取得
    products = file_util.read_csv(path.join(DATA_PATH, 'product.csv'))
    # 購入優先度リストを取得
    wishlists = file_util.read_csv(path.join(DATA_PATH, 'wishlist.csv'))

    # モデル生成
    # 購入者と購入優先度の紐付け
    buyer_models: list[Buyer] = []
    for buyer in buyers:
        wishlist = get_wishlist.get_wishlist(buyer['wishlist'], wishlists)
        buyer_model = Buyer(
            id=buyer['id'], name=buyer['name'], wishlist=wishlist)
        buyer_models.append(buyer_model)

    # 商品
    product_models: list[Product] = [
        Product(**product) for product in products]

    # 抽選処理
    # 商品ごとに購入優先度を設定する
    drawings: dict = {product.name: [] for product in product_models}

    # 購入者でループ
    for buyer in buyer_models:
        wishlist = buyer.wishlist
        for product_name, num_of_buy in zip(wishlist.priority, wishlist.number_of_buy):
            # バリデーション
            # 商品に存在しないものは弾く
            if not validate_product(product_name, product_models):
                log.warning(
                    f'選択した商品は存在しません。 購入者={buyer.name}, 商品名={product_name}')
                continue

            # 購入数が多いものは弾く
            if not validate_buy_of_num(num_of_buy):
                log.warning(
                    f'商品2つまでしか購入できません。購入者={buyer.name}, 購入数={num_of_buy}')
                continue

            drawings[product_name].append({
                'buyer': buyer.name,
                'number_of_buy': num_of_buy
            })

    drawing_result: dict = {product.name: [] for product in product_models}
    # 購入優先度順にソート
    for key in drawings:
        # 商品の購入者がいない場合はスキップ
        if len(drawings[key]) == 0:
            # 結果からも消す
            del drawing_result[key]
            continue
        max_number = max(drawings[key], key=lambda x: x['number_of_buy'])[
            'number_of_buy']
        min_number = min(drawings[key], key=lambda x: x['number_of_buy'])[
            'number_of_buy']
        buyers_of_product = drawings[key]
        # 最大値と最小値が混在している場合は最大値をリストから除去する
        if max_number != min_number:
            buyers_of_product = [buyer for buyer in drawings[key]
                                 if buyer['number_of_buy'] == min_number]

        # 1人のみに絞れた場合は終了する
        if len(buyers_of_product) == 1:
            drawing_result[key] = buyers_of_product
            continue

        # 対象者が複数人いる場合は、ランダム選出
        random_buyers = random.sample(
            buyers_of_product, len(buyers_of_product))
        # 2回抽選
        drawing_result[key] = random_buyers[random.randrange(
            len(random_buyers))]

    # TODO 確定枠を作成
    # ダンプ
    import json
    print(json.dumps(drawing_result, ensure_ascii=False, indent=2))


def validate_product(product_name, product_models: list[Product]):
    result = [p.name for p in product_models if p.name == product_name]
    return len(result) != 0


def validate_buy_of_num(buy_of_num):
    return buy_of_num <= 2
