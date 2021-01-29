# coding: utf-8

import requests
import json
import cli_ui as cli

class StockChecker:

    products = []
    store_id: int

    def __init__(self, api_url):
        """api_url: eg: https://iows.ikea.com/retail/iows/fr/fr/stores/%d/availability/ART"""
        self.api_url = api_url

    def get_availability(self, ref: str):
        headers = {
            'accept': 'application/vnd.ikea.iows+json;version=1.0',
            'contract': '37249',
            'consumer': 'MAMMUT#pip-range'
        }
        # xxx.xxx.xxx -> xxxxxxxxx
        ref = ref.replace('.', '')
        r = requests.get(self.api_url + '/' + ref, headers=headers)
        return r.json()

    def printAll(self):
        rows = []

        for product in self.products:
            ref = product['ref']
            name = product['name']
            stock = product['StockAvailability']['RetailItemAvailability']['AvailableStock']['$']
            location = product['StockAvailability']['RetailItemAvailability']['RecommendedSalesLocation']['$']
            stock_forcast = product['StockAvailability']['AvailableStockForecastList']['AvailableStockForecast']

            if 'RestockDateTime' in product['StockAvailability']['RetailItemAvailability']:
                restock_date = product['StockAvailability']['RetailItemAvailability']['RestockDateTime']['$']
            else:
                restock_date = '-'

            row = [
                (cli.reset, ref),
                (cli.reset, name),
                (cli.green if stock != '0' else cli.red, stock), 
                (cli.reset, self.format_location(location)),
                (cli.blue, restock_date)
            ]
            for forcast in stock_forcast:
                row.append((cli.reset, forcast['AvailableStock']['$']))

            rows.append(row)
        
        headers = ['Ref', 'Name', 'Stock', 'Location', 'Restock date', 'D+1', 'D+2', 'D+3', 'D+4']
        cli.info_table(rows, headers=headers)

    def format_location(self, rawPlace: str) -> str:
        """Format the place when located in the warehouse"""
        if not isinstance(rawPlace, str):
            return str(rawPlace)[0:2] + " " + str(rawPlace)[2:4]

        return rawPlace

    def ask_ref(self):
        ref = cli.ask_string('Add a reference number (xxx.xxx.xxx)')
        name = cli.ask_string('Display name (optionnal)')
        self.add_ref(ref, name)
            
    def add_ref(self, ref: str, name: str = None):
        product = self.get_availability(ref)
        product['ref'] = ref
        product['name'] = name if name != None else '-'
        self.products.append(product)