/**
 * Modern API Client with TanStack Query
 * Provides type-safe, async-first HTTP requests
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message)
    this.name = 'APIError'
  }
}

interface RequestOptions extends RequestInit {
  token?: string
}

/**
 * Core fetch wrapper with error handling
 */
async function fetchAPI<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }

  // Merge custom headers
  if (fetchOptions.headers) {
    Object.assign(headers, fetchOptions.headers)
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new APIError(
      errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
      response.status,
      errorData
    )
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

/**
 * Get auth token from localStorage
 */
export function getAuthToken(): string | null {
  return localStorage.getItem('token')
}

/**
 * Set auth token in localStorage
 */
export function setAuthToken(token: string): void {
  localStorage.setItem('token', token)
}

/**
 * Remove auth token from localStorage
 */
export function clearAuthToken(): void {
  localStorage.removeItem('token')
}

// ============================================================================
// Auth API
// ============================================================================

export interface RegisterRequest {
  email: string
  password: string
  display_name: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface AuthResponse {
  token: string
  user: {
    id: string
    email: string
  }
}

export const authAPI = {
  register: (data: RegisterRequest) =>
    fetchAPI<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  login: (data: LoginRequest) =>
    fetchAPI<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
}

// ============================================================================
// Conversations API
// ============================================================================

export interface Conversation {
  id: string
  user_id: string
  title: string
  created_at: string
  updated_at: string
}

export interface CreateConversationRequest {
  title: string
}

export const conversationsAPI = {
  list: () =>
    fetchAPI<Conversation[]>('/conversations/', {
      token: getAuthToken() || undefined,
    }),

  create: (data: CreateConversationRequest) =>
    fetchAPI<Conversation>('/conversations/', {
      method: 'POST',
      body: JSON.stringify(data),
      token: getAuthToken() || undefined,
    }),

  delete: (id: string) =>
    fetchAPI<void>(`/conversations/${id}`, {
      method: 'DELETE',
      token: getAuthToken() || undefined,
    }),
}

// ============================================================================
// Messages API
// ============================================================================

export interface Message {
  id: string
  conversation_id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface SendMessageRequest {
  content: string
}

export const messagesAPI = {
  list: (conversationId: string) =>
    fetchAPI<Message[]>(`/conversations/${conversationId}/messages`, {
      token: getAuthToken() || undefined,
    }),

  send: (conversationId: string, data: SendMessageRequest) =>
    fetchAPI<Message[]>(`/conversations/${conversationId}/messages`, {
      method: 'POST',
      body: JSON.stringify(data),
      token: getAuthToken() || undefined,
    }),
}

// ============================================================================
// Memories API
// ============================================================================

export interface Memory {
  id: string
  user_id: string
  memory_type: 'preference' | 'fact' | 'instruction' | 'correction'
  content: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface CreateMemoryRequest {
  memory_type: 'preference' | 'fact' | 'instruction' | 'correction'
  content: string
}

export const memoriesAPI = {
  list: () =>
    fetchAPI<Memory[]>('/memories/', {
      token: getAuthToken() || undefined,
    }),

  create: (data: CreateMemoryRequest) =>
    fetchAPI<Memory>('/memories/', {
      method: 'POST',
      body: JSON.stringify(data),
      token: getAuthToken() || undefined,
    }),

  delete: (id: string) =>
    fetchAPI<void>(`/memories/${id}`, {
      method: 'DELETE',
      token: getAuthToken() || undefined,
    }),
}

// ============================================================================
// Feedback API
// ============================================================================

export interface CreateFeedbackRequest {
  message_id: string
  rating?: number
  correction?: string
}

export interface Feedback {
  id: string
  message_id: string
  user_id: string
  rating?: number
  correction?: string
  created_at: string
}

export const feedbackAPI = {
  create: (data: CreateFeedbackRequest) =>
    fetchAPI<Feedback>('/feedback/', {
      method: 'POST',
      body: JSON.stringify(data),
      token: getAuthToken() || undefined,
    }),
}
