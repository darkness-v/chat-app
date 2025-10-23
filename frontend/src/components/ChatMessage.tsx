import { Message } from '@/types';
import { format } from 'date-fns';
import Image from 'next/image';

interface ChatMessageProps {
  message: Message;
  plots?: string[]; // Base64 encoded plots
}

const STORAGE_SERVICE_URL = process.env.NEXT_PUBLIC_STORAGE_SERVICE_URL || 'http://localhost:8002';

export default function ChatMessage({ message, plots }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const timestamp = format(new Date(message.timestamp), 'HH:mm');

  // Format message content with code blocks
  const formatContent = (content: string) => {
    // Split by code blocks
    const parts = content.split(/(```[\s\S]*?```)/g);
    
    return parts.map((part, index) => {
      if (part.startsWith('```')) {
        // Extract code and language
        const lines = part.split('\n');
        const firstLine = lines[0].replace('```', '');
        const code = lines.slice(1, -1).join('\n');
        
        return (
          <pre key={index} className="bg-gray-800 text-gray-100 p-3 rounded my-2 overflow-x-auto text-sm">
            <code>{code}</code>
          </pre>
        );
      }
      
      // Check for bold markers
      const boldParts = part.split(/(\*\*.*?\*\*)/g);
      return boldParts.map((boldPart, boldIndex) => {
        if (boldPart.startsWith('**') && boldPart.endsWith('**')) {
          return <strong key={`${index}-${boldIndex}`}>{boldPart.slice(2, -2)}</strong>;
        }
        return <span key={`${index}-${boldIndex}`}>{boldPart}</span>;
      });
    });
  };

  return (
    <div className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-semibold flex-shrink-0 ${
          isUser ? 'bg-green-500' : 'bg-primary'
        }`}
      >
        {isUser ? 'U' : 'AI'}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`rounded-lg p-4 ${
            isUser
              ? 'bg-green-500 text-white ml-auto'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {/* Display image if present */}
          {message.image_url && (
            <div className="mb-3">
              <img 
                src={`${STORAGE_SERVICE_URL}${message.image_url}`}
                alt="Uploaded image"
                className="max-w-full rounded-lg max-h-64 object-contain"
              />
            </div>
          )}
          
          {/* Display message content with formatting */}
          <div className="whitespace-pre-wrap break-words">
            {formatContent(message.content)}
          </div>
          
          {/* Display plots if present */}
          {plots && plots.length > 0 && (
            <div className="mt-4 space-y-3">
              {plots.map((plot, index) => (
                <div key={index} className="bg-white p-2 rounded">
                  <img 
                    src={`data:image/png;base64,${plot}`}
                    alt={`Plot ${index + 1}`}
                    className="max-w-full rounded"
                  />
                </div>
              ))}
            </div>
          )}
        </div>
        <div className={`text-xs text-gray-400 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {isUser ? 'You' : 'Assistant'} · {timestamp}
        </div>
      </div>
    </div>
  );
}
