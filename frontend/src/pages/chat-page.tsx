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
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { LanguageSelector } from '@/components/ui/language-selector'
import { AnimatedBackground } from '@/components/ui/animated-background'
import { 
  MessageSquarePlus, 
  Send, 
  Trash2, 
  LogOut, 
  Sparkles,
  User,
  Bot,
  AlertCircle,
  Paperclip,
  Code,
  Mail,
  Lightbulb,
  FileText,
} from 'lucide-react'
import { cn, formatRelativeTime } from '@/lib/utils'
import type { Message } from '@/lib/api-client'

export function ChatPage() {
  return (
    <div className="h-screen flex bg-gray-950 text-gray-100">
      <AnimatedBackground />
      
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
    if (conversations?.length && !selectedId) {
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

  // Group conversations by date
  const groupedConversations = conversations?.reduce((acc, conv) => {
    const date = new Date(conv.created_at)
    const now = new Date()
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))
    
    let group = 'Older'
    if (diffDays === 0) group = 'Today'
    else if (diffDays === 1) group = 'Yesterday'
    else if (diffDays <= 7) group = 'Previous 7 Days'
    
    if (!acc[group]) acc[group] = []
    acc[group].push(conv)
    return acc
  }, {} as Record<string, typeof conversations>)

  return (
    <aside className="w-64 bg-gray-900/50 backdrop-blur-xl border-r border-gray-800/50 flex flex-col">
      {/* Header */}
      <div className="p-3 border-b border-gray-800/30">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
              <Sparkles className="w-3.5 h-3.5 text-white" />
            </div>
            <span className="font-semibold text-sm text-gray-100">NeoNova AI</span>
          </div>
          <div className="flex gap-0.5">
            <LanguageSelector />
            <ThemeToggle />
          </div>
        </div>
        
        <Button
          onClick={handleCreateConversation}
          variant="primary"
          size="sm"
          className="w-full justify-center gap-2 bg-white/5 hover:bg-white/10 text-gray-100 border border-white/10 hover:border-white/20 transition-all text-sm py-2"
          isLoading={createConversation.isPending}
        >
          <MessageSquarePlus className="w-4 h-4" />
          <span>{t('chat.newChat')}</span>
        </Button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto px-2 py-2 space-y-4">
        {isLoading && (
          <div className="flex justify-center py-8">
            <LoadingSpinner size="sm" />
          </div>
        )}

        {error && (
          <div className="px-2 py-2 text-center">
            <p className="text-xs text-red-400">{t('chat.failedToLoad')}</p>
          </div>
        )}

        {conversations?.length === 0 && (
          <div className="px-2 py-8 text-center">
            <p className="text-xs text-gray-500">{t('chat.noConversations')}</p>
            <p className="text-xs text-gray-600 mt-1">{t('chat.createToStart')}</p>
          </div>
        )}

        {groupedConversations && Object.entries(groupedConversations).map(([group, convs]) => (
          <div key={group} className="space-y-0.5">
            <div className="px-2 py-1">
              <h3 className="text-[11px] font-medium text-gray-500 uppercase tracking-wider">{group}</h3>
            </div>
            
            {convs.map((conv) => (
              <button
                key={conv.id}
                className={cn(
                  'group relative flex items-center gap-2 px-2 py-1.5 rounded-md cursor-pointer transition-all w-full text-left',
                  selectedId === conv.id
                    ? 'bg-white/10 text-gray-100'
                    : 'text-gray-400 hover:bg-white/5 hover:text-gray-200'
                )}
                onClick={() => setSelectedId(conv.id)}
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm truncate">
                    {conv.title}
                  </p>
                </div>
                
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDeleteConversation(conv.id)
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-white/10 text-gray-500 hover:text-red-400 transition-all"
                  disabled={deleteConversation.isPending}
                  aria-label="Delete conversation"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </button>
            ))}
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-2 border-t border-gray-800/30">
        <Button
          onClick={logout}
          variant="ghost"
          size="sm"
          className="w-full justify-start gap-2 text-gray-400 hover:text-gray-200 hover:bg-white/5 text-sm py-2"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>{t('auth.logout')}</span>
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
    if (conversations?.length && !selectedId) {
      setSelectedId(conversations[0].id)
    }
  }, [conversations, selectedId])

  if (!selectedId) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="max-w-2xl mx-auto px-6 text-center">
          {/* Welcome Section */}
          <div className="mb-12 animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center mx-auto mb-6 animate-float">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-semibold text-gray-100 mb-3">
              {t('chat.welcomeTitle')}
            </h1>
            <p className="text-gray-400 text-lg">
              {t('chat.welcomeMessage')}
            </p>
          </div>

          {/* Suggested Prompts */}
          <div className="grid grid-cols-2 gap-3 max-w-xl mx-auto">
            {[
              { icon: Mail, text: t('chat.suggestedPrompts.writeEmail'), color: 'from-blue-500 to-cyan-500' },
              { icon: Code, text: t('chat.suggestedPrompts.generateCode'), color: 'from-purple-500 to-pink-500' },
              { icon: FileText, text: t('chat.suggestedPrompts.summarizeText'), color: 'from-green-500 to-emerald-500' },
              { icon: Lightbulb, text: t('chat.suggestedPrompts.brainstormIdeas'), color: 'from-orange-500 to-yellow-500' },
            ].map((prompt) => (
              <button
                key={prompt.text}
                className="group p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 transition-all text-left animate-fade-in-up"
                style={{ animationDelay: `${[Mail, Code, FileText, Lightbulb].indexOf(prompt.icon) * 0.1}s` }}
              >
                <div className={cn(
                  'w-10 h-10 rounded-lg bg-gradient-to-br flex items-center justify-center mb-3 group-hover:scale-110 transition-transform',
                  prompt.color
                )}>
                  <prompt.icon className="w-5 h-5 text-white" />
                </div>
                <p className="text-sm text-gray-300 group-hover:text-gray-100 transition-colors">
                  {prompt.text}
                </p>
              </button>
            ))}
          </div>
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
  readonly conversationId: string
}

function ChatMessages({ conversationId }: ChatMessagesProps) {
  const { t } = useTranslation()
  const { data: messages, isLoading, error } = useMessages(conversationId)
  const sendMessage = useSendMessage(conversationId)
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || sendMessage.isPending) return

    const content = input.trim()
    setInput('')
    await sendMessage.mutateAsync({ content })
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend(e)
    }
  }

  return (
    <div className="flex-1 flex flex-col relative">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-6 py-8 space-y-6">
          {isLoading && (
            <div className="flex justify-center py-12">
              <LoadingSpinner />
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center gap-2 p-4 rounded-xl bg-red-500/10 border border-red-500/20">
              <AlertCircle className="w-5 h-5 text-red-400" />
              <p className="text-sm text-red-400">{t('chat.failedToLoad')} messages</p>
            </div>
          )}

          {messages?.length === 0 && !isLoading && (
            <div className="text-center py-16">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500/20 to-secondary-500/20 flex items-center justify-center mx-auto mb-4">
                <Bot className="w-6 h-6 text-gray-400" />
              </div>
              <p className="text-gray-400">{t('chat.noMessages')}</p>
            </div>
          )}

          {messages?.map((message, index) => (
            <MessageBubble key={message.id} message={message} index={index} />
          ))}

          {sendMessage.isPending && (
            <div className="flex items-start gap-4 animate-fade-in-up">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="flex-1 p-4 rounded-2xl bg-white/5 border border-white/10">
                <div className="flex items-center gap-2">
                  <LoadingSpinner size="sm" />
                  <span className="text-sm text-gray-400">{t('chat.thinking')}</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area - Floating */}
      <div className="sticky bottom-0 border-t border-white/5 bg-gray-950/80 backdrop-blur-xl">
        <div className="max-w-3xl mx-auto px-6 py-4">
          <form onSubmit={handleSend}>
            <div className="relative flex items-end gap-2 p-3 rounded-2xl bg-white/5 border border-white/10 focus-within:border-white/20 focus-within:bg-white/[0.07] transition-all">
              <button
                type="button"
                className="p-2 rounded-lg hover:bg-white/10 text-gray-400 hover:text-gray-300 transition-all flex-shrink-0"
                aria-label="Attach file"
              >
                <Paperclip className="w-5 h-5" />
              </button>
              
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={t('chat.typeMessage')}
                disabled={sendMessage.isPending}
                rows={1}
                className="flex-1 bg-transparent text-gray-100 placeholder-gray-500 resize-none outline-none text-[15px] leading-6 max-h-[200px]"
              />
              
              <button
                type="submit"
                disabled={!input.trim() || sendMessage.isPending}
                className={cn(
                  'p-2 rounded-lg transition-all flex-shrink-0',
                  input.trim() && !sendMessage.isPending
                    ? 'bg-gradient-to-br from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white shadow-lg hover:shadow-xl hover:scale-105'
                    : 'bg-white/5 text-gray-600 cursor-not-allowed'
                )}
                aria-label="Send message"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// Message Bubble Component
// ============================================================================

interface MessageBubbleProps {
  readonly message: Message
  readonly index?: number
}

function MessageBubble({ message, index = 0 }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div 
      className={cn(
        'flex items-start gap-4 animate-fade-in-up',
        isUser && 'flex-row-reverse'
      )}
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      {/* Avatar */}
      <div className={cn(
        'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
        isUser 
          ? 'bg-gradient-to-br from-gray-700 to-gray-800' 
          : 'bg-gradient-to-br from-primary-500 to-secondary-500'
      )}>
        {isUser ? (
          <User className="w-4 h-4 text-gray-300" />
        ) : (
          <Bot className="w-4 h-4 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={cn(
        'flex-1 max-w-[85%]',
        isUser && 'flex flex-col items-end'
      )}>
        <div className={cn(
          'inline-block p-4 rounded-2xl transition-all',
          isUser 
            ? 'bg-gradient-to-br from-primary-500 to-secondary-500 text-white rounded-tr-sm' 
            : 'bg-white/5 border border-white/10 text-gray-100 rounded-tl-sm'
        )}>
          <p className="text-[15px] whitespace-pre-wrap leading-7">
            {message.content}
          </p>
        </div>
        <p className={cn(
          'text-xs mt-1.5 px-1',
          isUser ? 'text-gray-500' : 'text-gray-600'
        )}>
          {formatRelativeTime(message.created_at)}
        </p>
      </div>
    </div>
  )
}

// ============================================================================
// Skeleton Components
// ============================================================================

function SidebarSkeleton() {
  return (
    <aside className="w-64 bg-gray-900/50 backdrop-blur-xl border-r border-gray-800/50 flex flex-col">
      <div className="p-3 border-b border-gray-800/30">
        <div className="h-10 bg-white/5 rounded-lg animate-pulse mb-3" />
        <div className="h-9 bg-white/5 rounded-lg animate-pulse" />
      </div>
      <div className="flex-1 p-2 space-y-2">
        {Array.from({ length: 5 }, (_, i) => (
          <div key={`skeleton-item-${i}`} className="h-10 bg-white/5 rounded-md animate-pulse" />
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
