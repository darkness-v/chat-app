# CSV Data Analysis Feature - Implementation Guide

## Overview

The CSV data analysis feature adds intelligent data exploration capabilities to your chat application. Users can upload CSV files or provide URLs, and the AI agent will generate and execute Python code to answer questions, create visualizations, and provide insights.

## Architecture

### Components

1. **Code Executor** (`chat-service/code_executor.py`)
   - Sandboxed Python environment
   - Executes pandas, numpy, matplotlib code
   - Captures stdout and generated plots
   - Maintains dataframe state per conversation

2. **Data Analysis Agent** (`chat-service/data_analysis_agent.py`)
   - Specialized prompts for data analysis
   - Code extraction from LLM responses
   - Retry logic for failed code execution
   - Result formatting

3. **Backend Endpoints** (`chat-service/main.py`)
   - `/api/csv-analysis/stream` - Streaming data analysis
   - `/api/csv-analysis/clear/{conversation_id}` - Clear analysis state
   - `/api/csv-analysis/dataframes/{conversation_id}` - List loaded dataframes

4. **Storage Service** (`storage-service/main.py`)
   - `/api/upload-csv` - Handle CSV file uploads

5. **Frontend Components**
   - `CSVUpload.tsx` - File upload and URL input
   - Updated `ChatMessage.tsx` - Display plots and formatted code
   - Updated `page.tsx` - CSV mode integration

## Flow Diagram

```
User uploads CSV → Storage Service saves file
                ↓
User asks question → Chat Service receives request
                ↓
Code Executor loads CSV → DataFrame in memory
                ↓
LLM generates Python code → Code extracted
                ↓
Code Executor runs code → Captures output & plots
                ↓
If error → Retry with error feedback (max 2 retries)
                ↓
Results streamed to frontend → Displayed with plots
```

## Agent Prompt Strategy

The data analysis agent uses a specialized system prompt that:

1. **Sets Expectations**: Explains available tools (pandas, numpy, matplotlib)
2. **Provides Guidelines**: 
   - Wrap code in ```python blocks
   - Use print() for outputs
   - Keep outputs concise
   - Handle errors gracefully

3. **Analysis Approach**:
   - First explore data structure
   - Answer specific questions
   - Provide insights
   - Suggest follow-ups

4. **Example-Driven**: Shows proper interaction format

### Key Prompt Elements

```python
DATA_ANALYSIS_SYSTEM_PROMPT = """
You are an expert Data Analyst AI assistant with Python expertise.

**Your Capabilities:**
- Access to pandas, numpy, and matplotlib
- Code execution in sandboxed environment
- CSV already loaded as 'df' or 'df_1'

**Code Execution Guidelines:**
1. Wrap code in ```python blocks
2. Use print() for results
3. Keep outputs concise
4. Visualizations captured automatically

**Analysis Approach:**
1. Explore data structure
2. Answer specific question
3. Provide insights
4. Suggest follow-ups
"""
```

## Code Execution Safety

### Sandboxing Approach

1. **Limited Scope**: Only pandas, numpy, matplotlib available
2. **Stdout Capture**: All print() outputs captured
3. **Error Handling**: Exceptions caught and reported
4. **Memory Management**: Dataframes isolated per conversation
5. **Non-Interactive**: matplotlib uses 'Agg' backend

### Security Considerations

⚠️ **Current Implementation**: Basic sandboxing
- Limited to data analysis libraries
- No file system access (except loaded CSV)
- No network access
- exec() used with controlled globals/locals

🔒 **Production Recommendations**:
- Use containerized execution (Docker)
- Resource limits (CPU, memory, timeout)
- Additional library restrictions
- Input validation and sanitization

## Usage Examples

### Example 1: Basic Statistics

**User**: "Show me basic statistics for numeric columns"

**Agent Response**:
```python
# Display basic statistics for numeric columns
print("Dataset shape:", df.shape)
print("\nNumeric columns summary:")
print(df.describe())

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())
```

### Example 2: Visualization

**User**: "Plot a histogram of the price column"

**Agent Response**:
```python
import matplotlib.pyplot as plt

# Create histogram
plt.figure(figsize=(10, 6))
plt.hist(df['price'].dropna(), bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Distribution of Prices')
plt.grid(True, alpha=0.3)
```

*Plot automatically captured and displayed*

### Example 3: Data Exploration

**User**: "Which column has the most missing values?"

**Agent Response**:
```python
# Calculate missing values for each column
missing_values = df.isnull().sum().sort_values(ascending=False)
missing_pct = (missing_values / len(df) * 100).round(2)

# Display top 10 columns with missing values
result = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage': missing_pct
})

print("Columns with most missing values:")
print(result[result['Missing Values'] > 0].head(10))
```

## Error Handling & Retry Logic

### Retry Strategy

1. **Initial Execution**: Run generated code
2. **On Error**: Check if error is retryable
3. **Retry Prompt**: Send error back to LLM with context
4. **Fixed Code**: LLM generates corrected version
5. **Max Retries**: 2 attempts

### Retryable Errors

- `NameError`: Undefined variable
- `KeyError`: Missing column
- `AttributeError`: Wrong method/attribute
- `ValueError`: Invalid value
- `TypeError`: Type mismatch
- `SyntaxError`: Code syntax issue

### Example Retry Flow

**Initial Code** (contains error):
```python
print(df['Price'].mean())  # Column name is 'price', not 'Price'
```

**Error**: `KeyError: 'Price'`

**Retry Prompt**:
```
The previous code failed with an error.
Original Question: Show average price
Failed Code: print(df['Price'].mean())
Error: KeyError: 'Price'

