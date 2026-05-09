import { createFileRoute, Navigate } from '@tanstack/react-router'
import { getAuthToken } from '@/lib/api-client'
import { ChatPage } from '@/pages/chat-page'

export const Route = createFileRoute('/chat')({
  component: ChatRoute,
})

function ChatRoute() {
  const token = getAuthToken()
  
  if (!token) {
    return <Navigate to="/login" replace />
  }
  
  return <ChatPage />
}
