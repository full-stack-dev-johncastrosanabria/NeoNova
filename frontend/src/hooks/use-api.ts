/**
 * Reusable TanStack Query hooks for API calls
 * Provides async-first, declarative data fetching with automatic caching,
 * refetching, and error handling
 */

import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryOptions,
  type UseMutationOptions,
} from '@tanstack/react-query'
import {
  authAPI,
  conversationsAPI,
  messagesAPI,
  memoriesAPI,
  feedbackAPI,
  setAuthToken,
  clearAuthToken,
  type AuthResponse,
  type Conversation,
  type Message,
  type Memory,
  type Feedback,
  type RegisterRequest,
  type LoginRequest,
  type CreateConversationRequest,
  type SendMessageRequest,
  type CreateMemoryRequest,
  type CreateFeedbackRequest,
} from '@/lib/api-client'

// ============================================================================
// Query Keys - Centralized for cache management
// ============================================================================

export const queryKeys = {
  conversations: ['conversations'] as const,
  messages: (conversationId: string) => ['messages', conversationId] as const,
  memories: ['memories'] as const,
}

// ============================================================================
// Auth Hooks
// ============================================================================

export function useRegister(
  options?: UseMutationOptions<AuthResponse, Error, RegisterRequest>
) {
  return useMutation({
    mutationFn: authAPI.register,
    onSuccess: (data, variables, context) => {
      setAuthToken(data.token)
      // Call the custom onSuccess if provided
      options?.onSuccess?.(data, variables, context)
    },
  })
}

export function useLogin(
  options?: UseMutationOptions<AuthResponse, Error, LoginRequest>
) {
  return useMutation({
    mutationFn: authAPI.login,
    onSuccess: (data, variables, context) => {
      setAuthToken(data.token)
      // Call the custom onSuccess if provided
      options?.onSuccess?.(data, variables, context)
    },
  })
}

export function useLogout() {
  const queryClient = useQueryClient()
  
  return () => {
    clearAuthToken()
    queryClient.clear() // Clear all cached data
    window.location.href = '/login'
  }
}

// ============================================================================
// Conversations Hooks
// ============================================================================

export function useConversations(
  options?: Omit<UseQueryOptions<Conversation[], Error>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: queryKeys.conversations,
    queryFn: conversationsAPI.list,
    staleTime: 30000, // Consider data fresh for 30 seconds
    ...options,
  })
}

export function useCreateConversation(
  options?: UseMutationOptions<Conversation, Error, CreateConversationRequest>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: conversationsAPI.create,
    onSuccess: (newConversation) => {
      // Optimistically update the cache
      queryClient.setQueryData<Conversation[]>(
        queryKeys.conversations,
        (old) => [newConversation, ...(old || [])]
      )
    },
    ...options,
  })
}

export function useDeleteConversation(
  options?: UseMutationOptions<void, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: conversationsAPI.delete,
    onSuccess: (_, deletedId) => {
      // Optimistically update the cache
      queryClient.setQueryData<Conversation[]>(
        queryKeys.conversations,
        (old) => old?.filter((conv) => conv.id !== deletedId) || []
      )
      // Invalidate messages for this conversation
      queryClient.removeQueries({
        queryKey: queryKeys.messages(deletedId),
      })
    },
    ...options,
  })
}

// ============================================================================
// Messages Hooks
// ============================================================================

export function useMessages(
  conversationId: string,
  options?: Omit<UseQueryOptions<Message[], Error>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: queryKeys.messages(conversationId),
    queryFn: () => messagesAPI.list(conversationId),
    enabled: !!conversationId, // Only fetch if conversationId exists
    staleTime: 10000, // Consider data fresh for 10 seconds
    ...options,
  })
}

export function useSendMessage(
  conversationId: string,
  options?: UseMutationOptions<Message[], Error, SendMessageRequest>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data) => messagesAPI.send(conversationId, data),
    onMutate: async (newMessage): Promise<{ previousMessages: Message[] | undefined }> => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({
        queryKey: queryKeys.messages(conversationId),
      })

      // Snapshot previous value
      const previousMessages = queryClient.getQueryData<Message[]>(
        queryKeys.messages(conversationId)
      )

      // Optimistically update with user message
      const optimisticUserMessage: Message = {
        id: `temp-${Date.now()}`,
        conversation_id: conversationId,
        role: 'user',
        content: newMessage.content,
        created_at: new Date().toISOString(),
      }

      queryClient.setQueryData<Message[]>(
        queryKeys.messages(conversationId),
        (old) => [...(old || []), optimisticUserMessage]
      )

      return { previousMessages }
    },
    onError: (_err, _newMessage, context) => {
      // Rollback on error
      if (context?.previousMessages) {
        queryClient.setQueryData(
          queryKeys.messages(conversationId),
          context.previousMessages
        )
      }
    },
    onSuccess: (newMessages) => {
      // Backend returns [userMessage, assistantMessage]
      // Replace optimistic message with real messages
      queryClient.setQueryData<Message[]>(
        queryKeys.messages(conversationId),
        (old) => {
          // Remove temporary optimistic messages
          const filtered = old?.filter((msg) => !msg.id.startsWith('temp-')) || []
          // Add the real messages from the backend
          return [...filtered, ...newMessages]
        }
      )
    },
    ...options,
  })
}

// ============================================================================
// Memories Hooks
// ============================================================================

export function useMemories(
  options?: Omit<UseQueryOptions<Memory[], Error>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: queryKeys.memories,
    queryFn: memoriesAPI.list,
    staleTime: 60000, // Consider data fresh for 1 minute
    ...options,
  })
}

export function useCreateMemory(
  options?: UseMutationOptions<Memory, Error, CreateMemoryRequest>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: memoriesAPI.create,
    onSuccess: (newMemory) => {
      queryClient.setQueryData<Memory[]>(
        queryKeys.memories,
        (old) => [newMemory, ...(old || [])]
      )
    },
    ...options,
  })
}

export function useDeleteMemory(
  options?: UseMutationOptions<void, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: memoriesAPI.delete,
    onSuccess: (_, deletedId) => {
      queryClient.setQueryData<Memory[]>(
        queryKeys.memories,
        (old) => old?.filter((mem) => mem.id !== deletedId) || []
      )
    },
    ...options,
  })
}

// ============================================================================
// Feedback Hooks
// ============================================================================

export function useCreateFeedback(
  options?: UseMutationOptions<Feedback, Error, CreateFeedbackRequest>
) {
  return useMutation({
    mutationFn: feedbackAPI.create,
    ...options,
  })
}
