"""
Main execution script for Customer Purchase Behavior Analyzer
Demonstrates the complete data preprocessing and feature engineering pipeline
"""

import json
import os
from pathlib import Path
from customer_purchase_analyzer import CustomerPurchaseBehaviorAnalyzer
from generate_sample_data import generate_sample_data


def main():
    """Execute the complete analysis pipeline"""
    
    print("=" * 80)
    print("CUSTOMER PURCHASE BEHAVIOR ANALYZER")
    print("Data Preprocessing and Feature Engineering Pipeline")
    print("=" * 80)
    print()
    
    # Step 1: Generate sample data
    print("STEP 1: Generating Sample Data")
    print("-" * 80)
    
    data_dir = 'data'
    output_dir = 'output'
    
    # Create directories
    Path(data_dir).mkdir(exist_ok=True)
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate sample data
    customers_df, transactions_df, categories_df = generate_sample_data(data_dir)
    print()
    
    # Step 2: Load configuration
    print("STEP 2: Loading Configuration")
    print("-" * 80)
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    print("Preprocessing Configuration:")
    print(f"  - Remove duplicates: {config['preprocessing']['remove_duplicates']}")
    print(f"  - Handle missing values: {len(config['preprocessing']['missing_values_strategy'])} columns")
    print(f"  - Handle outliers: {len(config['preprocessing']['outlier_columns'])} columns")
    print(f"  - Type conversions: {len(config['preprocessing']['type_mapping'])} columns")
    
    print("\nFeature Engineering Configuration:")
    feature_config = config['feature_engineering']
    print(f"  - Monetary features: {'enabled' if feature_config.get('monetary_features') else 'disabled'}")
    print(f"  - Temporal features: {'enabled' if feature_config.get('temporal_features') else 'disabled'}")
    print(f"  - Customer lifecycle: {'enabled' if feature_config.get('customer_lifecycle_features') else 'disabled'}")
    print(f"  - Purchase frequency: {'enabled' if feature_config.get('frequency_features') else 'disabled'}")
    print(f"  - Category features: {'enabled' if feature_config.get('category_features') else 'disabled'}")
    print(f"  - RFM features: {'enabled' if feature_config.get('rfm_features') else 'disabled'}")
    print()
    
    # Step 3: Initialize analyzer and load data
    print("STEP 3: Loading Data from Multiple Sources")
    print("-" * 80)
    
    analyzer = CustomerPurchaseBehaviorAnalyzer()
    
    # Map config file paths to actual paths
    file_paths = {
        'transactions': os.path.join(data_dir, 'transactions.csv'),
        'customers': os.path.join(data_dir, 'customers.json')
    }
    
    # Try to load Excel, fall back to CSV if not available
    excel_path = os.path.join(data_dir, 'categories.xlsx')
    csv_path = os.path.join(data_dir, 'categories.csv')
    
    if os.path.exists(excel_path):
        file_paths['categories'] = excel_path
    elif os.path.exists(csv_path):
        file_paths['categories'] = csv_path
    
    analyzer.load_data(file_paths)
    
    raw_summary = analyzer.raw_data.describe()
    print(f"Raw data loaded: {analyzer.raw_data.shape}")
    print(f"Columns: {list(analyzer.raw_data.columns)}")
    print()
    
    # Step 4: Preprocess data
    print("STEP 4: Data Preprocessing")
    print("-" * 80)
    
    preprocessing_config = config['preprocessing']
    analyzer.preprocess_data(preprocessing_config)
    
    print(f"Processed data shape: {analyzer.processed_data.shape}")
    print(f"Rows removed: {analyzer.raw_data.shape[0] - analyzer.processed_data.shape[0]}")
    print(f"Missing values remaining: {analyzer.processed_data.isnull().sum().sum()}")
    print()
    
    # Step 5: Engineer features
    print("STEP 5: Feature Engineering")
    print("-" * 80)
    
    feature_engineering_config = config['feature_engineering']
    analyzer.engineer_features(feature_engineering_config)
    
    feature_summary = analyzer.pipeline_config.get('feature_summary', {})
    print(f"Engineered data shape: {analyzer.engineered_data.shape}")
    print(f"Total engineered features: {feature_summary.get('total_features', 0)}")
    print(f"New features added: {feature_summary.get('total_features', 0)}")
    
    if feature_summary.get('engineered_features'):
        print(f"Engineered feature list:")
        for feature in feature_summary['engineered_features'][:10]:
            print(f"  - {feature}")
        if len(feature_summary['engineered_features']) > 10:
            print(f"  ... and {len(feature_summary['engineered_features']) - 10} more")
    print()
    
    # Step 6: Data Quality Report
    print("STEP 6: Data Quality Report")
    print("-" * 80)
    
    engineered_df = analyzer.engineered_data
    
    print(f"Dataset Statistics:")
    print(f"  - Total rows: {len(engineered_df)}")
    print(f"  - Total columns: {len(engineered_df.columns)}")
    print(f"  - Data types: {engineered_df.dtypes.value_counts().to_dict()}")
    print(f"  - Missing values: {engineered_df.isnull().sum().sum()}")
    print(f"  - Duplicate rows: {engineered_df.duplicated().sum()}")
    
    # Numeric columns summary
    numeric_cols = engineered_df.select_dtypes(include=['int64', 'float64']).columns
    print(f"\nNumeric Columns Summary ({len(numeric_cols)} total):")
    
    numeric_summary = engineered_df[numeric_cols].describe()
    print(numeric_summary.to_string())
    print()
    
    # Step 7: Save results
    print("STEP 7: Saving Results")
    print("-" * 80)
    
    analyzer.save_results(output_dir)
    
    print(f"Results saved to '{output_dir}/' directory:")
    print(f"  - customer_behavior_engineered.csv (main dataset)")
    print(f"  - pipeline_config.json (pipeline configuration)")
    print()
    
    # Step 8: Sample output
    print("STEP 8: Sample Output Data")
    print("-" * 80)
    
    print("\nFirst 5 rows of engineered data:")
    sample_columns = [col for col in engineered_df.columns if col not in ['source']][:10]
    print(engineered_df[sample_columns].head(5).to_string())
    print()
    
    # Step 9: Summary statistics
    print("STEP 9: Feature Analysis Summary")
    print("-" * 80)
    
    # Analyze RFM if available
    if 'rfm_monetary' in engineered_df.columns:
        print("\nRFM Analysis (sample):")
        rfm_cols = [col for col in engineered_df.columns if col.startswith('rfm_')]
        for col in rfm_cols:
            if engineered_df[col].dtype in ['int64', 'float64']:
                print(f"  {col}:")
                print(f"    Mean: {engineered_df[col].mean():.2f}")
                print(f"    Median: {engineered_df[col].median():.2f}")
                print(f"    Min: {engineered_df[col].min():.2f}")
                print(f"    Max: {engineered_df[col].max():.2f}")
    
    # Customer segments
    if 'frequency_category' in engineered_df.columns:
        print("\nCustomer Frequency Distribution:")
        freq_dist = engineered_df['frequency_category'].value_counts()
        for category, count in freq_dist.items():
            print(f"  {category}: {count} ({count/len(engineered_df)*100:.1f}%)")
    
    # High-value customers
    if 'is_high_value' in engineered_df.columns:
        high_value_count = engineered_df['is_high_value'].sum()
        print(f"\nHigh-Value Customers: {high_value_count} ({high_value_count/len(engineered_df)*100:.1f}%)")
    
    print()
    print("=" * 80)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    return analyzer


if __name__ == '__main__':
    analyzer = main()
