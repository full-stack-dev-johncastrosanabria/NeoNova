import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  Conversation,
  Message,
  Memory,
  Feedback,
  LoginResponse,
} from '../types';

export class APIClient {
  private readonly axiosInstance: AxiosInstance;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.axiosInstance = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor: attach Bearer token when available
    this.axiosInstance.interceptors.request.use((config) => {
      if (this.token) {
        config.headers['Authorization'] = `Bearer ${this.token}`;
      }
      return config;
    });

    // Response interceptor: clear token on 401
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.clearToken();
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string): void {
    this.token = token;
  }

  clearToken(): void {
    this.token = null;
  }

  async register(
    email: string,
    password: string,
    displayName: string
  ): Promise<User> {
    try {
      const response = await this.axiosInstance.post<User>('/auth/register', {
        email,
        password,
        display_name: displayName,
      });
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await this.axiosInstance.post<LoginResponse>(
        '/auth/login',
        { email, password }
      );
      this.setToken(response.data.token);
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async createConversation(title: string): Promise<Conversation> {
    try {
      const response = await this.axiosInstance.post<Conversation>(
        '/conversations',
        { title }
      );
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async listConversations(): Promise<Conversation[]> {
    try {
      const response = await this.axiosInstance.get<Conversation[]>(
        '/conversations'
      );
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async sendMessage(
    conversationId: string,
    content: string
  ): Promise<Message[]> {
    try {
      const response = await this.axiosInstance.post<Message[]>(
        `/conversations/${conversationId}/messages`,
        { content }
      );
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async listMessages(conversationId: string): Promise<Message[]> {
    try {
      const response = await this.axiosInstance.get<Message[]>(
        `/conversations/${conversationId}/messages`
      );
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async listMemories(): Promise<Memory[]> {
    try {
      const response = await this.axiosInstance.get<Memory[]>('/memories');
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async createMemory(
    type: string,
    content: string,
    importance: number
  ): Promise<Memory> {
    try {
      const response = await this.axiosInstance.post<Memory>('/memories', {
        type,
        content,
        importance,
      });
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async deactivateMemory(memoryId: string): Promise<Memory> {
    try {
      const response = await this.axiosInstance.delete<Memory>(
        `/memories/${memoryId}`
      );
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  async createFeedback(
    messageId: string,
    rating?: number,
    comment?: string,
    correction?: string
  ): Promise<Feedback> {
    try {
      const response = await this.axiosInstance.post<Feedback>('/feedback', {
        message_id: messageId,
        rating,
        comment,
        correction,
      });
      return response.data;
    } catch (error) {
      throw this._normalizeError(error);
    }
  }

  private _normalizeError(error: unknown): Error {
    if (axios.isAxiosError(error)) {
      const message =
        error.response?.data?.message ??
        error.response?.data?.error ??
        error.message;
      return new Error(message);
    }
    if (error instanceof Error) {
      return error;
    }
    return new Error('An unexpected network error occurred');
  }
}

export const apiClient = new APIClient(
  import.meta.env.VITE_API_URL || 'http://localhost:8000'
);
