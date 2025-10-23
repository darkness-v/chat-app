export interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant';
  content: string;
  image_url?: string;
  plots?: string[];  // Base64 encoded plots
  timestamp: string;
  feedback?: 'like' | 'dislike' | null;  // User feedback on assistant messages
}

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}
