"""
Customer Purchase Behavior Analyzer
A comprehensive data preprocessing and feature engineering pipeline for analyzing customer purchase patterns.

Author: Data Engineering Team
Date: 2026
"""

import pandas as pd
import numpy as np
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load data from multiple formats (CSV, JSON, Excel)"""
    
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Load CSV file"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded CSV: {file_path} ({len(df)} rows)")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def load_json(file_path: str) -> pd.DataFrame:
        """Load JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            df = pd.json_normalize(data) if isinstance(data, list) else pd.DataFrame([data])
            logger.info(f"Loaded JSON: {file_path} ({len(df)} rows)")
            return df
        except Exception as e:
            logger.error(f"Error loading JSON {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def load_excel(file_path: str, sheet_name: str = 0) -> pd.DataFrame:
        """Load Excel file"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded Excel: {file_path} ({len(df)} rows)")
            return df
        except Exception as e:
            logger.error(f"Error loading Excel {file_path}: {str(e)}")
            raise


class DataPreprocessor:
    """Handle data cleaning and preprocessing"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_shape = df.shape
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_rows = len(self.df)
        self.df.drop_duplicates(subset=subset, keep='first', inplace=True)
        removed = initial_rows - len(self.df)
        logger.info(f"Removed {removed} duplicate rows")
        return self
    
    def handle_missing_values(self, strategy: Dict[str, str] = None) -> pd.DataFrame:
        """
        Handle missing values based on strategy
        
        Strategy options:
        - 'drop': Remove rows with missing values
        - 'mean': Fill with mean (numeric columns)
        - 'median': Fill with median (numeric columns)
        - 'forward_fill': Forward fill
        - 'backward_fill': Backward fill
        - 'constant': Fill with constant value
        """
        if strategy is None:
            strategy = {}
        
        missing_before = self.df.isnull().sum().sum()
        
        for col, method in strategy.items():
            if col in self.df.columns:
                if method == 'drop':
                    self.df.dropna(subset=[col], inplace=True)
                elif method == 'mean' and self.df[col].dtype in ['float64', 'int64']:
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif method == 'median' and self.df[col].dtype in ['float64', 'int64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                elif method == 'forward_fill':
                    self.df[col].fillna(method='ffill', inplace=True)
                elif method == 'backward_fill':
                    self.df[col].fillna(method='bfill', inplace=True)
                elif isinstance(method, (int, float, str)):
                    self.df[col].fillna(method, inplace=True)
        
        missing_after = self.df.isnull().sum().sum()
        logger.info(f"Handled missing values: {missing_before} -> {missing_after}")
        return self
    
    def handle_outliers(self, columns: List[str], method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Handle outliers using IQR or Z-score method
        
        Args:
            columns: List of columns to check for outliers
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier (default 1.5) or Z-score threshold (default 3)
        """
        for col in columns:
            if col in self.df.columns and self.df[col].dtype in ['float64', 'int64']:
                if method == 'iqr':
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    before = len(self.df)
                    self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
                    logger.info(f"Removed {before - len(self.df)} outliers in {col}")
                
                elif method == 'zscore':
                    z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                    before = len(self.df)
                    self.df = self.df[z_scores < threshold]
                    logger.info(f"Removed {before - len(self.df)} outliers in {col}")
        
        return self
    
    def convert_data_types(self, type_mapping: Dict[str, str]) -> pd.DataFrame:
        """Convert columns to specified data types"""
        for col, dtype in type_mapping.items():
            if col in self.df.columns:
                try:
                    if dtype == 'datetime':
                        self.df[col] = pd.to_datetime(self.df[col])
                    elif dtype == 'category':
                        self.df[col] = self.df[col].astype('category')
                    else:
                        self.df[col] = self.df[col].astype(dtype)
                    logger.info(f"Converted {col} to {dtype}")
                except Exception as e:
                    logger.warning(f"Could not convert {col} to {dtype}: {str(e)}")
        return self
    
    def clean_text_columns(self, columns: List[str]) -> pd.DataFrame:
        """Clean text columns (strip, lowercase, remove special chars)"""
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.lower()
                self.df[col] = self.df[col].str.replace(r'[^a-z0-9\s]', '', regex=True)
                logger.info(f"Cleaned text column: {col}")
        return self
    
    def get_processed_data(self) -> pd.DataFrame:
        """Return processed dataframe"""
        logger.info(f"Data shape: {self.original_shape} -> {self.df.shape}")
        return self.df


class FeatureEngineer:
    """Create and engineer features for analysis"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.engineered_features = []
    
    def create_monetary_features(self, amount_col: str, transaction_col: str = None) -> pd.DataFrame:
        """Create monetary-based features"""
        if amount_col in self.df.columns:
            # Total spending
            if transaction_col and transaction_col in self.df.columns:
                self.df['total_spending'] = self.df.groupby(transaction_col)[amount_col].transform('sum')
            
            # Spending quantiles
            self.df['spending_quartile'] = pd.qcut(self.df[amount_col], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'], duplicates='drop')
            
            # High-value customer flag
            threshold = self.df[amount_col].quantile(0.75)
            self.df['is_high_value'] = (self.df[amount_col] >= threshold).astype(int)
            
            self.engineered_features.extend(['total_spending', 'spending_quartile', 'is_high_value'])
            logger.info("Created monetary features")
        return self
    
    def create_temporal_features(self, date_col: str) -> pd.DataFrame:
        """Create time-based features"""
        if date_col in self.df.columns:
            if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
                self.df[date_col] = pd.to_datetime(self.df[date_col])
            
            self.df['year'] = self.df[date_col].dt.year
            self.df['month'] = self.df[date_col].dt.month
            self.df['quarter'] = self.df[date_col].dt.quarter
            self.df['day_of_week'] = self.df[date_col].dt.day_name()
            self.df['is_weekend'] = self.df[date_col].dt.dayofweek.isin([5, 6]).astype(int)
            self.df['is_holiday_season'] = self.df['month'].isin([11, 12]).astype(int)
            
            self.engineered_features.extend(['year', 'month', 'quarter', 'day_of_week', 'is_weekend', 'is_holiday_season'])
            logger.info("Created temporal features")
        return self
    
    def create_customer_lifecycle_features(self, customer_col: str, date_col: str) -> pd.DataFrame:
        """Create customer lifecycle features"""
        if customer_col in self.df.columns and date_col in self.df.columns:
            if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
                self.df[date_col] = pd.to_datetime(self.df[date_col])
            
            # First purchase date
            first_purchase = self.df.groupby(customer_col)[date_col].min()
            self.df['first_purchase_date'] = self.df[customer_col].map(first_purchase)
            
            # Last purchase date
            last_purchase = self.df.groupby(customer_col)[date_col].max()
            self.df['last_purchase_date'] = self.df[customer_col].map(last_purchase)
            
            # Customer age (days since first purchase)
            self.df['customer_age_days'] = (self.df[date_col] - self.df['first_purchase_date']).dt.days
            
            # Recency (days since last purchase)
            reference_date = self.df[date_col].max()
            self.df['recency_days'] = (reference_date - self.df['last_purchase_date']).dt.days
            
            self.engineered_features.extend(['first_purchase_date', 'last_purchase_date', 'customer_age_days', 'recency_days'])
            logger.info("Created customer lifecycle features")
        return self
    
    def create_frequency_features(self, customer_col: str) -> pd.DataFrame:
        """Create purchase frequency features"""
        if customer_col in self.df.columns:
            # Number of purchases per customer
            purchase_frequency = self.df[customer_col].value_counts()
            self.df['purchase_frequency'] = self.df[customer_col].map(purchase_frequency)
            
            # Frequency category
            self.df['frequency_category'] = pd.cut(
                self.df['purchase_frequency'],
                bins=[-np.inf, 1, 5, 10, np.inf],
                labels=['One-time', 'Occasional', 'Regular', 'VIP']
            )
            
            self.engineered_features.extend(['purchase_frequency', 'frequency_category'])
            logger.info("Created frequency features")
        return self
    
    def create_category_features(self, category_col: str) -> pd.DataFrame:
        """Create category-based features"""
        if category_col in self.df.columns:
            # One-hot encoding
            category_dummies = pd.get_dummies(self.df[category_col], prefix='category')
            self.df = pd.concat([self.df, category_dummies], axis=1)
            
            self.engineered_features.extend(category_dummies.columns.tolist())
            logger.info(f"Created {len(category_dummies.columns)} category features")
        return self
    
    def create_rfm_features(self, customer_col: str, amount_col: str, date_col: str) -> pd.DataFrame:
        """Create RFM (Recency, Frequency, Monetary) features"""
        if all(col in self.df.columns for col in [customer_col, amount_col, date_col]):
            if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
                self.df[date_col] = pd.to_datetime(self.df[date_col])
            
            reference_date = self.df[date_col].max()
            
            rfm = self.df.groupby(customer_col).agg({
                date_col: lambda x: (reference_date - x.max()).days,  # Recency
                customer_col: 'size',  # Frequency
                amount_col: 'sum'  # Monetary
            })
            
            rfm.columns = ['recency', 'frequency', 'monetary']
            
            self.df['rfm_recency'] = self.df[customer_col].map(rfm['recency'])
            self.df['rfm_frequency'] = self.df[customer_col].map(rfm['frequency'])
            self.df['rfm_monetary'] = self.df[customer_col].map(rfm['monetary'])
            
            self.engineered_features.extend(['rfm_recency', 'rfm_frequency', 'rfm_monetary'])
            logger.info("Created RFM features")
        return self
    
    def get_engineered_data(self) -> pd.DataFrame:
        """Return dataframe with engineered features"""
        logger.info(f"Total engineered features: {len(self.engineered_features)}")
        return self.df
    
    def get_feature_summary(self) -> Dict:
        """Get summary of engineered features"""
        return {
            'total_features': len(self.engineered_features),
            'engineered_features': self.engineered_features,
            'dataframe_shape': self.df.shape
        }


class CustomerPurchaseBehaviorAnalyzer:
    """Main orchestrator for the analysis pipeline"""
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.engineered_data = None
        self.pipeline_config = {}
    
    def load_data(self, file_paths: Dict[str, str]) -> 'CustomerPurchaseBehaviorAnalyzer':
        """Load data from multiple sources"""
        loader = DataLoader()
        dfs = []
        
        for source_name, file_path in file_paths.items():
            try:
                if file_path.endswith('.csv'):
                    df = loader.load_csv(file_path)
                elif file_path.endswith('.json'):
                    df = loader.load_json(file_path)
                elif file_path.endswith(('.xlsx', '.xls')):
                    df = loader.load_excel(file_path)
                else:
                    logger.warning(f"Unsupported file format: {file_path}")
                    continue
                
                df['source'] = source_name
                dfs.append(df)
            except Exception as e:
                logger.error(f"Failed to load {source_name}: {str(e)}")
        
        if dfs:
            self.raw_data = pd.concat(dfs, ignore_index=True)
            logger.info(f"Combined {len(dfs)} data sources: {self.raw_data.shape}")
        
        return self
    
    def preprocess_data(self, preprocessing_config: Dict) -> 'CustomerPurchaseBehaviorAnalyzer':
        """Apply preprocessing steps"""
        if self.raw_data is None:
            logger.error("No raw data loaded")
            return self
        
        preprocessor = DataPreprocessor(self.raw_data)
        
        # Apply preprocessing steps based on config
        if preprocessing_config.get('remove_duplicates'):
            preprocessor.remove_duplicates(subset=preprocessing_config.get('duplicate_subset'))
        
        if preprocessing_config.get('missing_values_strategy'):
            preprocessor.handle_missing_values(preprocessing_config['missing_values_strategy'])
        
        if preprocessing_config.get('outlier_columns'):
            preprocessor.handle_outliers(
                columns=preprocessing_config['outlier_columns'],
                method=preprocessing_config.get('outlier_method', 'iqr'),
                threshold=preprocessing_config.get('outlier_threshold', 1.5)
            )
        
        if preprocessing_config.get('type_mapping'):
            preprocessor.convert_data_types(preprocessing_config['type_mapping'])
        
        if preprocessing_config.get('text_columns'):
            preprocessor.clean_text_columns(preprocessing_config['text_columns'])
        
        self.processed_data = preprocessor.get_processed_data()
        self.pipeline_config['preprocessing'] = preprocessing_config
        
        return self
    
    def engineer_features(self, feature_config: Dict) -> 'CustomerPurchaseBehaviorAnalyzer':
        """Create engineered features"""
        if self.processed_data is None:
            logger.error("No processed data available")
            return self
        
        engineer = FeatureEngineer(self.processed_data)
        
        # Apply feature engineering based on config
        if feature_config.get('monetary_features'):
            engineer.create_monetary_features(
                amount_col=feature_config['monetary_features'].get('amount_col'),
                transaction_col=feature_config['monetary_features'].get('transaction_col')
            )
        
        if feature_config.get('temporal_features'):
            engineer.create_temporal_features(feature_config['temporal_features'].get('date_col'))
        
        if feature_config.get('customer_lifecycle_features'):
            engineer.create_customer_lifecycle_features(
                customer_col=feature_config['customer_lifecycle_features'].get('customer_col'),
                date_col=feature_config['customer_lifecycle_features'].get('date_col')
            )
        
        if feature_config.get('frequency_features'):
            engineer.create_frequency_features(feature_config['frequency_features'].get('customer_col'))
        
        if feature_config.get('category_features'):
            engineer.create_category_features(feature_config['category_features'].get('category_col'))
        
        if feature_config.get('rfm_features'):
            engineer.create_rfm_features(
                customer_col=feature_config['rfm_features'].get('customer_col'),
                amount_col=feature_config['rfm_features'].get('amount_col'),
                date_col=feature_config['rfm_features'].get('date_col')
            )
        
        self.engineered_data = engineer.get_engineered_data()
        self.pipeline_config['features'] = feature_config
        self.pipeline_config['feature_summary'] = engineer.get_feature_summary()
        
        return self
    
    def save_results(self, output_path: str) -> None:
        """Save processed and engineered data"""
        if self.engineered_data is not None:
            output_file = f"{output_path}/customer_behavior_engineered.csv"
            self.engineered_data.to_csv(output_file, index=False)
            logger.info(f"Saved engineered data to {output_file}")
            
            # Save pipeline config
            config_file = f"{output_path}/pipeline_config.json"
            with open(config_file, 'w') as f:
                json.dump(self.pipeline_config, f, indent=2, default=str)
            logger.info(f"Saved pipeline configuration to {config_file}")
    
    def get_summary(self) -> Dict:
        """Get analysis summary"""
        return {
            'raw_data_shape': self.raw_data.shape if self.raw_data is not None else None,
            'processed_data_shape': self.processed_data.shape if self.processed_data is not None else None,
            'engineered_data_shape': self.engineered_data.shape if self.engineered_data is not None else None,
            'pipeline_config': self.pipeline_config,
            'missing_values': self.engineered_data.isnull().sum().to_dict() if self.engineered_data is not None else None
        }
