# Quick Fix: Correlation Heatmap Not Showing

## Problem
Correlation heatmaps were not displaying when requested.

## Cause
Seaborn library was missing from the environment.

## Solution

### 1. Install Seaborn
```bash
cd chat-app
./install-seaborn.sh
```

Or manually:
```bash
cd chat-app/chat-service
uv pip install seaborn>=0.12.0
```

### 2. Restart Services
```bash
cd chat-app
./stop-services.sh
./start-services.sh
```

### 3. Test
Upload iris.csv and ask:
```
"Show me a correlation matrix"
"Create a correlation heatmap"
```

## What Was Changed

### Files Modified:
1. **pyproject.toml** - Added `seaborn>=0.12.0` to dependencies
2. **code_executor.py** - Added `import seaborn as sns` and `'sns': sns` to globals
3. **data_analysis_agent.py** - Updated prompt to mention seaborn + added example

### New File:
- **install-seaborn.sh** - Installation script

## Result
✅ Correlation heatmaps now display correctly
✅ All seaborn visualizations work (boxplots, violin plots, pairplots, etc.)

---

For detailed information, see `HEATMAP_FIX_COMPLETE.md`
