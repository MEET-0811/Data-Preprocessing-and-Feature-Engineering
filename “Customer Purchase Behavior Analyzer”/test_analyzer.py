"""
Unit Tests and Validation Suite
Tests for the Customer Purchase Behavior Analyzer
"""

import unittest
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from customer_purchase_analyzer import (
    DataLoader, DataPreprocessor, FeatureEngineer,
    CustomerPurchaseBehaviorAnalyzer
)


class TestDataLoader(unittest.TestCase):
    """Test DataLoader class"""
    
    def setUp(self):
        """Create test data files"""
        self.test_dir = 'test_data'
        Path(self.test_dir).mkdir(exist_ok=True)
        
        # Create test CSV
        self.test_csv = os.path.join(self.test_dir, 'test.csv')
        pd.DataFrame({
            'id': [1, 2, 3],
            'value': [10, 20, 30]
        }).to_csv(self.test_csv, index=False)
        
        # Create test JSON
        self.test_json = os.path.join(self.test_dir, 'test.json')
        with open(self.test_json, 'w') as f:
            json.dump([{'id': 1, 'value': 10}, {'id': 2, 'value': 20}], f)
    
    def test_load_csv(self):
        """Test CSV loading"""
        loader = DataLoader()
        df = loader.load_csv(self.test_csv)
        self.assertEqual(len(df), 3)
        self.assertIn('id', df.columns)
    
    def test_load_json(self):
        """Test JSON loading"""
        loader = DataLoader()
        df = loader.load_json(self.test_json)
        self.assertEqual(len(df), 2)
        self.assertIn('id', df.columns)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)


class TestDataPreprocessor(unittest.TestCase):
    """Test DataPreprocessor class"""
    
    def setUp(self):
        """Create test dataframe"""
        self.test_df = pd.DataFrame({
            'id': [1, 1, 2, 3, 4, 5],
            'value': [10, 10, 20, np.nan, 40, 1000],
            'category': ['A', 'A', 'B', 'B', 'C', 'C']
        })
    
    def test_remove_duplicates(self):
        """Test duplicate removal"""
        preprocessor = DataPreprocessor(self.test_df)
        preprocessor.remove_duplicates()
        # Should have 5 rows after removing one duplicate
        self.assertLessEqual(len(preprocessor.df), 5)
    
    def test_handle_missing_values_median(self):
        """Test missing value handling with median"""
        preprocessor = DataPreprocessor(self.test_df)
        preprocessor.handle_missing_values({'value': 'median'})
        # Should have no NaN in value column
        self.assertEqual(preprocessor.df['value'].isnull().sum(), 0)
    
    def test_handle_outliers_iqr(self):
        """Test outlier handling with IQR"""
        preprocessor = DataPreprocessor(self.test_df)
        preprocessor.handle_outliers(['value'], method='iqr')
        # Should remove extreme outlier (1000)
        self.assertLess(len(preprocessor.df), len(self.test_df))
    
    def test_convert_data_types(self):
        """Test data type conversion"""
        df = self.test_df.copy()
        df['id'] = df['id'].astype(str)
        preprocessor = DataPreprocessor(df)
        preprocessor.convert_data_types({'id': 'int64'})
        self.assertEqual(preprocessor.df['id'].dtype, 'int64')


