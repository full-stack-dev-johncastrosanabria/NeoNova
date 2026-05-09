import { createFileRoute, Navigate } from '@tanstack/react-router'
import { getAuthToken } from '@/lib/api-client'

export const Route = createFileRoute('/')({
  component: IndexComponent,
})

function IndexComponent() {
  const token = getAuthToken()
  return <Navigate to={token ? '/chat' : '/login'} replace />
}
