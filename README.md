# Order Flow Imbalance (OFI) Analysis

## Setup Guide

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation Steps

1. **Create and Activate Virtual Environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### Project Structure
```
orderFlowImbalance/
├── .venv/                  # Virtual environment
├── data/
│   └── first_25000_rows.csv  # Dataset
├── dataPrep.ipynb          # Main analysis notebook
├── ofiFeatures.py          # OFI calculation functions
└── requirements.txt        # Project dependencies
```

### Running the Analysis

**Open and Run the Notebook**
- Open `main.ipynb`
- Run cells

### Available OFI Features

#### 1. Best-Level OFI
- Calculates order flow imbalance at the best bid/ask level
- Uses level '00' which represents the top of the book
- Formula: `OFI = Δ(bid_size) - Δ(ask_size)`

#### 2. Multi-Level OFI
- Looks at multiple price levels (00-09)
- Weights each level based on distance from best price
- More comprehensive than best-level OFI
- Also have a PCA based multi level OFI

#### 3. Integrated OFI
- Time-integrated version of OFI
- Available windows: 1s, 5s, 10s, 30s, 60s
- Helps identify persistent order flow pressure

#### 4. Cross Asset OFI
- Cross Asset version of OFI
- Helps identify broader order flow pressure
- Note: did not implement due to no other assets in the A/C

### Data Requirements
The dataset (`first_25000_rows.csv`) should contain:
- `ts_event`: Timestamp of the event
- `bid_sz_00` through `bid_sz_09`: Bid sizes at each level
- `ask_sz_00` through `ask_sz_09`: Ask sizes at each level
- `bid_px_00` through `bid_px_09`: Bid prices at each level
- `ask_px_00` through `ask_px_09`: Ask prices at each level

### Output Analysis
The notebook generates:
1. OFI time series plots
2. Statistical summaries
3. Correlation analysis
4. Comparative visualizations

### Notes
- Current dataset contains AAPL data only
- Cross-Asset OFI requires multiple assets

### Potential Next Steps
1. Implement additional OFI features:
   - Volume-Weighted OFI
   - Price-Impact OFI
   - Time-of-Day OFI patterns

2. Add more assets to enable Cross-Asset OFI analysis

