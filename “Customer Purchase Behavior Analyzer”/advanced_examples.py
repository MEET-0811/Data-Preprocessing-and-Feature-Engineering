"""
Advanced Examples and Analysis Techniques
Demonstrates sophisticated usage patterns for the Customer Purchase Behavior Analyzer
"""

import pandas as pd
import numpy as np
import json
from customer_purchase_analyzer import CustomerPurchaseBehaviorAnalyzer, FeatureEngineer


class AdvancedAnalysis:
    """Advanced analysis techniques on engineered data"""
    
    def __init__(self, dataframe):
        self.df = dataframe
    
    def customer_segmentation(self):
        """
        Advanced customer segmentation based on RFM and monetary features
        """
        print("\n" + "="*80)
        print("CUSTOMER SEGMENTATION ANALYSIS")
        print("="*80)
        
        # Define segments based on RFM scores
        segment_conditions = {
            'Champions': (
                (self.df['rfm_recency'] < 30) & 
                (self.df['rfm_frequency'] >= 5) & 
                (self.df['rfm_monetary'] >= 500)
            ),
            'Loyal Customers': (
                (self.df['rfm_recency'] < 60) & 
                (self.df['rfm_frequency'] >= 3) & 
                (self.df['rfm_monetary'] >= 300)
            ),
            'At Risk': (
                (self.df['rfm_recency'] > 150) & 
                (self.df['rfm_frequency'] <= 3)
            ),
            'Need Activation': (
                (self.df['rfm_recency'] > 200) & 
                (self.df['purchase_frequency'] == 1)
            )
        }
        
        self.df['customer_segment_advanced'] = 'Other'
        for segment, condition in segment_conditions.items():
            self.df.loc[condition, 'customer_segment_advanced'] = segment
        
        # Print segmentation results
        segment_counts = self.df['customer_segment_advanced'].value_counts()
        print("\nSegmentation Results:")
        for segment, count in segment_counts.items():
            percentage = (count / len(self.df)) * 100
            avg_value = self.df[self.df['customer_segment_advanced'] == segment]['rfm_monetary'].mean()
            print(f"  {segment}: {count} customers ({percentage:.1f}%) - Avg Value: ${avg_value:.2f}")
    
    def cohort_analysis(self):
        """
        Analyze customer cohorts based on acquisition period
        """
        print("\n" + "="*80)
        print("COHORT ANALYSIS")
        print("="*80)
        
        if 'year' in self.df.columns and 'month' in self.df.columns:
            self.df['cohort'] = self.df['year'].astype(str) + '-' + self.df['month'].astype(str).str.zfill(2)
            
            cohort_analysis = self.df.groupby('cohort').agg({
                'transaction_id': 'count',
                'amount': ['sum', 'mean'],
                'customer_id': 'nunique'
            }).round(2)
            
            cohort_analysis.columns = ['Transactions', 'Total_Spending', 'Avg_Transaction', 'Unique_Customers']
            
            print("\nCohort Performance:")
            print(cohort_analysis.head(10).to_string())
    
    def seasonality_analysis(self):
        """
        Analyze seasonal trends in purchasing behavior
        """
        print("\n" + "="*80)
        print("SEASONALITY ANALYSIS")
        print("="*80)
        
        if 'month' in self.df.columns:
            monthly_spending = self.df.groupby('month').agg({
                'amount': ['sum', 'mean', 'count'],
                'customer_id': 'nunique'
            }).round(2)
            
            monthly_spending.columns = ['Total_Spending', 'Avg_Transaction', 'Transactions', 'Unique_Customers']
            
            print("\nMonthly Performance:")
            print(monthly_spending.to_string())
            
            # Identify peak and off-peak months
            peak_month = monthly_spending['Total_Spending'].idxmax()
            off_peak_month = monthly_spending['Total_Spending'].idxmin()
            
            month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                          7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
            
            print(f"\nPeak Month: {month_names.get(peak_month, peak_month)} (${monthly_spending.loc[peak_month, 'Total_Spending']:.2f})")
            print(f"Off-Peak Month: {month_names.get(off_peak_month, off_peak_month)} (${monthly_spending.loc[off_peak_month, 'Total_Spending']:.2f})")
    
    def product_category_analysis(self):
        """
        Analyze performance by product category
        """
        print("\n" + "="*80)
        print("PRODUCT CATEGORY ANALYSIS")
        print("="*80)
        
        if 'product_category' in self.df.columns:
            category_analysis = self.df.groupby('product_category').agg({
                'amount': ['sum', 'mean', 'count'],
                'customer_id': 'nunique',
                'quantity': 'mean'
            }).round(2)
            
            category_analysis.columns = ['Total_Revenue', 'Avg_Transaction', 'Transactions', 'Unique_Customers', 'Avg_Quantity']
            category_analysis = category_analysis.sort_values('Total_Revenue', ascending=False)
            
            print("\nCategory Performance:")
            print(category_analysis.to_string())
            
            # Revenue distribution
            print("\nRevenue Distribution:")
            total_revenue = category_analysis['Total_Revenue'].sum()
            for category, row in category_analysis.iterrows():
                if pd.notna(category):
                    percentage = (row['Total_Revenue'] / total_revenue) * 100
                    print(f"  {category}: {percentage:.1f}% of total revenue")
    
    def customer_lifetime_value(self):
        """
        Calculate and analyze customer lifetime value (CLV)
        """
        print("\n" + "="*80)
        print("CUSTOMER LIFETIME VALUE ANALYSIS")
        print("="*80)
        
        # Group by customer and calculate CLV metrics
        clv_data = self.df.groupby('customer_id').agg({
            'amount': 'sum',
            'rfm_frequency': 'first',
            'customer_age_days': 'first',
            'rfm_recency': 'first'
        }).reset_index()
        
        clv_data.columns = ['customer_id', 'total_lifetime_value', 'purchase_count', 'customer_age_days', 'recency_days']
        
        # Calculate CLV per day
        clv_data['clv_per_day'] = clv_data['total_lifetime_value'] / (clv_data['customer_age_days'] + 1)
        
        # Segmentation by CLV
        clv_data['clv_segment'] = pd.qcut(clv_data['total_lifetime_value'], 
                                          q=4, 
                                          labels=['Low', 'Medium', 'High', 'VIP'],
                                          duplicates='drop')
        
        print("\nCLV Statistics:")
        print(f"  Average CLV: ${clv_data['total_lifetime_value'].mean():.2f}")
        print(f"  Median CLV: ${clv_data['total_lifetime_value'].median():.2f}")
        print(f"  Max CLV: ${clv_data['total_lifetime_value'].max():.2f}")
        print(f"  Min CLV: ${clv_data['total_lifetime_value'].min():.2f}")
        
        print("\nCLV Segments:")
        segment_stats = clv_data.groupby('clv_segment').agg({
            'customer_id': 'count',
            'total_lifetime_value': ['mean', 'min', 'max']
        }).round(2)
        print(segment_stats.to_string())
        
        return clv_data
    
    def churn_risk_analysis(self):
        """
        Identify customers at risk of churning
        """
        print("\n" + "="*80)
        print("CHURN RISK ANALYSIS")
        print("="*80)
        
        if 'rfm_recency' in self.df.columns and 'rfm_frequency' in self.df.columns:
            # Define churn risk based on recency and frequency
            self.df['churn_risk'] = 'Low'
            
            # High risk: High recency (hasn't purchased recently) + Low frequency
            high_risk = (self.df['rfm_recency'] > 180) & (self.df['rfm_frequency'] <= 2)
            self.df.loc[high_risk, 'churn_risk'] = 'High'
            
            # Medium risk: High recency + Medium frequency
            medium_risk = (self.df['rfm_recency'] > 120) & (self.df['rfm_frequency'] <= 4) & ~high_risk
            self.df.loc[medium_risk, 'churn_risk'] = 'Medium'
            
            churn_distribution = self.df['churn_risk'].value_counts()
            print("\nChurn Risk Distribution:")
            for risk_level, count in churn_distribution.items():
                percentage = (count / len(self.df)) * 100
                print(f"  {risk_level}: {count} customers ({percentage:.1f}%)")
            
            # High risk customers analysis
            high_risk_customers = self.df[self.df['churn_risk'] == 'High']
            print(f"\nHigh-Risk Customer Metrics:")
            print(f"  Avg Recency: {high_risk_customers['rfm_recency'].mean():.1f} days")
            print(f"  Avg Frequency: {high_risk_customers['rfm_frequency'].mean():.1f} purchases")
            print(f"  Avg Lifetime Value: ${high_risk_customers['rfm_monetary'].mean():.2f}")


