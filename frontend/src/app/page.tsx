'use client';

import { useState, useEffect, useRef } from 'react';
import ChatMessage from '@/components/ChatMessage';
import ChatInput from '@/components/ChatInput';
import { Message } from '@/types';

const CHAT_SERVICE_URL = process.env.NEXT_PUBLIC_CHAT_SERVICE_URL || 'http://localhost:8001';
const STORAGE_SERVICE_URL = process.env.NEXT_PUBLIC_STORAGE_SERVICE_URL || 'http://localhost:8002';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize conversation
  useEffect(() => {
    const initConversation = async () => {
      try {
        const response = await fetch(`${STORAGE_SERVICE_URL}/api/conversations`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: 'New Conversation' }),
        });
        const data = await response.json();
        setConversationId(data.id);
        
        // Load existing messages
        await loadMessages(data.id);
      } catch (error) {
        console.error('Error initializing conversation:', error);
      }
    };

    initConversation();
  }, []);

  const loadMessages = async (convId: number) => {
    try {
      const response = await fetch(`${STORAGE_SERVICE_URL}/api/conversations/${convId}/messages`);
      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!conversationId || !content.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
      conversation_id: conversationId,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setIsStreaming(true);

    try {
      const response = await fetch(`${CHAT_SERVICE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: content.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('No reader available');
      }

      let assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '',
        timestamp: new Date().toISOString(),
        conversation_id: conversationId,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.error) {
                console.error('Stream error:', data.error);
                break;
              }

              if (data.done) {
                setIsStreaming(false);
                // Reload messages to get the final saved version
                await loadMessages(conversationId);
                break;
              }

              if (data.content) {
                assistantMessage.content += data.content;
                setMessages((prev) => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = { ...assistantMessage };
                  return newMessages;
                });
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 2,
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date().toISOString(),
          conversation_id: conversationId,
        },
      ]);
    } finally {
      setIsLoading(false);
      setIsStreaming(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50">
      <div className="w-full max-w-4xl h-[90vh] bg-white rounded-lg shadow-xl flex flex-col">
        {/* Header */}
        <div className="bg-primary text-white p-4 rounded-t-lg">
          <h1 className="text-2xl font-bold">Chat Application</h1>
          <p className="text-sm text-blue-100">Multi-turn conversation with AI</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-400 mt-10">
              <p className="text-lg">Start a conversation!</p>
              <p className="text-sm mt-2">Your messages will be saved automatically</p>
            </div>
          )}
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && messages[messages.length - 1]?.role !== 'assistant' && (
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-semibold">
                AI
              </div>
              <div className="flex-1 bg-gray-100 rounded-lg p-4">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <ChatInput onSend={handleSendMessage} disabled={isLoading || !conversationId} />
      </div>
    </main>
  );
}
