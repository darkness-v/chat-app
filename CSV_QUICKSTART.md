# CSV Data Analysis Feature - Quick Start

## 🎯 What's New

Your chat application now supports **intelligent CSV data analysis**! Upload CSV files or provide URLs, and the AI will:

- 📊 Generate Python code to analyze your data
- 📈 Create visualizations (histograms, scatter plots, etc.)
- 🔢 Calculate statistics and insights
- 🔄 Automatically retry if code fails
- 💬 Explain results in natural language

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /Users/tani/TechJDI/chat-app
./setup-csv-analysis.sh
```

Or manually:
```bash
cd chat-service
uv pip install pandas numpy matplotlib
```

### 2. Restart Services

```bash
./stop-services.sh
./start-services.sh
```

### 3. Try It Out!

1. Open http://localhost:3000
2. Click on the **CSV Upload** section
3. Upload a CSV file or paste a URL (e.g., GitHub raw URL, Google Drive link)
4. Start asking questions!

## 💡 Example Questions

Once you've loaded a CSV, try asking:

### Basic Exploration
- "Summarize the dataset"
- "Show me the first 10 rows"
- "What columns does this dataset have?"
- "Show basic statistics for numeric columns"

### Data Quality
- "Which columns have missing values?"
- "How many duplicate rows are there?"
- "Show data types for each column"

### Analysis
- "What's the average price?"
- "Which category appears most frequently?"
- "Show correlation between price and quantity"
- "Find outliers in the age column"

### Visualizations
- "Plot a histogram of prices"
- "Create a scatter plot of age vs income"
- "Show a bar chart of sales by category"
- "Plot the distribution of ratings"

## 🎨 Features

### ✅ Supported Operations

- **Data Loading**: CSV files, URLs (HTTP/HTTPS)
- **Libraries**: pandas, numpy, matplotlib
- **Visualizations**: Histograms, scatter plots, bar charts, line plots
- **Statistics**: Mean, median, mode, std dev, correlations
- **Data Cleaning**: Missing values, duplicates, filtering
- **Aggregations**: Group by, pivot tables, summaries

### 🔄 Smart Retry Logic

If the generated code has errors:
1. Error is captured and sent back to the AI
2. AI analyzes the error and generates fixed code
3. Automatic retry (up to 2 attempts)
4. Clear error messages if retry fails

### 📊 Inline Results

- **Text Output**: Printed results shown in chat
- **Tables**: DataFrames displayed as formatted text
- **Plots**: Charts embedded directly in messages
- **Code Blocks**: Syntax-highlighted Python code

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │ (React/Next.js)
│  CSV Upload │
└──────┬──────┘
       │ Upload CSV
       ▼
┌─────────────────┐
│ Storage Service │ (Port 8002)
│  Saves CSV file │
└─────────────────┘
       │
       │ CSV path
       ▼
┌──────────────────┐
│  Chat Service    │ (Port 8001)
│                  │
│ ┌──────────────┐ │
│ │ Data Agent   │ │ → Generates Python code
│ └──────────────┘ │
│        ↓         │
│ ┌──────────────┐ │
│ │Code Executor │ │ → Runs code safely
│ └──────────────┘ │
│        ↓         │
│  Returns results │
│  + plots         │
└──────────────────┘
```

## 📝 Example Session

**User**: *Uploads sales_data.csv*

**AI**: 
> 📊 CSV file "sales_data.csv" loaded successfully! You can now ask questions about the data.

**User**: "Summarize the dataset"

**AI**: 
> I'll analyze the dataset structure and provide a summary.
> 
> ```python
> print("Dataset shape:", df.shape)
> print("\nColumn names:")
> print(df.columns.tolist())
> print("\nData types:")
> print(df.dtypes)
> print("\nFirst 5 rows:")
> print(df.head())
> ```
> 
> **Output:**
> ```
> Dataset shape: (1000, 5)
> 
> Column names:
> ['date', 'product', 'price', 'quantity', 'revenue']
> 
> Data types:
> date        object
> product     object
> price      float64
> quantity     int64
> revenue    float64
> dtype: object
> ```