def example_1_custom_preprocessing():
    """Example: Custom preprocessing workflow"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Custom Preprocessing Workflow")
    print("="*80)
    
    analyzer = CustomerPurchaseBehaviorAnalyzer()
    
    # Load data with custom configuration
    custom_config = {
        'remove_duplicates': True,
        'duplicate_subset': ['customer_id', 'purchase_date', 'amount'],
        'missing_values_strategy': {
            'amount': 'median',
            'product_category': 'constant'
        },
        'outlier_columns': ['amount'],
        'outlier_method': 'zscore',
        'outlier_threshold': 3.0,
        'type_mapping': {
            'purchase_date': 'datetime',
            'customer_id': 'string'
        }
    }
    
    analyzer.load_data({
        'transactions': 'data/transactions.csv'
    })
    
    analyzer.preprocess_data(custom_config)
    
    print(f"Dataset processed: {analyzer.processed_data.shape}")
    print(f"Original size: {analyzer.raw_data.shape[0]} rows")
    print(f"Processed size: {analyzer.processed_data.shape[0]} rows")


def example_2_feature_extraction():
    """Example: Extract and analyze specific features"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Feature Extraction and Analysis")
    print("="*80)
    
    # Load engineered data
    engineered_df = pd.read_csv('output/customer_behavior_engineered.csv')
    
    # Analyze feature distributions
    feature_cols = [col for col in engineered_df.columns if 'rfm_' in col or 'is_' in col]
    
    print(f"\nFeature Statistics:")
    for col in feature_cols[:5]:
        if engineered_df[col].dtype in ['int64', 'float64']:
            print(f"  {col}:")
            print(f"    Mean: {engineered_df[col].mean():.2f}")
            print(f"    Median: {engineered_df[col].median():.2f}")
            print(f"    Std Dev: {engineered_df[col].std():.2f}")


def example_3_advanced_analysis():
    """Example: Run advanced analysis suite"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Advanced Analysis Suite")
    print("="*80)
    
    # Load engineered data
    engineered_df = pd.read_csv('output/customer_behavior_engineered.csv')
    
    analysis = AdvancedAnalysis(engineered_df)
    
    # Run analyses
    analysis.customer_segmentation()
    analysis.seasonality_analysis()
    analysis.product_category_analysis()
    clv_data = analysis.customer_lifetime_value()
    analysis.churn_risk_analysis()


if __name__ == '__main__':
    print("\n")
    print("████████████████████████████████████████████████████████████████████████████████")
    print("   ADVANCED EXAMPLES - Customer Purchase Behavior Analyzer")
    print("████████████████████████████████████████████████████████████████████████████████")
    
    # Run examples
    example_1_custom_preprocessing()
    example_2_feature_extraction()
    example_3_advanced_analysis()
    
    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("="*80)
