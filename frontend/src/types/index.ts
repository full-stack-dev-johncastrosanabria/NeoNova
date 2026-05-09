export interface User {
  id: string;
  email: string;
  display_name: string;
  created_at: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface Memory {
  id: string;
  user_id: string;
  type: string;
  content: string;
  importance: number;
  is_active: boolean;
  created_at: string;
}

export interface Feedback {
  id: string;
  message_id: string;
  rating?: number;
  comment?: string;
  correction?: string;
  created_at: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: string;
}
