"""
Generate sample data for Customer Purchase Behavior Analyzer testing
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random

def generate_sample_data(output_dir: str = 'data', num_customers: int = 500, num_transactions: int = 2000):
    """Generate sample datasets for analysis"""
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    print("Generating sample data...")
    
    # 1. Generate customer data
    print("  - Generating customer data...")
    customer_ids = [f"CUST_{i:05d}" for i in range(1, num_customers + 1)]
    
    customers = {
        'customer_id': customer_ids,
        'age': np.random.randint(18, 75, num_customers),
        'location': np.random.choice(['North', 'South', 'East', 'West', 'Central'], num_customers),
        'customer_segment': np.random.choice(['Premium', 'Standard', 'Budget', 'VIP'], num_customers),
        'registration_date': [datetime.now() - timedelta(days=random.randint(1, 730)) for _ in range(num_customers)]
    }
    
    customers_df = pd.DataFrame(customers)
    customers_df.to_csv(f'{output_dir}/customers.csv', index=False)
    
    # Also save as JSON for testing multi-format loading
    customers_df['registration_date'] = customers_df['registration_date'].astype(str)
    customers_json = customers_df.to_dict('records')
    with open(f'{output_dir}/customers.json', 'w') as f:
        json.dump(customers_json, f, indent=2, default=str)
    
    # 2. Generate transaction data
    print("  - Generating transaction data...")
    
    transactions = []
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty', 'Groceries', 'Toys']
    
    for _ in range(num_transactions):
        customer_id = random.choice(customer_ids)
        purchase_date = datetime.now() - timedelta(days=random.randint(1, 365))
        amount = np.random.gamma(shape=2, scale=50) + 10  # Realistic spending distribution
        quantity = random.randint(1, 5)
        category = random.choice(categories)
        
        # Add some missing values naturally
        product_category = category if random.random() > 0.05 else None
        
        transactions.append({
            'transaction_id': len(transactions) + 1,
            'customer_id': customer_id,
            'purchase_date': purchase_date,
            'amount': round(amount, 2),
            'quantity': quantity,
            'product_category': product_category,
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Wallet']),
            'discount_applied': random.random() > 0.7
        })
    
    transactions_df = pd.DataFrame(transactions)
    transactions_df['purchase_date'] = transactions_df['purchase_date'].astype(str)
    transactions_df.to_csv(f'{output_dir}/transactions.csv', index=False)
    
    # 3. Generate product categories (for Excel file)
    print("  - Generating product categories...")
    
    categories_data = {
        'category_name': categories,
        'avg_price': [400, 60, 80, 100, 20, 40, 15, 25],
        'inventory': np.random.randint(50, 500, len(categories)),
        'last_updated': [datetime.now() - timedelta(days=random.randint(1, 30)) for _ in range(len(categories))]
    }
    
    categories_df = pd.DataFrame(categories_data)
    categories_df['last_updated'] = categories_df['last_updated'].astype(str)
    
    # Save as Excel
    try:
        categories_df.to_excel(f'{output_dir}/categories.xlsx', index=False)
    except Exception as e:
        print(f"  Note: Could not save Excel file (openpyxl may not be installed): {e}")
        categories_df.to_csv(f'{output_dir}/categories.csv', index=False)
    
    print(f"\nSample data generated successfully:")
    print(f"  - Customers: {len(customers_df)} records")
    print(f"  - Transactions: {len(transactions_df)} records")
    print(f"  - Categories: {len(categories_df)} records")
    print(f"  - Output directory: {output_dir}/")
    
    return customers_df, transactions_df, categories_df


if __name__ == '__main__':
    generate_sample_data()
