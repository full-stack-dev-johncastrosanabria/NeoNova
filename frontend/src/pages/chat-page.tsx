import { Suspense, useState, useEffect, useRef } from 'react'
import { 
  useConversations, 
  useCreateConversation, 
  useDeleteConversation,
  useMessages,
  useSendMessage,
  useLogout,
} from '@/hooks/use-api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { 
  MessageSquarePlus, 
  Send, 
  Trash2, 
  LogOut, 
  Sparkles,
  User,
  Bot,
  AlertCircle,
} from 'lucide-react'
import { cn, formatRelativeTime } from '@/lib/utils'
import type { Message } from '@/lib/api-client'

export function ChatPage() {
  return (
    <div className="h-screen flex bg-gray-50">
      {/* Sidebar */}
      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />
      </Suspense>

      {/* Main Chat Area */}
      <Suspense fallback={<ChatAreaSkeleton />}>
        <ChatArea />
      </Suspense>
    </div>
  )
}

// ============================================================================
// Sidebar Component
// ============================================================================

function Sidebar() {
  const { data: conversations, isLoading, error } = useConversations()
  const createConversation = useCreateConversation()
  const deleteConversation = useDeleteConversation()
  const logout = useLogout()
  const [selectedId, setSelectedId] = useState<string | null>(null)

  // Auto-select first conversation
  useEffect(() => {
    if (conversations && conversations.length > 0 && !selectedId) {
      setSelectedId(conversations[0].id)
    }
  }, [conversations, selectedId])

  const handleCreateConversation = async () => {
    const title = `Chat ${new Date().toLocaleString()}`
    const result = await createConversation.mutateAsync({ title })
    setSelectedId(result.id)
  }

  const handleDeleteConversation = async (id: string) => {
    await deleteConversation.mutateAsync(id)
    if (selectedId === id) {
      setSelectedId(conversations?.[0]?.id || null)
    }
  }

  return (
    <aside className="w-80 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-600 to-secondary-600 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="font-semibold text-gray-900">NeoNova AI</h2>
            <p className="text-xs text-gray-500">Your conversations</p>
          </div>
        </div>
        
        <Button
          onClick={handleCreateConversation}
          variant="primary"
          size="md"
          className="w-full"
          isLoading={createConversation.isPending}
        >
          <MessageSquarePlus className="w-4 h-4" />
          New Chat
        </Button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto p-2">
        {isLoading && (
          <div className="flex justify-center py-8">
            <LoadingSpinner />
          </div>
        )}

        {error && (
          <div className="p-4 text-center">
            <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-2" />
            <p className="text-sm text-red-600">Failed to load conversations</p>
          </div>
        )}

        {conversations && conversations.length === 0 && (
          <div className="p-4 text-center text-gray-500">
            <p className="text-sm">No conversations yet</p>
            <p className="text-xs mt-1">Create one to get started</p>
          </div>
        )}

        <div className="space-y-1">
          {conversations?.map((conv) => (
            <div
              key={conv.id}
              className={cn(
                'group flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-all',
                selectedId === conv.id
                  ? 'bg-primary-50 border border-primary-200'
                  : 'hover:bg-gray-50 border border-transparent'
              )}
              onClick={() => setSelectedId(conv.id)}
            >
              <div className="flex-1 min-w-0">
                <p className={cn(
                  'text-sm font-medium truncate',
                  selectedId === conv.id ? 'text-primary-900' : 'text-gray-900'
                )}>
                  {conv.title}
                </p>
                <p className="text-xs text-gray-500">
                  {formatRelativeTime(conv.updated_at)}
                </p>
              </div>
              
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleDeleteConversation(conv.id)
                }}
                className="opacity-0 group-hover:opacity-100 p-1.5 rounded-md hover:bg-red-50 text-gray-400 hover:text-red-600 transition-all"
                disabled={deleteConversation.isPending}
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <Button
          onClick={logout}
          variant="ghost"
          size="md"
          className="w-full justify-start text-gray-700"
        >
          <LogOut className="w-4 h-4" />
          Sign out
        </Button>
      </div>
    </aside>
  )
}

// ============================================================================
// Chat Area Component
// ============================================================================

function ChatArea() {
  const { data: conversations } = useConversations()
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    if (conversations && conversations.length > 0 && !selectedId) {
      setSelectedId(conversations[0].id)
    }
  }, [conversations, selectedId])

  if (!selectedId) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <Sparkles className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Welcome to NeoNova AI
          </h3>
          <p className="text-gray-500">
            Create a new conversation to get started
          </p>
        </div>
      </div>
    )
  }

  return (
    <Suspense fallback={<ChatAreaSkeleton />}>
      <ChatMessages conversationId={selectedId} />
    </Suspense>
  )
}