**User**: "Plot a histogram of revenue"

**AI**:
> I'll create a histogram showing the distribution of revenue.
> 
> ```python
> import matplotlib.pyplot as plt
> 
> plt.figure(figsize=(10, 6))
> plt.hist(df['revenue'], bins=30, edgecolor='black', alpha=0.7)
> plt.xlabel('Revenue ($)')
> plt.ylabel('Frequency')
> plt.title('Distribution of Revenue')
> plt.grid(True, alpha=0.3)
> ```
> 
> *[Histogram displayed inline]*

## 🔒 Security Notes

### Current Implementation (Development)

The code executor provides basic sandboxing:
- ✅ Limited to data analysis libraries (pandas, numpy, matplotlib)
- ✅ No file system access beyond loaded CSV
- ✅ No network access
- ✅ Stdout/stderr captured
- ✅ Exceptions caught

### ⚠️ Production Recommendations

For production deployment, consider:
- 🐳 **Docker Containers**: Isolate execution environment
- ⏱️ **Resource Limits**: CPU, memory, execution timeout
- 🔐 **Input Validation**: Sanitize file uploads and code
- 📊 **Audit Logging**: Track all code execution
- 🚫 **Library Restrictions**: Whitelist allowed imports

## 🛠️ API Endpoints

### Chat Service (Port 8001)

#### `POST /api/csv-analysis/stream`
Stream CSV data analysis with code execution.

**Request:**
```json
{
  "conversation_id": 1,
  "message": "Show statistics",
  "csv_path": "/path/to/file.csv"
}
```

**Response:** Server-Sent Events (SSE)

#### `POST /api/csv-analysis/clear/{conversation_id}`
Clear CSV analysis data for a conversation.

#### `GET /api/csv-analysis/dataframes/{conversation_id}`
List all loaded dataframes for a conversation.

### Storage Service (Port 8002)

#### `POST /api/upload-csv`
Upload a CSV file.

**Response:**
```json
{
  "csv_path": "/absolute/path/to/file.csv",
  "csv_url": "/uploads/uuid.csv",
  "filename": "original.csv"
}
```

## 🐛 Troubleshooting

### Dependencies not installed
```bash
cd chat-service
uv pip install pandas numpy matplotlib
```

### CSV upload fails
- Check file is valid CSV
- Ensure storage-service is running (port 8002)
- Check `uploads/` directory exists and is writable

### Code execution errors
- Most errors trigger automatic retry
- Check chat-service logs for details
- Verify CSV loaded correctly

### Plots not displaying
- Check browser console for errors
- Verify base64 image data in network tab
- Ensure matplotlib backend is 'Agg'

## 📚 Learn More

- **Full Documentation**: [CSV_ANALYSIS_GUIDE.md](./CSV_ANALYSIS_GUIDE.md)
- **Code Executor**: [chat-service/code_executor.py](./chat-service/code_executor.py)
- **Data Agent**: [chat-service/data_analysis_agent.py](./chat-service/data_analysis_agent.py)
- **MCP Server Reference**: https://github.com/reading-plus-ai/mcp-server-data-exploration

## 🎓 Inspired By

This implementation is inspired by the [MCP Server for Data Exploration](https://github.com/reading-plus-ai/mcp-server-data-exploration) but adapted for:
- Direct REST API integration
- Streaming responses
- Simpler setup (no MCP protocol)
- Web-based UI
- Automatic retry logic

## 🚀 Next Steps

1. Try uploading your own CSV files
2. Experiment with different questions
3. Check out the example datasets:
   - [Kaggle Datasets](https://www.kaggle.com/datasets)
   - [Google Dataset Search](https://datasetsearch.research.google.com/)
   - [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)

4. Extend functionality:
   - Add more visualization types
   - Support multiple DataFrames
   - Export results to PDF/Excel
   - Create analysis templates

Happy analyzing! 📊✨
