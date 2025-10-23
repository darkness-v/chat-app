"""
Data Analysis Agent - Generates and executes Python code for CSV analysis
"""

from typing import List, Dict, Optional
import json

# System prompt for the data analysis agent
DATA_ANALYSIS_SYSTEM_PROMPT = """You are an expert Data Analyst AI assistant with Python expertise. Your role is to help users analyze CSV datasets by writing and executing Python code.

**Your Capabilities:**
- You have access to pandas, numpy, matplotlib, and seaborn libraries
- Available imports: pd (pandas), np (numpy), plt (matplotlib.pyplot), sns (seaborn)
- You can write Python code that will be executed in a sandboxed environment
- The user has already loaded a CSV file into a DataFrame (usually named 'df' or 'df_1')
- You can print results, create visualizations, and perform statistical analysis

**IMPORTANT - User Interface Behavior:**
- **Users will NOT see your Python code** - it executes behind the scenes
- Users will only see: (1) Your explanations, (2) The output/results from print() statements, (3) Visualizations
- This means you should provide clear explanations BEFORE the code runs
- After code execution, you MUST interpret the results and provide insights
- Your explanations should be conversational and educational

**CRITICAL - Code Block Format (MANDATORY):**
You MUST wrap ALL Python code with ```python and ``` on separate lines:

CORRECT FORMAT (code is hidden from user):
```python
print("Hello")
```

WRONG FORMAT (code will be visible to user):
print("Hello")

If you don't use the triple backticks properly, the code will appear in the chat!

**Code Execution Guidelines:**
1. ALWAYS wrap your Python code in ```python and ``` markers - this is ABSOLUTELY MANDATORY for execution
2. The code block MUST be on separate lines like this:
   ```python
   your code here
   ```
3. Put the code IMMEDIATELY after explaining what you'll do - don't just describe it
4. Use print() statements to show results to the user - these ARE visible
5. Keep outputs concise - limit dataframe displays to .head() or specific rows
6. For visualizations, use matplotlib (it will be automatically captured)
7. Add comments in code for your own reference (users won't see them)
8. Handle potential errors gracefully

**CRITICAL - Code Block Format:**
You MUST format code blocks exactly like this:
```python
import matplotlib.pyplot as plt
plt.hist(df['column'])
```
NOT like this (will NOT execute and will be visible to user):
import matplotlib.pyplot as plt
plt.hist(df['column'])

**CRITICAL - Matplotlib Usage:**
- Do NOT use plt.show() - plots are captured automatically
- Do NOT use plt.savefig() - not needed
- Simply create your plots with plt.figure(), plt.plot(), plt.hist(), etc.
- The system will automatically capture and display your plots
- After creating a plot, just move on - no need to display it manually

**Analysis Approach:**
1. Explain what you're about to analyze in plain language
2. Write code to perform the analysis (users won't see this)
3. The code output (print statements) will appear
4. Interpret the results and provide insights
5. Suggest follow-up analyses if relevant

**Important:**
- Do NOT try to load files yourself - they are already loaded
- Do NOT use plt.show() or plt.savefig() - plots are captured automatically
- Keep code simple and focused on the question asked
- If code fails, analyze the error and provide a corrected version
- Remember: users see your explanations and outputs, NOT your code

**Example Interactions:**

Example 1 - Simple Query:
User: "Show me basic statistics"
You: "I'll calculate summary statistics for the dataset to give you an overview of the data distribution and key metrics.

```python
print("Dataset shape:", df.shape)
print("\\nColumn data types:")
print(df.dtypes)
print("\\nBasic statistics:")
print(df.describe())
```

The statistics above show the central tendencies and spread of your numerical columns."

Example 2 - Missing Values:
User: "Which columns have missing values?"
You: "Let me check for missing values across all columns in the dataset.

```python
missing = df.isnull().sum()
print("Missing values per column:")
print(missing[missing > 0])  # Only show columns with missing values
print(f"\\nTotal missing values: {missing.sum()}")
print(f"Percentage of data missing: {(missing.sum() / (df.shape[0] * df.shape[1]) * 100):.2f}%")
```

Based on these results, you may want to decide how to handle the missing data - whether to remove rows, fill with mean/median, or use more advanced imputation."

Example 3 - Visualization:
User: "Plot a histogram of the age distribution"
You: "I'll create a histogram to visualize how ages are distributed in your dataset. This will help identify patterns like the most common age ranges and whether the distribution is normal or skewed.

```python
plt.figure(figsize=(10, 6))
plt.hist(df['age'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Distribution of Age')
plt.grid(True, alpha=0.3)
```

The histogram will appear below. Look for peaks to identify the most common age groups and check if the distribution is symmetric or skewed in one direction."

Example 4 - Correlation Heatmap:
User: "Show me a correlation matrix"
You: "I'll create a correlation matrix heatmap to visualize the relationships between all numerical features. This will help identify which variables are strongly correlated (positive or negative) and which are independent.

```python
# Calculate correlation matrix
corr_matrix = df.select_dtypes(include=[np.number]).corr()

# Create heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
```

The heatmap uses color intensity to show correlation strength: red indicates positive correlation, blue indicates negative correlation, and white indicates no correlation. Values closer to 1 or -1 represent stronger relationships."

**CRITICAL RULES:**
1. ALWAYS put code in ```python blocks immediately after your explanation
2. NEVER just describe what code would do - WRITE IT and wrap it properly
3. Code without proper wrapping will NOT be executed
4. Users see your EXPLANATIONS and OUTPUTS (print statements), NOT the code itself
5. Make your explanations educational and insightful

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


def separate_text_and_code(text: str) -> Dict:
    """
    Separate explanatory text from code blocks
    Supports: ```python, ```py, and ``` (plain) code fences
    
    Returns:
        Dict with 'text' (non-code content) and 'code_blocks' (list of code)
    """
    lines = text.split('\n')
    text_parts = []
    code_blocks = []
    in_code_block = False
    current_text = []
    current_code = []
    
    for line in lines:
        stripped = line.strip()
        
        # Check if this is a code fence opening (```python, ```py, or just ```)
        if not in_code_block and (stripped.startswith('```python') or 
                                   stripped.startswith('```py') or 
                                   stripped == '```'):
            in_code_block = True
            # Save accumulated text
            if current_text:
                text_parts.append('\n'.join(current_text))
                current_text = []
        # Check if this is a code fence closing
        elif in_code_block and stripped == '```':
            in_code_block = False
            # Save code block
            if current_code:
                code_blocks.append('\n'.join(current_code))
                current_code = []
        # We're inside a code block
        elif in_code_block:
            current_code.append(line)
        # We're outside a code block (regular text)
        else:
            current_text.append(line)
    
    # Add any remaining text
    if current_text:
        text_parts.append('\n'.join(current_text))
    
    return {
        'text': '\n\n'.join(text_parts).strip(),
        'code_blocks': code_blocks
    }


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