// ============================================================================
// Chat Messages Component
// ============================================================================

interface ChatMessagesProps {
  conversationId: string
}

function ChatMessages({ conversationId }: ChatMessagesProps) {
  const { data: messages, isLoading, error } = useMessages(conversationId)
  const sendMessage = useSendMessage(conversationId)
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || sendMessage.isPending) return

    const content = input.trim()
    setInput('')
    await sendMessage.mutateAsync({ content })
  }

  return (
    <div className="flex-1 flex flex-col">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {isLoading && (
          <div className="flex justify-center py-8">
            <LoadingSpinner />
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center gap-2 p-4 rounded-lg bg-red-50 border border-red-200">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="text-sm text-red-600">Failed to load messages</p>
          </div>
        )}

        {messages && messages.length === 0 && (
          <div className="text-center py-12">
            <Bot className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">No messages yet. Start the conversation!</p>
          </div>
        )}

        {messages?.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {sendMessage.isPending && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-600 to-secondary-600 flex items-center justify-center flex-shrink-0">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <Card className="flex-1 p-4 border-primary-200 bg-primary-50/50">
              <div className="flex items-center gap-2">
                <LoadingSpinner size="sm" />
                <span className="text-sm text-gray-600">Thinking...</span>
              </div>
            </Card>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4">
        <form onSubmit={handleSend} className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={sendMessage.isPending}
              className="flex-1"
              autoFocus
            />
            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={!input.trim() || sendMessage.isPending}
              isLoading={sendMessage.isPending}
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

// ============================================================================
// Message Bubble Component
// ============================================================================

interface MessageBubbleProps {
  message: Message
}

function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div className={cn('flex items-start gap-3', isUser && 'flex-row-reverse')}>
      {/* Avatar */}
      <div className={cn(
        'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
        isUser 
          ? 'bg-gray-200' 
          : 'bg-gradient-to-br from-primary-600 to-secondary-600'
      )}>
        {isUser ? (
          <User className="w-5 h-5 text-gray-600" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <Card className={cn(
        'flex-1 p-4 animate-slide-up',
        isUser 
          ? 'bg-primary-600 text-white border-primary-600' 
          : 'bg-white border-gray-200'
      )}>
        <p className={cn(
          'text-sm whitespace-pre-wrap',
          isUser ? 'text-white' : 'text-gray-900'
        )}>
          {message.content}
        </p>
        <p className={cn(
          'text-xs mt-2',
          isUser ? 'text-primary-100' : 'text-gray-400'
        )}>
          {formatRelativeTime(message.created_at)}
        </p>
      </Card>
    </div>
  )
}

// ============================================================================
// Skeleton Components
// ============================================================================

function SidebarSkeleton() {
  return (
    <aside className="w-80 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="h-10 bg-gray-200 rounded-lg animate-pulse mb-4" />
        <div className="h-10 bg-gray-200 rounded-lg animate-pulse" />
      </div>
      <div className="flex-1 p-2 space-y-2">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-100 rounded-lg animate-pulse" />
        ))}
      </div>
    </aside>
  )
}

function ChatAreaSkeleton() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <LoadingSpinner size="lg" />
    </div>
  )
}