Please provide corrected code.
```

**Fixed Code**:
```python
# Corrected: use lowercase 'price'
print(f"Average price: ${df['price'].mean():.2f}")
```

## Frontend Integration

### CSV Upload

```tsx
<CSVUpload 
  onUpload={(path, filename) => {
    // Switch to CSV mode
    // Show success message
    // Enable data analysis
  }}
  disabled={isLoading}
/>
```

### Message Display with Plots

```tsx
<ChatMessage 
  message={message}
  plots={messagePlots[message.id]}  // Array of base64 images
/>
```

### Streaming with Code Execution

The frontend handles two types of events:
1. **Text Content**: `{content: "...", done: false}`
2. **Image Data**: `{type: "image", data: "base64...", done: false}`

## Installation & Setup

### 1. Install Dependencies

```bash
cd chat-service
uv pip install pandas numpy matplotlib
```

Or update `pyproject.toml`:
```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "openai>=1.3.0",
    "python-dotenv>=1.0.1",
    "pydantic>=2.5.0",
    "httpx>=0.25.1",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "matplotlib>=3.7.0",
]
```

Then run:
```bash
uv pip install -e .
```

### 2. Restart Services

```bash
cd /Users/tani/TechJDI/chat-app
./stop-services.sh
./start-services.sh
```

### 3. Test CSV Analysis

1. Open http://localhost:3000
2. Upload a CSV file or provide URL
3. Ask questions like:
   - "Summarize the dataset"
   - "Show statistics for numeric columns"
   - "Plot histogram of [column_name]"

## API Reference

### POST `/api/csv-analysis/stream`

Stream CSV data analysis with code execution.

**Request Body**:
```json
{
  "conversation_id": 1,
  "message": "Show basic statistics",
  "csv_path": "/path/to/file.csv",
  "model": "gpt-4o-mini"
}
```

**Response**: Server-Sent Events (SSE)

```
data: {"content": "I'll analyze...", "done": false}
data: {"content": "\n```python\n...", "done": false}
data: {"type": "image", "data": "base64...", "done": false}
data: {"content": "", "done": true}
```

### POST `/api/csv-analysis/clear/{conversation_id}`

Clear CSV analysis data for a conversation.

**Response**:
```json
{
  "message": "CSV analysis data cleared"
}
```

### GET `/api/csv-analysis/dataframes/{conversation_id}`

List loaded dataframes.

**Response**:
```json
{
  "dataframes": ["df", "df_1", "df_2"]
}
```

### POST `/api/upload-csv` (Storage Service)

Upload CSV file.

**Request**: multipart/form-data with file

**Response**:
```json
{
  "csv_path": "/absolute/path/to/file.csv",
  "csv_url": "/uploads/uuid.csv",
  "filename": "original.csv"
}
```

## Comparison with MCP Server

### Similarities

1. **Code Execution**: Both use pandas/numpy/matplotlib
2. **Sandboxing**: Both capture stdout and plots
3. **Dataframe Management**: Both maintain state
4. **Error Handling**: Both catch and report errors

### Differences

| Feature | Our Implementation | MCP Server |
|---------|-------------------|------------|
| **Architecture** | REST API + SSE streaming | MCP protocol (stdio) |
| **Integration** | Direct FastAPI endpoints | Claude Desktop integration |
| **Prompting** | Simpler, focused prompts | Elaborate 5-step process |
| **Visualization** | Base64 embedded in stream | Plotly.js code generation |
| **Retry Logic** | Automatic with LLM feedback | Manual iteration |
| **Frontend** | React components | Claude UI |

### Why This Approach?

1. **Lightweight**: No MCP server installation needed
2. **Integrated**: Works directly with existing chat app
3. **Flexible**: Easy to extend and customize
4. **Streaming**: Real-time feedback to user
5. **Simple**: Fewer moving parts

## Troubleshooting

### Issue: Code won't execute

**Check**:
1. Dependencies installed: `uv pip list | grep pandas`
2. Code executor initialized: Check logs for errors
3. CSV loaded: Verify file path is accessible

### Issue: Plots not displaying

**Check**:
1. matplotlib backend: Should be 'Agg'
2. Base64 encoding: Verify in browser network tab
3. Frontend message handling: Check `type === 'image'`

### Issue: Out of memory

**Solution**:
- Limit dataframe size in code
- Clear old conversations: `/api/csv-analysis/clear/{id}`
- Add resource limits (production)

### Issue: Permission errors

**Check**:
- File permissions on uploads directory
- CSV file readable by service
- Absolute path used for local files

## Future Enhancements

1. **Advanced Visualizations**: Plotly, Seaborn support
2. **Multiple DataFrames**: Join/merge operations
3. **Export Results**: Download generated plots
4. **Code History**: Save and reuse successful code
5. **Templates**: Pre-built analysis templates
6. **Streaming Plots**: Progressive rendering
7. **Resource Limits**: CPU/memory/timeout controls
8. **User Libraries**: Allow custom imports (with safety)

## Conclusion

This implementation provides a powerful, integrated CSV analysis capability that:
- ✅ Works seamlessly with existing chat application
- ✅ Generates and executes Python code intelligently
- ✅ Handles errors with automatic retry
- ✅ Displays results inline with visualizations
- ✅ Maintains conversation context
- ✅ Streams responses in real-time

The approach balances simplicity with capability, making it easy to use while providing professional data analysis features.
