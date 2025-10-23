import { Message } from '@/types';
import { format } from 'date-fns';
import Image from 'next/image';
import { useState } from 'react';

interface ChatMessageProps {
  message: Message;
  plots?: string[]; // Base64 encoded plots
  onFeedback?: (messageId: number, feedback: 'like' | 'dislike' | null) => void;
}

const STORAGE_SERVICE_URL = process.env.NEXT_PUBLIC_STORAGE_SERVICE_URL || 'http://localhost:8002';

export default function ChatMessage({ message, plots, onFeedback }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const timestamp = format(new Date(message.timestamp), 'HH:mm');
  const [currentFeedback, setCurrentFeedback] = useState<'like' | 'dislike' | null>(message.feedback || null);
  const [isHovered, setIsHovered] = useState(false);

  const handleFeedback = (feedback: 'like' | 'dislike') => {
    // Toggle feedback: if clicking the same button, remove feedback
    const newFeedback = currentFeedback === feedback ? null : feedback;
    setCurrentFeedback(newFeedback);
    onFeedback?.(message.id, newFeedback);
  };

  // Format message content with code blocks
  // Note: Code blocks with 'python' or 'py' language are hidden (executed in background)
  const formatContent = (content: string) => {
    // Split by code blocks
    const parts = content.split(/(```[\s\S]*?```)/g);
    
    return parts.map((part, index) => {
      if (part.startsWith('```')) {
        // Extract code and language
        const lines = part.split('\n');
        const firstLine = lines[0].replace('```', '').trim().toLowerCase();
        const code = lines.slice(1, -1).join('\n');
        
        // Hide Python code blocks (they're executed in background)
        if (firstLine === 'python' || firstLine === 'py' || firstLine === '') {
          // Don't render Python code blocks for assistant messages
          if (!isUser) {
            return null;
          }
        }
        
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
        
        {/* Feedback buttons - only show for assistant messages */}
        {!isUser && (
          <div 
            className="flex items-center gap-2 mt-2"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
          >
            <button
              onClick={() => handleFeedback('like')}
              className={`p-1.5 rounded-lg transition-all hover:bg-gray-200 ${
                currentFeedback === 'like' 
                  ? 'bg-green-100 text-green-600' 
                  : 'text-gray-400 hover:text-green-600'
              } ${!isHovered && !currentFeedback ? 'opacity-0' : 'opacity-100'}`}
              title="Good response"
              aria-label="Like this response"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill={currentFeedback === 'like' ? 'currentColor' : 'none'}
                viewBox="0 0 24 24" 
                strokeWidth={1.5} 
                stroke="currentColor" 
                className="w-4 h-4"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M6.633 10.5c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75A2.25 2.25 0 0116.5 4.5c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-.952a3.75 3.75 0 00-1.423-.23H6.75a2.25 2.25 0 01-2.25-2.25v-7.5A2.25 2.25 0 016.75 8.25h-.117z" />
              </svg>
            </button>
            
            <button
              onClick={() => handleFeedback('dislike')}
              className={`p-1.5 rounded-lg transition-all hover:bg-gray-200 ${
                currentFeedback === 'dislike' 
                  ? 'bg-red-100 text-red-600' 
                  : 'text-gray-400 hover:text-red-600'
              } ${!isHovered && !currentFeedback ? 'opacity-0' : 'opacity-100'}`}
              title="Bad response"
              aria-label="Dislike this response"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill={currentFeedback === 'dislike' ? 'currentColor' : 'none'}
                viewBox="0 0 24 24" 
                strokeWidth={1.5} 
                stroke="currentColor" 
                className="w-4 h-4"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 15h2.25m8.024-9.75c.011.05.028.1.052.148.591 1.2.924 2.55.924 3.977a8.96 8.96 0 01-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368.339 1.11.521 2.287.521 3.507 0 1.553-.295 3.036-.831 4.398C20.613 14.547 19.833 15 19 15h-1.053c-.472 0-.745-.556-.5-.96a8.95 8.95 0 00.303-.54m.023-8.25H16.48a4.5 4.5 0 01-1.423-.23l-3.114-.952a6.75 6.75 0 00-1.423-.23H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25h.117c.489 0 .977.078 1.423.23l3.114.952c.459.152.94.23 1.423.23h3.92c.618 0 1.217-.247 1.605-.729A11.95 11.95 0 0019.5 13.5c0-.435-.023-.863-.068-1.285-.045-1.021-.964-1.715-2.054-1.715h-3.126c-.618 0-.991-.724-.725-1.282.443-.975.703-2.066.703-3.218a2.25 2.25 0 00-2.25-2.25.75.75 0 00-.75.75v.072a4.498 4.498 0 01-.322 1.672c-.303.759-.93 1.331-1.653 1.715a9.041 9.041 0 00-2.861 2.4c-.498.634-1.225 1.08-2.031 1.08H3.75z" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
