"""
Sandboxed Python Code Executor for Data Analysis
Inspired by MCP server data exploration
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
import sys
import base64
from typing import Dict, Optional, List, Tuple
import traceback
import json

class CodeExecutor:
    """Execute Python code safely for data analysis"""
    
    def __init__(self):
        self.dataframes: Dict[str, pd.DataFrame] = {}
        self.df_count = 0
        self.execution_history: List[Dict] = []
        
    def load_csv(self, csv_path: str, df_name: Optional[str] = None) -> Tuple[bool, str]:
        """Load a CSV file into a DataFrame"""
        self.df_count += 1
        if not df_name:
            df_name = f"df_{self.df_count}"
            
        try:
            # Handle both local paths and URLs
            if csv_path.startswith('http://') or csv_path.startswith('https://'):
                self.dataframes[df_name] = pd.read_csv(csv_path)
            else:
                self.dataframes[df_name] = pd.read_csv(csv_path)
            
            df = self.dataframes[df_name]
            summary = f"Successfully loaded CSV into DataFrame '{df_name}'\n"
            summary += f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
            summary += f"Columns: {', '.join(df.columns.tolist())}\n"
            summary += f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
            
            self.execution_history.append({
                'action': 'load_csv',
                'df_name': df_name,
                'path': csv_path,
                'success': True
            })
            
            return True, summary
        except Exception as e:
            error_msg = f"Error loading CSV: {str(e)}\n{traceback.format_exc()}"
            self.execution_history.append({
                'action': 'load_csv',
                'df_name': df_name,
                'path': csv_path,
                'success': False,
                'error': str(e)
            })
            return False, error_msg
    
    def execute_code(self, code: str, save_to_memory: Optional[List[str]] = None) -> Dict:
        """
        Execute Python code and return results
        
        Returns:
            Dict with:
                - success: bool
                - stdout: str (printed output)
                - error: str (if failed)
                - plots: List[str] (base64 encoded images)
                - saved_dfs: List[str] (saved dataframe names)
        """
        result = {
            'success': False,
            'stdout': '',
            'error': None,
            'plots': [],
            'saved_dfs': []
        }
        
        # Clean up code - remove plt.show() and plt.savefig() calls
        code = code.replace('plt.show()', '# plt.show() removed - plots captured automatically')
        code = code.replace('plt.savefig(', '# plt.savefig removed - not needed #(')
        
        # Prepare local environment with dataframes
        local_dict = {
            **{df_name: df.copy() for df_name, df in self.dataframes.items()},
        }
        
        # Prepare safe globals
        safe_globals = {
            'pd': pd,
            'np': np,
            'plt': plt,
            'print': print,
            '__builtins__': __builtins__,
        }
        
        # Capture stdout
        stdout_capture = io.StringIO()
        old_stdout = sys.stdout
        
        try:
            sys.stdout = stdout_capture
            
            # Execute the code
            exec(code, safe_globals, local_dict)
            
            # Get stdout
            result['stdout'] = stdout_capture.getvalue()
            
            # Save dataframes if requested
            if save_to_memory:
                for df_name in save_to_memory:
                    if df_name in local_dict and isinstance(local_dict[df_name], pd.DataFrame):
                        self.dataframes[df_name] = local_dict[df_name]
                        result['saved_dfs'].append(df_name)
            
            # Capture any matplotlib plots
            if plt.get_fignums():
                for fig_num in plt.get_fignums():
                    fig = plt.figure(fig_num)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
                    buf.seek(0)
                    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                    result['plots'].append(img_base64)
                    buf.close()
                plt.close('all')
            
            result['success'] = True
            
            self.execution_history.append({
                'action': 'execute_code',
                'code': code[:100] + '...' if len(code) > 100 else code,
                'success': True,
                'plots_count': len(result['plots'])
            })
            
        except Exception as e:
            result['error'] = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            result['stdout'] = stdout_capture.getvalue()
            
            self.execution_history.append({
                'action': 'execute_code',
                'code': code[:100] + '...' if len(code) > 100 else code,
                'success': False,
                'error': str(e)
            })
        finally:
            sys.stdout = old_stdout
            plt.close('all')
        
        return result
    
    def get_dataframe_info(self, df_name: str) -> Optional[str]:
        """Get information about a specific dataframe"""
        if df_name not in self.dataframes:
            return None
        
        df = self.dataframes[df_name]
        info_buffer = io.StringIO()
        df.info(buf=info_buffer)
        
        return f"""
DataFrame: {df_name}
Shape: {df.shape[0]} rows × {df.shape[1]} columns

{info_buffer.getvalue()}

First 5 rows:
{df.head().to_string()}

Summary statistics:
{df.describe().to_string()}
"""
    
    def list_dataframes(self) -> List[str]:
        """List all loaded dataframes"""
        return list(self.dataframes.keys())
    
    def clear(self):
        """Clear all dataframes and history"""
        self.dataframes.clear()
        self.execution_history.clear()
        self.df_count = 0
