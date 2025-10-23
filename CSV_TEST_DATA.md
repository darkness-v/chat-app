# Test CSV Files for Data Analysis

## Sample CSV for Testing

You can use these public CSV URLs to test the data analysis feature:

### 1. Iris Dataset (Classic ML Dataset)
```
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv
```
- 150 rows, 5 columns
- Species classification data
- **Example questions:**
  - "Show summary statistics for each species"
  - "Plot the distribution of sepal length"
  - "Create a scatter plot of sepal length vs petal length"

### 2. Tips Dataset (Restaurant Tips)
```
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv
```
- 244 rows, 7 columns
- Restaurant tipping data
- **Example questions:**
  - "What's the average tip percentage?"
  - "Show tips by day of week"
  - "Plot the relationship between total bill and tip"

### 3. Titanic Dataset
```
https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
```
- 891 rows, 12 columns
- Titanic passenger data
- **Example questions:**
  - "What was the survival rate?"
  - "Show survival rate by passenger class"
  - "Plot age distribution of survivors vs non-survivors"

### 4. Diamonds Dataset (Small Sample)
```
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv
```
- Price and characteristics of diamonds
- **Example questions:**
  - "What's the correlation between carat and price?"
  - "Show average price by cut quality"
  - "Plot a histogram of diamond prices"

### 5. Car MPG Dataset
```
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv
```
- Car fuel efficiency data
- **Example questions:**
  - "What's the average MPG by origin?"
  - "Show correlation between weight and MPG"
  - "Plot MPG over model years"

## Creating Your Own Test CSV

Create a simple CSV file:

```csv
name,age,salary,department
Alice,28,75000,Engineering
Bob,35,85000,Engineering
Carol,42,95000,Management
David,31,70000,Sales
Eve,29,72000,Sales
Frank,38,90000,Management
Grace,26,65000,Engineering
Henry,45,100000,Management
Iris,33,78000,Sales
Jack,27,68000,Engineering
```

Save as `employees.csv` and try:
- "What's the average salary by department?"
- "Show age distribution"
- "Plot salary by department as a bar chart"

## Local File Testing

1. Save any CSV file to your computer
2. Upload it via the web interface
3. Start analyzing!

## Tips for Best Results

1. **Start Simple**: Begin with "Summarize the dataset" or "Show me the columns"
2. **Be Specific**: Mention exact column names in your questions
3. **Progressive Analysis**: Build on previous results
4. **Visualizations**: Request specific plot types (histogram, scatter, bar, etc.)
5. **Multiple Questions**: Ask follow-up questions based on results

## Common Analysis Patterns

### Pattern 1: Initial Exploration
```
1. "Summarize the dataset"
2. "Show basic statistics"
3. "Which columns have missing values?"
```

### Pattern 2: Distribution Analysis
```
1. "Show the distribution of [column_name]"
2. "Plot a histogram of [column_name]"
3. "What are the outliers in [column_name]?"
```

### Pattern 3: Relationship Analysis
```
1. "Show correlation between all numeric columns"
2. "Plot [column_a] vs [column_b]"
3. "Is there a relationship between [column_a] and [column_b]?"
```

### Pattern 4: Group Analysis
```
1. "Show average [metric] by [category]"
2. "Group the data by [column] and count"
3. "Compare [metric] across different [categories]"
```

## Troubleshooting Test Data

### URL not working?
- Ensure URL points directly to CSV file (not HTML page)
- Use "raw" GitHub URLs
- Check URL is publicly accessible

### Upload fails?
- Verify file is CSV format
- Check file size (< 100MB recommended)
- Ensure proper encoding (UTF-8 recommended)

### Analysis errors?
- Check column names match question
- Verify data types (numeric for calculations)
- Look at error message for hints

## Advanced Test Scenarios

### Large Dataset Testing
For stress testing, use larger datasets:
- [New York Taxi Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

### Complex Analysis
Try multi-step analysis:
1. "Filter rows where price > 100"
2. "For filtered data, show average by category"
3. "Plot the results as a bar chart"

### Error Recovery Testing
Intentionally use wrong column names to test retry logic:
- "Show statistics for column_that_doesnt_exist"
- AI should catch error and ask for clarification

Enjoy testing! 🧪📊
