import pandas as pd
import random

from collections import defaultdict
from datetime import timedelta
from pandas import DataFrame
from constants import START_DATE, DAYS_OF_DATA

class StockManager:
    def __init__(self, products_df: DataFrame, sites_df: DataFrame):
        self.__products_df = products_df
        self.__sites_df = sites_df
        self.__initial_stock_df = None

    @staticmethod
    def __restock(channel:str):
        match channel:
            case 'wholesale':
                restock_limit = 1000
            case 'distributor':
                restock_limit = 500
            case _:
                restock_limit = 250

        restock_qty = random.randint(0, restock_limit) if random.random() < 0.2 else 0  # 20% chance of restock

        return restock_qty

    def generate_first_stock(self):
        stock_data = []

        for _, site in self.__sites_df.iterrows():
            for _, product in self.__products_df.iterrows():

                # Different initial stock based on channel
                if site['channel'] == 'wholesale':
                    stock = random.randint(500, 2500)

                elif site['channel'] == 'distributor':
                    stock = random.randint(200, 1000)

                else:  # retail or self-service
                    stock = random.randint(50, 500)

                stock_data.append({
                    'site_code': site['site_code'],
                    'sku': product['sku'],
                    'stock': stock,
                    'date': START_DATE.strftime('%Y-%m-%d')
                })

        self.__initial_stock_df = pd.DataFrame(stock_data)

    def generate_stock_update_sales(self, sales_df):
        """
        Updates stock day by day, ensuring stock is carried over correctly,
        sales do not exceed stock, and stock is adjusted for losses/restocking.
        """
        stock_dict = defaultdict(int)
        updated_sales = []
        updated_stock = []

        # Load initial stock into dictionary
        for _, row in self.__initial_stock_df.iterrows():
            stock_dict[(row['site_code'], row['sku'], row['date'])] = row['stock']

            # first day of stock is not altered
            updated_stock.append({
                        'site_code': row['site_code'],
                        'sku': row['sku'],
                        'date': row['date'],
                        'stock': row['stock']
                    })

        # Process stock day by day
        for day_offset in range(DAYS_OF_DATA):
            current_date = (START_DATE + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            next_date = (START_DATE + timedelta(days=day_offset + 1)).strftime('%Y-%m-%d')

            # Process sales for the current day
            daily_sales = sales_df[sales_df['date'] == current_date]

            for _, sale in daily_sales.iterrows():
                key = (sale['site_code'], sale['sku'], current_date)
                available_stock = stock_dict.get(key, 0)

                # Ensure sales do not exceed available stock
                actual_sale = min(available_stock, sale['quantity'])

                if actual_sale > 0:
                    updated_sales.append({
                        'date': sale['date'],
                        'site_code': sale['site_code'],
                        'sku': sale['sku'],
                        'quantity': actual_sale
                    })

                # Reduce stock accordingly
                stock_dict[key] = max(0, available_stock - actual_sale)

            # Carry stock to the next day and apply losses/restocking
            for (site_code, sku, date), stock in list(stock_dict.items()):
                if date == current_date:  # Only process today's stock
                    # Apply spoilage (small % loss) and random restocking
                    spoilage = random.uniform(0.97, 1.0)  # 0-3% loss
                    site_channel = self.__sites_df[self.__sites_df ['site_code'] == site_code]['channel'].iloc[0]
                    restock = self.__restock(site_channel)
                    new_stock = max(0, int(stock * spoilage) + restock)

                    # Store next day's stock
                    stock_dict[(site_code, sku, next_date)] = new_stock

                    updated_stock.append({
                        'site_code': site_code,
                        'sku': sku,
                        'date': next_date,
                        'stock': new_stock
                    })

        return pd.DataFrame(updated_stock), pd.DataFrame(updated_sales)
