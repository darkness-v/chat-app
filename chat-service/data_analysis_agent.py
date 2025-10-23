"""
Data Analysis Agent - Generates and executes Python code for CSV analysis
"""

from typing import List, Dict, Optional
import json

# System prompt for the data analysis agent
DATA_ANALYSIS_SYSTEM_PROMPT = """You are an expert Data Analyst AI assistant with Python expertise. Your role is to help users analyze CSV datasets by writing and executing Python code.

**Your Capabilities:**
- You have access to pandas, numpy, and matplotlib libraries
- You can write Python code that will be executed in a sandboxed environment
- The user has already loaded a CSV file into a DataFrame (usually named 'df' or 'df_1')
- You can print results, create visualizations, and perform statistical analysis

**Code Execution Guidelines:**
1. ALWAYS wrap your Python code in ```python code blocks
2. Use print() statements to show results to the user
3. Keep outputs concise - limit dataframe displays to .head() or specific rows
4. For visualizations, use matplotlib (it will be automatically captured)
5. Add comments to explain your analysis steps
6. Handle potential errors gracefully

**CRITICAL - Matplotlib Usage:**
- Do NOT use plt.show() - plots are captured automatically
- Do NOT use plt.savefig() - not needed
- Simply create your plots with plt.figure(), plt.plot(), plt.hist(), etc.
- The system will automatically capture and display your plots
- After creating a plot, just move on - no need to display it manually

**Analysis Approach:**
1. First, explore the data structure (shape, columns, types, missing values)
2. Answer the user's specific question
3. Provide insights and interpretations in natural language
4. Suggest follow-up analyses if relevant

**Important:**
- Do NOT try to load files yourself - they are already loaded
- Do NOT use plt.show() or plt.savefig() - plots are captured automatically
- Keep code simple and focused on the question asked
- If code fails, analyze the error and provide a corrected version

**Example Interaction:**
User: "Show me basic statistics for numeric columns"
You: "I'll calculate summary statistics for all numeric columns in the dataset.

```python
# Display basic statistics for numeric columns
print("Dataset shape:", df.shape)
print("\\nNumeric columns summary:")
print(df.describe())

# Check for missing values
print("\\nMissing values per column:")
print(df.isnull().sum())
```

This will show you the mean, median, standard deviation, and other statistics for each numeric column."

User: "Plot a histogram"
You: "I'll create a histogram to visualize the distribution.

```python
import matplotlib.pyplot as plt

# Create histogram
plt.figure(figsize=(10, 6))
plt.hist(df['column_name'], bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Column Name')
plt.ylabel('Frequency')
plt.title('Distribution of Column Name')
plt.grid(True, alpha=0.3)
# No plt.show() needed - plot is captured automatically
```

The histogram will be displayed automatically below."

Now, help the user analyze their data!"""


def create_analysis_messages(conversation_history: List[Dict], csv_info: Optional[str] = None) -> List[Dict]:
    """
    Create messages for the data analysis agent
    
    Args:
        conversation_history: Previous messages in the conversation
        csv_info: Information about the loaded CSV (optional)
    
    Returns:
        List of messages formatted for OpenAI API
    """
    messages = [{"role": "system", "content": DATA_ANALYSIS_SYSTEM_PROMPT}]
    
    # Add CSV info if available
    if csv_info:
        messages.append({
            "role": "system",
            "content": f"Dataset Information:\n{csv_info}"
        })
    
    # Add conversation history
    messages.extend(conversation_history)
    
    return messages


def extract_python_code(text: str) -> List[str]:
    """
    Extract Python code blocks from markdown text
    
    Returns:
        List of code snippets found in the text
    """
    code_blocks = []
    lines = text.split('\n')
    in_code_block = False
    current_block = []
    
    for line in lines:
        if line.strip().startswith('```python'):
            in_code_block = True
            current_block = []
        elif line.strip().startswith('```') and in_code_block:
            in_code_block = False
            if current_block:
                code_blocks.append('\n'.join(current_block))
            current_block = []
        elif in_code_block:
            current_block.append(line)
    
    return code_blocks


def format_execution_result(result: Dict) -> str:
    """
    Format code execution result for display
    
    Args:
        result: Dict from CodeExecutor.execute_code()
    
    Returns:
        Formatted string for user display
    """
    output = ""
    
    if result['success']:
        if result['stdout']:
            output += f"**Output:**\n```\n{result['stdout']}\n```\n\n"
        
        if result['plots']:
            output += f"**Visualization:** {len(result['plots'])} plot(s) generated\n\n"
        
        if result['saved_dfs']:
            output += f"**Saved DataFrames:** {', '.join(result['saved_dfs'])}\n\n"
            
        if not result['stdout'] and not result['plots']:
            output += "Code executed successfully (no output)\n\n"
    else:
        output += f"**Error during execution:**\n```\n{result['error']}\n```\n\n"
        if result['stdout']:
            output += f"**Partial output before error:**\n```\n{result['stdout']}\n```\n\n"
    
    return output


def should_retry_code(error_message: str, retry_count: int, max_retries: int = 2) -> bool:
    """
    Determine if code execution should be retried
    
    Args:
        error_message: The error message from failed execution
        retry_count: Current number of retries
        max_retries: Maximum number of retries allowed
    
    Returns:
        True if should retry, False otherwise
    """
    if retry_count >= max_retries:
        return False
    
    # Retry for common fixable errors
    retryable_errors = [
        'NameError',
        'KeyError',
        'AttributeError',
        'ValueError',
        'TypeError',
        'SyntaxError'
    ]
    
    return any(error in error_message for error in retryable_errors)


def create_retry_prompt(original_question: str, code: str, error: str) -> str:
    """
    Create a prompt for retrying failed code execution
    
    Args:
        original_question: The original user question
        code: The code that failed
        error: The error message
    
    Returns:
        Prompt for the LLM to fix the code
    """
    return f"""The previous code failed with an error. Please analyze the error and provide corrected code.

**Original Question:** {original_question}

**Failed Code:**
```python
{code}
```

**Error:**
```
{error}
```

Please provide corrected Python code that fixes this error. Explain what went wrong and how you fixed it."""
