import { useState, useRef } from 'react';

interface CSVUploadProps {
  onUpload: (csvPath: string, filename: string) => void;
  disabled?: boolean;
}

export default function CSVUpload({ onUpload, disabled }: CSVUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [csvUrl, setCsvUrl] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8002/api/upload-csv', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload CSV');
      }

      const data = await response.json();
      onUpload(data.csv_path, data.filename);
      
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleUrlSubmit = () => {
    if (!csvUrl.trim()) return;

    // Basic URL validation
    try {
      new URL(csvUrl);
      onUpload(csvUrl, 'Remote CSV');
      setCsvUrl('');
    } catch {
      setError('Please enter a valid URL');
    }
  };

  return (
    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
      <h3 className="font-semibold text-blue-900 mb-3">📊 CSV Data Analysis</h3>
      
      {/* File Upload */}
      <div className="mb-3">
        <label className="block text-sm text-gray-700 mb-2">Upload CSV File:</label>
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          disabled={uploading || disabled}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-500 file:text-white hover:file:bg-blue-600 disabled:opacity-50"
        />
      </div>

      {/* URL Input */}
      <div className="mb-3">
        <label className="block text-sm text-gray-700 mb-2">Or enter CSV URL:</label>
        <div className="flex space-x-2">
          <input
            type="text"
            value={csvUrl}
            onChange={(e) => setCsvUrl(e.target.value)}
            placeholder="https://example.com/data.csv"
            disabled={uploading || disabled}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            onClick={handleUrlSubmit}
            disabled={!csvUrl.trim() || uploading || disabled}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Load
          </button>
        </div>
      </div>

      {/* Loading State */}
      {uploading && (
        <div className="text-sm text-blue-600">
          Uploading CSV file...
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="text-sm text-red-600 bg-red-50 p-2 rounded">
          {error}
        </div>
      )}

      {/* Help Text */}
      <div className="mt-3 text-xs text-gray-600">
        <p className="font-semibold mb-1">Example questions:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>Summarize the dataset</li>
          <li>Show basic statistics for numeric columns</li>
          <li>Which column has the most missing values?</li>
          <li>Plot a histogram of the price column</li>
          <li>Show correlation between variables</li>
        </ul>
      </div>
    </div>
  );
}
