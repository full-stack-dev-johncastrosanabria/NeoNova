import { Suspense, useState, useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
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
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { LanguageSelector } from '@/components/ui/language-selector'
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
    <div className="h-screen flex bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
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
  const { t } = useTranslation()
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
    <aside className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col shadow-lg animate-slide-in-left">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-gray-800 dark:to-gray-800">
        <div className="flex items-center justify-between mb-4 animate-fade-in-down">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-600 to-secondary-600 flex items-center justify-center shadow-lg hover:scale-110 transition-transform duration-300 cursor-pointer">
              <Sparkles className="w-5 h-5 text-white animate-pulse-slow" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900 dark:text-white">NeoNova AI</h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">{t('chat.conversations')}</p>
            </div>
          </div>
          <div className="flex gap-1">
            <LanguageSelector />
            <ThemeToggle />
          </div>
        </div>
        
        <Button
          onClick={handleCreateConversation}
          variant="primary"
          size="md"
          className="w-full group relative overflow-hidden"
          isLoading={createConversation.isPending}
        >
          <MessageSquarePlus className="w-4 h-4 group-hover:rotate-90 transition-transform duration-300" />
          <span>{t('chat.newChat')}</span>
          <div className="absolute inset-0 bg-gradient-to-r from-primary-700 to-secondary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
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
            <AlertCircle className="w-8 h-8 text-red-500 dark:text-red-400 mx-auto mb-2" />
            <p className="text-sm text-red-600 dark:text-red-400">{t('chat.failedToLoad')} conversations</p>
          </div>
        )}

        {conversations && conversations.length === 0 && (
          <div className="p-4 text-center text-gray-500 dark:text-gray-400">
            <p className="text-sm">{t('chat.noConversations')}</p>
            <p className="text-xs mt-1">{t('chat.createToStart')}</p>
          </div>
        )}

        <div className="space-y-1">
          {conversations?.map((conv, index) => (
            <div
              key={conv.id}
              className={cn(
                'group flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-all duration-300 animate-fade-in-up',
                selectedId === conv.id
                  ? 'bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 border border-primary-200 dark:border-primary-700 shadow-sm scale-[1.02]'
                  : 'hover:bg-gray-50 dark:hover:bg-gray-700 border border-transparent hover:scale-[1.01]'
              )}
              style={{ animationDelay: `${index * 0.05}s` }}
              onClick={() => setSelectedId(conv.id)}
            >
              <div className="flex-1 min-w-0">
                <p className={cn(
                  'text-sm font-medium truncate transition-colors',
                  selectedId === conv.id ? 'text-primary-900 dark:text-primary-300' : 'text-gray-900 dark:text-gray-100'
                )}>
                  {conv.title}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  {formatRelativeTime(conv.updated_at)}
                </p>
              </div>
              
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleDeleteConversation(conv.id)
                }}
                className="opacity-0 group-hover:opacity-100 p-1.5 rounded-md hover:bg-red-50 text-gray-400 hover:text-red-600 transition-all duration-200 hover:scale-110 hover:rotate-12"
                disabled={deleteConversation.isPending}
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
        <Button
          onClick={logout}
          variant="ghost"
          size="md"
          className="w-full justify-start text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200 group"
        >
          <LogOut className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          {t('auth.logout')}
        </Button>
      </div>
    </aside>
  )
}

// ============================================================================
// Chat Area Component
// ============================================================================

function ChatArea() {
  const { t } = useTranslation()
  const { data: conversations } = useConversations()
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    if (conversations && conversations.length > 0 && !selectedId) {
      setSelectedId(conversations[0].id)
    }
  }, [conversations, selectedId])

  if (!selectedId) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gradient-to-br from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
        <div className="text-center animate-fade-in">
          <Sparkles className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4 animate-float" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 animate-fade-in-up">
            {t('chat.welcomeTitle')}
          </h3>
          <p className="text-gray-500 dark:text-gray-400 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            {t('chat.welcomeMessage')}
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
  const { t } = useTranslation()
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
          <div className="flex items-center justify-center gap-2 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
            <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
            <p className="text-sm text-red-600 dark:text-red-400">{t('chat.failedToLoad')} messages</p>
          </div>
        )}

        {messages && messages.length === 0 && (
          <div className="text-center py-12">
            <Bot className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
            <p className="text-gray-500 dark:text-gray-400">{t('chat.noMessages')}</p>
          </div>
        )}

        {messages?.map((message, index) => (
          <MessageBubble key={message.id} message={message} index={index} />
        ))}

        {sendMessage.isPending && (
          <div className="flex items-start gap-3 animate-fade-in-up">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-600 to-secondary-600 flex items-center justify-center flex-shrink-0 animate-pulse-glow">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <Card className="flex-1 p-4 border-primary-200 dark:border-primary-700 bg-primary-50/50 dark:bg-primary-900/20 animate-pulse">
              <div className="flex items-center gap-2">
                <LoadingSpinner size="sm" />
                <span className="text-sm text-gray-600 dark:text-gray-400 animate-typing">{t('chat.thinking')}</span>
              </div>
            </Card>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 shadow-lg">
        <form onSubmit={handleSend} className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={t('chat.typeMessage')}
              disabled={sendMessage.isPending}
              className="flex-1 transition-all duration-200 focus:scale-[1.01] focus:shadow-lg dark:bg-gray-700 dark:text-white dark:border-gray-600"
              autoFocus
            />
            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={!input.trim() || sendMessage.isPending}
              isLoading={sendMessage.isPending}
              className="group relative overflow-hidden hover:scale-105 transition-transform"
            >
              <Send className="w-4 h-4 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
              <div className="absolute inset-0 bg-gradient-to-r from-primary-700 to-secondary-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
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
  index?: number
}

function MessageBubble({ message, index = 0 }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div 
      className={cn(
        'flex items-start gap-3 animate-fade-in-up',
        isUser && 'flex-row-reverse'
      )}
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      {/* Avatar */}
      <div className={cn(
        'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 transition-transform duration-300 hover:scale-110',
        isUser 
          ? 'bg-gradient-to-br from-gray-200 to-gray-300 shadow-sm' 
          : 'bg-gradient-to-br from-primary-600 to-secondary-600 shadow-lg animate-pulse-slow'
      )}>
        {isUser ? (
          <User className="w-5 h-5 text-gray-600" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <Card className={cn(
        'flex-1 p-4 transition-all duration-300 hover:shadow-lg',
        isUser 
          ? 'bg-gradient-to-br from-primary-600 to-primary-700 text-white border-primary-600 dark:border-primary-500 hover:scale-[1.01]' 
          : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-primary-200 dark:hover:border-primary-700 hover:scale-[1.01]'
      )}>
        <p className={cn(
          'text-sm whitespace-pre-wrap leading-relaxed',
          isUser ? 'text-white' : 'text-gray-900 dark:text-gray-100'
        )}>
          {message.content}
        </p>
        <p className={cn(
          'text-xs mt-2 flex items-center gap-1',
          isUser ? 'text-primary-100' : 'text-gray-400 dark:text-gray-500'
        )}>
          <span>{formatRelativeTime(message.created_at)}</span>
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
    <aside className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse mb-4" />
        <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse" />
      </div>
      <div className="flex-1 p-2 space-y-2">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-100 dark:bg-gray-700 rounded-lg animate-pulse" />
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