class TestFeatureEngineer(unittest.TestCase):
    """Test FeatureEngineer class"""
    
    def setUp(self):
        """Create test dataframe"""
        dates = pd.date_range('2025-01-01', periods=100, freq='D')
        self.test_df = pd.DataFrame({
            'customer_id': ['CUST_001'] * 50 + ['CUST_002'] * 50,
            'purchase_date': list(dates[:50]) + list(dates[:50]),
            'amount': np.random.uniform(10, 100, 100),
            'product_category': np.random.choice(['A', 'B', 'C'], 100)
        })
    
    def test_create_monetary_features(self):
        """Test monetary feature creation"""
        engineer = FeatureEngineer(self.test_df)
        engineer.create_monetary_features('amount', 'customer_id')
        # Should have new features
        self.assertIn('is_high_value', engineer.df.columns)
    
    def test_create_temporal_features(self):
        """Test temporal feature creation"""
        engineer = FeatureEngineer(self.test_df)
        engineer.create_temporal_features('purchase_date')
        # Should have month and year columns
        self.assertIn('month', engineer.df.columns)
        self.assertIn('year', engineer.df.columns)
    
    def test_create_frequency_features(self):
        """Test frequency feature creation"""
        engineer = FeatureEngineer(self.test_df)
        engineer.create_frequency_features('customer_id')
        # Should have frequency column
        self.assertIn('purchase_frequency', engineer.df.columns)
    
    def test_create_rfm_features(self):
        """Test RFM feature creation"""
        engineer = FeatureEngineer(self.test_df)
        engineer.create_rfm_features('customer_id', 'amount', 'purchase_date')
        # Should have RFM columns
        self.assertIn('rfm_recency', engineer.df.columns)
        self.assertIn('rfm_frequency', engineer.df.columns)
        self.assertIn('rfm_monetary', engineer.df.columns)


class TestCustomerPurchaseBehaviorAnalyzer(unittest.TestCase):
    """Test main analyzer class"""
    
    def setUp(self):
        """Create test data"""
        self.test_dir = 'test_analyzer_data'
        Path(self.test_dir).mkdir(exist_ok=True)
        
        # Create sample CSV
        self.test_csv = os.path.join(self.test_dir, 'test_transactions.csv')
        df = pd.DataFrame({
            'customer_id': ['CUST_001'] * 10 + ['CUST_002'] * 10,
            'purchase_date': pd.date_range('2025-01-01', periods=20, freq='D').astype(str),
            'amount': np.random.uniform(10, 100, 20),
            'product_category': np.random.choice(['A', 'B', 'C'], 20)
        })
        df.to_csv(self.test_csv, index=False)
    
    def test_full_pipeline(self):
        """Test complete pipeline execution"""
        analyzer = CustomerPurchaseBehaviorAnalyzer()
        
        # Load data
        analyzer.load_data({'test': self.test_csv})
        self.assertIsNotNone(analyzer.raw_data)
        
        # Preprocess
        analyzer.preprocess_data({
            'remove_duplicates': True,
            'type_mapping': {'purchase_date': 'datetime'}
        })
        self.assertIsNotNone(analyzer.processed_data)
        
        # Engineer features
        analyzer.engineer_features({
            'temporal_features': {'date_col': 'purchase_date'},
            'frequency_features': {'customer_col': 'customer_id'}
        })
        self.assertIsNotNone(analyzer.engineered_data)
    
    def test_pipeline_summary(self):
        """Test pipeline summary generation"""
        analyzer = CustomerPurchaseBehaviorAnalyzer()
        analyzer.load_data({'test': self.test_csv})
        analyzer.preprocess_data({'remove_duplicates': True})
        analyzer.engineer_features({})
        
        summary = analyzer.get_summary()
        self.assertIn('raw_data_shape', summary)
        self.assertIn('processed_data_shape', summary)
        self.assertIn('engineered_data_shape', summary)
    
    def tearDown(self):
        """Clean up"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)


class TestDataQuality(unittest.TestCase):
    """Test data quality validations"""
    
    def setUp(self):
        """Create test dataframe"""
        self.df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'value': [10, 20, np.nan, 40, 50],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
    
    def test_missing_values_count(self):
        """Test missing values detection"""
        missing_count = self.df.isnull().sum().sum()
        self.assertEqual(missing_count, 1)
    
    def test_duplicates_count(self):
        """Test duplicate detection"""
        df_with_dups = pd.concat([self.df, self.df.iloc[0:1]])
        duplicates = df_with_dups.duplicated().sum()
        self.assertGreater(duplicates, 0)
    
    def test_data_types(self):
        """Test data type consistency"""
        expected_types = ['int64', 'float64', 'object']
        actual_types = self.df.dtypes.astype(str).tolist()
        for dtype in actual_types:
            self.assertTrue(any(exp in dtype for exp in expected_types))


def run_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("RUNNING TEST SUITE")
    print("="*80 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestDataPreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestFeatureEngineer))
    suite.addTests(loader.loadTestsFromTestCase(TestCustomerPurchaseBehaviorAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestDataQuality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
