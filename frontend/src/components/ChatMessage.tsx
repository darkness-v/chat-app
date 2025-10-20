import { Message } from '@/types';
import { format } from 'date-fns';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const timestamp = format(new Date(message.timestamp), 'HH:mm');

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
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
        </div>
        <div className={`text-xs text-gray-400 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {isUser ? 'You' : 'Assistant'} · {timestamp}
        </div>
      </div>
    </div>
  );
}
