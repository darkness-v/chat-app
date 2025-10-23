'use client';

import { useState, useEffect, useRef } from 'react';
import ChatMessage from '@/components/ChatMessage';
import ChatInput from '@/components/ChatInput';
import CSVUpload from '@/components/CSVUpload';
import Sidebar from '@/components/Sidebar';
import { Message, Conversation } from '@/types';

const CHAT_SERVICE_URL = process.env.NEXT_PUBLIC_CHAT_SERVICE_URL || 'http://localhost:8001';
const STORAGE_SERVICE_URL = process.env.NEXT_PUBLIC_STORAGE_SERVICE_URL || 'http://localhost:8002';

export default function Home() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [csvMode, setCsvMode] = useState(false);
  const [csvPath, setCsvPath] = useState<string | null>(null);
  const [csvFilename, setCsvFilename] = useState<string | null>(null);
  const [messagePlots, setMessagePlots] = useState<Record<number, string[]>>({});
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const firstMessageSentRef = useRef(false);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load all conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const response = await fetch(`${STORAGE_SERVICE_URL}/api/conversations`);
      const data = await response.json();
      setConversations(data);
      
      // If no conversations, create a new one
      if (data.length === 0) {
        await createNewConversation();
      } else {
        // Load the most recent conversation
        const mostRecent = data[0];
        await loadConversation(mostRecent.id);
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const createNewConversation = async () => {
    try {
      const response = await fetch(`${STORAGE_SERVICE_URL}/api/conversations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New Conversation' }),
      });
      const newConv = await response.json();
      
      setConversations((prev) => [newConv, ...prev]);
      setConversationId(newConv.id);
      setMessages([]);
      setCsvMode(false);
      setCsvPath(null);
      setCsvFilename(null);
      setMessagePlots({});
      firstMessageSentRef.current = false;
      setSidebarOpen(false); // Close sidebar on mobile
    } catch (error) {
      console.error('Error creating conversation:', error);
    }
  };

  const loadConversation = async (convId: number) => {
    try {
      setConversationId(convId);
      await loadMessages(convId);
      setCsvMode(false);
      setCsvPath(null);
      setCsvFilename(null);
      setSidebarOpen(false); // Close sidebar on mobile
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const deleteConversation = async (convId: number) => {
    try {
      await fetch(`${STORAGE_SERVICE_URL}/api/conversations/${convId}`, {
        method: 'DELETE',
      });
      
      const remainingConversations = conversations.filter((c) => c.id !== convId);
      setConversations(remainingConversations);
      
      // If deleted current conversation, handle appropriately
      if (convId === conversationId) {
        if (remainingConversations.length > 0) {
          // Load the most recent remaining conversation
          await loadConversation(remainingConversations[0].id);
        } else {
          // No conversations left, create a new one
          await createNewConversation();
        }
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const updateConversationTitle = async (convId: number, title: string) => {
    try {
      await fetch(`${STORAGE_SERVICE_URL}/api/conversations/${convId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      });
      
      setConversations((prev) =>
        prev.map((c) => (c.id === convId ? { ...c, title } : c))
      );
    } catch (error) {
      console.error('Error updating conversation title:', error);
    }
  };

  const loadMessages = async (convId: number) => {
    try {
      const response = await fetch(`${STORAGE_SERVICE_URL}/api/conversations/${convId}/messages`);
      const data = await response.json();
      setMessages(data);
      
      // Load plots from messages into messagePlots state
      const plots: Record<number, string[]> = {};
      data.forEach((msg: Message) => {
        if (msg.plots && msg.plots.length > 0) {
          plots[msg.id] = msg.plots;
        }
      });
      setMessagePlots(plots);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const handleCSVUpload = (path: string, filename: string) => {
    setCsvPath(path);
    setCsvFilename(filename);
    setCsvMode(true);
    
    // Add system message
    const systemMessage: Message = {
      id: Date.now(),
      role: 'assistant',
      content: `📊 CSV file "${filename}" loaded successfully! You can now ask questions about the data.\n\nTry asking:\n- "Summarize the dataset"\n- "Show basic statistics"\n- "Plot a histogram of [column_name]"`,
      timestamp: new Date().toISOString(),
      conversation_id: conversationId!,
    };
    setMessages((prev) => [...prev, systemMessage]);
  };

  const handleClearCSV = async () => {
    if (conversationId && csvMode) {
      try {
        await fetch(`${CHAT_SERVICE_URL}/api/csv-analysis/clear/${conversationId}`, {
          method: 'POST',
        });
      } catch (error) {
        console.error('Error clearing CSV:', error);
      }
    }
    setCsvMode(false);
    setCsvPath(null);
    setCsvFilename(null);
  };

  const handleSendCSVMessage = async (content: string) => {
    if (!conversationId || !csvPath || !content.trim()) return;

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

    // Auto-generate title from first message
    if (!firstMessageSentRef.current) {
      firstMessageSentRef.current = true;
      const title = content.trim().slice(0, 50) + (content.length > 50 ? '...' : '');
      await updateConversationTitle(conversationId, title);
    }

    try {
      const response = await fetch(`${CHAT_SERVICE_URL}/api/csv-analysis/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: content.trim(),
          csv_path: csvPath,
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

      const plots: string[] = [];
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
                assistantMessage.content += `\n\n❌ Error: ${data.error}`;
                setMessages((prev) => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = { ...assistantMessage };
                  return newMessages;
                });
                break;
              }

              if (data.done) {
                setIsStreaming(false);
                // Save plots for this message
                if (plots.length > 0) {
                  setMessagePlots((prev) => ({
                    ...prev,
                    [assistantMessage.id]: plots
                  }));
                }
                // Reload messages to get the saved version with plots
                await loadMessages(conversationId);
                break;
              }

              if (data.type === 'image') {
                // Handle plot image
                plots.push(data.data);
                // Force re-render with updated plots
                setMessagePlots((prev) => ({
                  ...prev,
                  [assistantMessage.id]: [...plots]
                }));
              } else if (data.content) {
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

  const handleSendMessage = async (content: string, imageFile?: File) => {
    // Route to CSV handler if in CSV mode
    if (csvMode && !imageFile) {
      return handleSendCSVMessage(content);
    }

    if (!conversationId || (!content.trim() && !imageFile)) return;

    let imageUrl: string | undefined;
    
    if (imageFile) {
      try {
        const formData = new FormData();
        formData.append('file', imageFile);
        
        const uploadResponse = await fetch(`${STORAGE_SERVICE_URL}/api/upload-image`, {
          method: 'POST',
          body: formData,
        });
        
        if (!uploadResponse.ok) {
          throw new Error('Failed to upload image');
        }
        
        const uploadData = await uploadResponse.json();
        imageUrl = uploadData.image_url;
      } catch (error) {
        console.error('Error uploading image:', error);
        alert('Failed to upload image. Please try again.');
        return;
      }
    }

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: content.trim() || '(Image)',
      image_url: imageUrl,
      timestamp: new Date().toISOString(),
      conversation_id: conversationId,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setIsStreaming(true);

    // Auto-generate title from first message
    if (!firstMessageSentRef.current && content.trim()) {
      firstMessageSentRef.current = true;
      const title = content.trim().slice(0, 50) + (content.length > 50 ? '...' : '');
      await updateConversationTitle(conversationId, title);
    }

    try {
      const response = await fetch(`${CHAT_SERVICE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: content.trim() || 'What is in this image?',
          image_url: imageUrl,
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
    <main className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        currentConversationId={conversationId}
        onSelectConversation={loadConversation}
        onNewConversation={createNewConversation}
        onDeleteConversation={deleteConversation}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="w-full max-w-5xl mx-auto h-full bg-white shadow-xl flex flex-col">
          {/* Header */}
          <div className="bg-primary text-white p-4">
            <div className="flex justify-between items-center">
              <div className="flex-1 ml-0 md:ml-0">
                <h1 className="text-2xl font-bold">Chat Application</h1>
                <p className="text-sm text-blue-100">
                  {csvMode ? `📊 CSV Analysis: ${csvFilename}` : 'Multi-turn conversation with AI'}
                </p>
              </div>
              {csvMode && (
                <button
                  onClick={handleClearCSV}
                  className="px-3 py-1 bg-red-500 hover:bg-red-600 rounded text-sm transition-colors"
                >
                  Clear CSV
                </button>
              )}
            </div>
          </div>

          {/* CSV Upload Section */}
          {!csvMode && conversationId && (
            <div className="p-4 border-b">
              <CSVUpload onUpload={handleCSVUpload} disabled={isLoading} />
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-400 mt-10">
                <p className="text-lg">Start a conversation!</p>
                <p className="text-sm mt-2">Upload a CSV file for data analysis or chat normally</p>
              </div>
            )}
            {messages.map((message) => (
              <ChatMessage 
                key={message.id} 
                message={message} 
                plots={messagePlots[message.id]}
              />
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
      </div>
    </main>
  );
}
