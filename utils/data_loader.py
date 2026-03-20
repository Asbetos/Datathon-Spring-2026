"""Data loader for ReFED food waste datasets."""
import os
import warnings
import pandas as pd

warnings.filterwarnings('ignore')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')
CLEAN = os.path.join(BASE, 'outputs', 'analysis', 'cleaned_data')

SECTOR_COLORS = {
    'Farm': '#2C5F2D',
    'Foodservice': '#F96167',
    'Manufacturing': '#065A82',
    'Residential': '#F9E795',
    'Retail': '#028090',
}

def _load_csv(filename, skiprows=3):
    return pd.read_csv(os.path.join(DATA, filename), skiprows=skiprows)

def load_national_summary():
    return _load_csv('ReFED_US_Food_Surplus_Summary.csv')

def load_national_cause():
    return _load_csv('ReFED_US_Food_Surplus_Cause_Summary.csv')

def load_national_detail():
    return _load_csv('ReFED_US_Food_Surplus_Detail.csv')

def load_state_summary():
    return _load_csv('ReFED_US_State_Food_Surplus_Summary.csv')

def load_state_detail():
    return _load_csv('ReFED_US_State_Food_Surplus_Detail.csv')

def load_all():
    return {
        'national_summary': load_national_summary(),
        'national_cause': load_national_cause(),
        'national_detail': load_national_detail(),
        'state_summary': load_state_summary(),
        'state_detail': load_state_detail(),
    }

def save_clean_parquet(datasets=None):
    """Clean and save all datasets as parquet."""
    os.makedirs(CLEAN, exist_ok=True)
    if datasets is None:
        datasets = load_all()
    for name, df in datasets.items():
        path = os.path.join(CLEAN, f'{name}.parquet')
        df.to_parquet(path, index=False)
    return datasets

def load_clean_parquet():
    """Load pre-cleaned parquet files."""
    out = {}
    for name in ['national_summary', 'national_cause', 'national_detail',
                  'state_summary', 'state_detail']:
        path = os.path.join(CLEAN, f'{name}.parquet')
        out[name] = pd.read_parquet(path)
    return out
