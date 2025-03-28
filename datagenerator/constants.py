from datetime import datetime

NUM_PRODUCTS = 5
NUM_SITES = 20
DAYS_OF_DATA = 1827  # 5 years
START_DATE = datetime(2020, 1, 1)
COUNTRIES = ['US', 'MX', 'CA', 'CO', 'EC', 'PE']
CITIES = {
    'US': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'MX': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana'],
    'CA': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
    'CO': ['Bogota', 'Cali', 'Medellin', 'Barranquilla', 'Cartagena'],
    'EC': ['Quito', 'Guayaquil', 'Cuenca', 'Manta', 'Loja'],
    'PE': ['Lima', 'Arequipa', 'Cusco', 'Iquitos', 'Trujillo']
}

# Product catalog setup
CATEGORIES = ['lollipop', 'chocolate', 'marshmallow', 'candy', 'gum']

# 18 package types
PACKAGE_TYPES = {
    'lollipop': ['single', '10 piece pack', '20 piece pack'],
    'chocolate': ['single', '6 pack', '12 pack', '50 units box'],
    'marshmallow': ['single', '12 piece pack', '24 piece pack'],
    'candy': ['single', '10 piece pack', '25 piece pack', '50 units box'],
    'gum': ['single', '5 pack', '10 pack', '50 units box']
}

# 15 brand names
BRAND_NAMES = {
    'lollipop': ['Sweet Swirl', 'Rainbow Pops', 'Fruit Licks'],
    'chocolate': ['Cocoa Delight', 'Milk Magic', 'Dark Dream'],
    'marshmallow': ['Fluffy Clouds', 'Sweet Puffs', 'Mallow Magic'],
    'candy': ['Fruit Burst', 'Sugar Drops', 'Jelly Joy'],
    'gum': ['Fresh Chew', 'Bubble Mania', 'Minty Pop']
}

CHANNELS = ['distributor', 'retailer', 'self-service', 'wholesaler']