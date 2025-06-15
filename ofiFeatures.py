import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def calculate_best_level_ofi(df):
    # Create a copy to avoid modifying original data
    df = df.copy()
    
    df['best_bid_size'] = df['bid_sz_00']
    df['best_ask_size'] = df['ask_sz_00']
    
    # Calculate size changes using diff for difference between current and previous row
    df['bid_size_change'] = df['best_bid_size'].diff()
    df['ask_size_change'] = df['best_ask_size'].diff()
    df['ofi'] = df['bid_size_change'] - df['ask_size_change']
    
    # Fill NaN values with 0 (due to diff)
    df['ofi'] = df['ofi'].fillna(0)
    return df

def calculate_multi_level_ofi(df, num_levels=10):
    df = df.copy()
    
    # Calculate mid price at each level
    for level in range(num_levels):
        level_str = f"{level:02d}"
        mid_price = (df[f'bid_px_{level_str}'] + df[f'ask_px_{level_str}']) / 2
        df[f'mid_price_{level_str}'] = mid_price
    df['best_mid_price'] = df['mid_price_00']
    
    # Calculate OFI for each level with distance-based weighting
    for level in range(num_levels):
        level_str = f"{level:02d}"

        df[f'bid_size_change_{level_str}'] = df[f'bid_sz_{level_str}'].diff()
        df[f'ask_size_change_{level_str}'] = df[f'ask_sz_{level_str}'].diff()
        df[f'price_distance_{level_str}'] = abs(df[f'mid_price_{level_str}'] - df['best_mid_price'])
        
        df[f'ofi_{level_str}'] = df[f'bid_size_change_{level_str}'] - df[f'ask_size_change_{level_str}']
        df[f'weighted_ofi_{level_str}'] = df[f'ofi_{level_str}'] * np.exp(-df[f'price_distance_{level_str}'])
    
    # Calculate total multi-level OFI
    ofi_columns = [f'weighted_ofi_{f"{i:02d}"}' for i in range(num_levels)]
    df['multi_level_ofi'] = df[ofi_columns].sum(axis=1)
    df['multi_level_ofi'] = df['multi_level_ofi'].fillna(0)
    
    return df

def calculate_multi_level_ofi_with_pca(df, num_levels=10, n_components=2):
    df = df.copy()
    
    # Calculate multi-level OFI
    df = calculate_multi_level_ofi(df, num_levels)
    
    ofi_columns = [f'weighted_ofi_{f"{i:02d}"}' for i in range(num_levels)]

    # Calculate PCA
    pca = PCA(n_components=2)

    ofi_df = df[ofi_columns]
    #fill na with 0
    ofi_df = ofi_df.fillna(0)

    pca.fit(ofi_df)
    df['pca_1'] = pca.transform(ofi_df)[:, 0]
    return df

def calculate_integrated_ofi(df, window_sizes=[1, 5, 10, 30, 60]):
    df = df.copy()
    
    df['ts_event'] = pd.to_datetime(df['ts_event'])
    
    # Calculate integrated OFI for each window size
    for window in window_sizes:
        df[f'integrated_ofi_{window}s'] = df['ofi'].rolling(
            window=window,
            min_periods=1
        ).sum()
        df[f'integrated_ofi_{window}s'] = df[f'integrated_ofi_{window}s'] / window
    return df

def calculate_cross_asset_ofi(df, asset_pairs):
    df = df.copy()
    
    # Group data by asset
    asset_groups = df.groupby('symbol')
    
    for asset1, asset2 in asset_pairs:
        ofi1 = asset_groups.get_group(asset1)['ofi']
        ofi2 = asset_groups.get_group(asset2)['ofi']
        cross_ofi = ofi1 * ofi2
        df[f'cross_ofi_{asset1}_{asset2}'] = cross_ofi
    return df

# # --- Analysis of Functions given a return set of information ---

# def calculate_multi_level_ofi_with_lasso(df, num_levels=10):
#     df = df.copy()
    
#     # Calculate multi-level OFI
#     df = calculate_multi_level_ofi(df, num_levels)
    
#     ofi_columns = [f'weighted_ofi_{f"{i:02d}"}' for i in range(num_levels)]
    
#     # Calculate Lasso
#     lasso = Lasso(alpha=0.1)
#     lasso.fit(df[ofi_columns], df['ofi'])
#     lasso_coefficients = lasso.coef_

#     # Add Lasso coefficients to dataframe
#     df['lasso_coef_00'] = lasso_coefficients[0]
#     df['lasso_coef_01'] = lasso_coefficients[1]
#     return df

# def calculate_multi_level_ofi_with_ols(df, num_levels=10):
#     df = df.copy()
    
#     # Calculate multi-level OFI
#     df = calculate_multi_level_ofi(df, num_levels)
    
#     ofi_columns = [f'weighted_ofi_{f"{i:02d}"}' for i in range(num_levels)]
    
#     ols = OLS(df['ofi'], df[ofi_columns])
#     ols_coefficients = ols.coef_

#     # Add OLS coefficients to dataframe
#     df['ols_coef_00'] = ols_coefficients[0]
#     df['ols_coef_01'] = ols_coefficients[1]
#     return df