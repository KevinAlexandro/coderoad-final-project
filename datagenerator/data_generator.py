import pandas as pd
import random

from faker import Faker
from datetime import datetime, timedelta
from collections import defaultdict
from constants import (CATEGORIES, BRAND_NAMES, PACKAGE_TYPES, CITIES, COUNTRIES, CHANNELS, NUM_PRODUCTS, NUM_SITES,
                       DAYS_OF_DATA, START_DATE)
from stock_manager import StockManager


class DataGenerator:

    def __init__(self):
        # Initialize Faker
        self.__faker = Faker()
        self.__run()
    
    # Generate product data
    def __generate_products(self, num_products):
        products = []
        sku_counter = 1000  # Starting SKU
    
        # Ensure we have products in all categories
        base_products_per_category = num_products // len(CATEGORIES)
        remaining_products = num_products % len(CATEGORIES)
    
        for category in CATEGORIES:
            products_to_create = base_products_per_category + (1 if remaining_products > 0 else 0)
    
            if remaining_products > 0:
                remaining_products -= 1
    
            for i in range(products_to_create):
                sku = f"{sku_counter}"
                package_type = random.choice(PACKAGE_TYPES[category])
                brand_name = random.choice(BRAND_NAMES[category])
                barcode = self.__faker.ean13()
    
                products.append({
                    'sku': sku,
                    'category': category,
                    'package_type': package_type,
                    'brand_name': brand_name,
                    'barcode': barcode
                })
    
                sku_counter += 1
    
        return pd.DataFrame(products)
    
    
    # Generate site data
    def __generate_sites(self, num_sites):
        sites = []
        site_code_counter = 100  # Starting site code
    
        for _ in range(num_sites):
            country = random.choice(COUNTRIES)
            city = random.choice(CITIES[country])
            zip_code = self.__faker.postcode()
            channel = random.choice(CHANNELS)
    
            sites.append({
                'site_code': f"{country}{site_code_counter}",
                'country': country,
                'city': city,
                'zip_code': zip_code,
                'channel': channel
            })
    
            site_code_counter += 1
    
        return pd.DataFrame(sites)

    @staticmethod
    def __get_base_sale_quantity(channel: str):
        match channel:
            case 'wholesale':
                base_sales = random.randint(1, 100)
            case 'distributor':
                base_sales = random.randint(1, 50)
            case _:
                base_sales = random.randint(1, 25)

        return base_sales

    @staticmethod
    def __get_final_quantity(base_sales: int, channel: str):
        """
        Convert to integer and ensure at least 0
        """
        match channel:
            case 'wholesale':
                limit_sales_modifier = 20
            case 'distributor':
                limit_sales_modifier = 10
            case _:
                limit_sales_modifier = 5

        return max(0, int(round(base_sales + random.uniform(-limit_sales_modifier, limit_sales_modifier))))
    
    # Generate sales data with realistic trends
    def __generate_sales(self, products_df, sites_df, days_of_data, start_date):
        sales_data = []
        date_range = [start_date + timedelta(days=i) for i in range(days_of_data)]
    
        # Create product popularity index (some products sell better than others)
        product_popularity = {row['sku']: random.uniform(0.5, 2.0) for _, row in products_df.iterrows()}
    
        # Create site activity index (some sites are busier than others)
        site_activity = {row['site_code']: random.uniform(0.7, 1.5) for _, row in sites_df.iterrows()}
    
        # Seasonal multipliers (holidays, etc.)
        seasonal_multipliers = {
            datetime(2024, 12, 25): 2.5,  # Christmas
            datetime(2024, 10, 31): 1.8,  # Halloween
            datetime(2024, 2, 14): 1.6,  # Valentine's
            datetime(2024, 11, 1): 1.4,  # All Saints
            datetime(2024, 5, 12): 1.5,  # Mother's Day
            datetime(2024, 3, 8): 1.3,  # Women's Day
            datetime(2024, 12, 31): 1.8,  # New Year's Eve
            datetime(2024, 2, 13): 1.2  # Carnival
        }
    
        # Weekly pattern (more sales on weekends)
        weekly_pattern = [1.0, 1.0, 1.0, 1.0, 1.2, 1.5, 1.3]  # Mon-Sun
    
        for date in date_range:
            # Get seasonal multiplier
            seasonal_mult = 1.0
            for special_date, mult in seasonal_multipliers.items():
                if (date - special_date).days in range(-3, 4):  # ±3 days around holiday
                    seasonal_mult = mult
                    break

            # Get day of week multiplier
            dow_mult = weekly_pattern[date.weekday()]
    
            for _, site in sites_df.iterrows():
                channel = site['channel']

                for _, product in products_df.iterrows():

                    # Base sales rate
                    #sales number depend on the channel
                    base_sales = self.__get_base_sale_quantity(channel)
    
                    # Adjust for product popularity
                    base_sales *= product_popularity[product['sku']]
    
                    # Adjust for site activity
                    base_sales *= site_activity[site['site_code']]
    
                    # Adjust for seasonality
                    base_sales *= seasonal_mult
    
                    # Adjust for day of week
                    base_sales *= dow_mult
    
                    # Chocolate sells better in winter
                    if product['category'] == 'chocolate' and date.month in [11, 12, 1, 2]:
                        base_sales *= 1.5
    
                    # Gum sells better in summer
                    if product['category'] == 'gum' and date.month in [6, 7, 8]:
                        base_sales *= 1.3

                    quantity = self.__get_final_quantity(base_sales, channel)

                    if quantity > 0:
                        sales_data.append({
                            'date': date.strftime('%Y-%m-%d'),
                            'site_code': site['site_code'],
                            'sku': product['sku'],
                            'quantity': quantity
                        })
    
        return pd.DataFrame(sales_data)

    # Main data generation function
    def __generate_all_data(self):
        print("Generating products...")
        products_df = self.__generate_products(NUM_PRODUCTS)
    
        print("Generating sites...")
        sites_df = self.__generate_sites(NUM_SITES)
    
        print("Generating initial stock...")
        stock_manager = StockManager(products_df, sites_df)
        stock_manager.generate_first_stock()
    
        print("Generating sales data... (this may take a moment)")
        sales_df = self.__generate_sales(products_df, sites_df, DAYS_OF_DATA, START_DATE)
    
        print("Updating stock levels based on sales...")
        # updated_stock_df = self.__update_stock(stock_df, sales_df)
        updated_stock_df, updated_sales = stock_manager.generate_stock_update_sales(sales_df)
    
        return {
            'products': products_df,
            'sites': sites_df,
            'stock': updated_stock_df,
            'sales': updated_sales
        }

    def __run(self):
        data = self.__generate_all_data()

        # Save to CSV files
        data['products'].to_csv('../data/products.csv', index=False)
        data['sites'].to_csv('../data/sites.csv', index=False)
        data['stock'].to_csv('../data/stock.csv', index=False)
        data['sales'].to_csv('../data/sales.csv', index=False)

        print("Data generation complete! Files saved as:")
        print("- products.csv")
        print("- sites.csv")
        print("- stock.csv")
        print("- sales.csv")


# Generate and save all data
if __name__ == "__main__":
    DataGenerator()