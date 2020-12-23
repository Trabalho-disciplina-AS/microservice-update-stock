from flask import request, jsonify
from stock.services.stock_service import get_quantity, insert_product
from flask_restful import Resource
from stock import app, api
from random import randrange
import json
import requests
from time import sleep
from datetime import datetime


class UpdateStockController(Resource):
    def get(self):
        while True:
            # Get all products
            all_products = requests.get(f"http://localhost:5005/products").json()

            # Get all qtd_stock of products
            for product in all_products:
                qtd_stock = requests.get(
                    f"http://localhost:5010/stock/{product['_id']['$oid']}"
                ).json()
                data = {
                    "id": product["_id"]["$oid"],
                    "qtd_stock": qtd_stock["quantity"],
                }
                requests.post(
                    "http://localhost:5005/products/qtd_stock", json=data
                ).json()

            sleep(10)
            print(datetime.now())

        return {"quantity": randrange(9)}, 200


api.add_resource(UpdateStockController, "/update_stock/")
