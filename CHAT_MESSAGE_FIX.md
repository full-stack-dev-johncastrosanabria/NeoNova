# Chat Message Error Fix

## Issue
When sending a message in the chat, the app crashed with error:
```
Cannot read properties of undefined (reading 'getTime')
```

The error occurred in the `MessageBubble` component when trying to format the message timestamp.

## Root Cause
**Type mismatch between frontend and backend API response:**

The backend's `/conversations/{id}/messages` POST endpoint returns **an array of 2 messages**:
```json
[
  {
    "id": "...",
    "role": "user",
    "content": "Hello",
    "created_at": "2026-05-09T16:42:03.302130Z"
  },
  {
    "id": "...",
    "role": "assistant", 
    "content": "Hello! I'm NeoNova...",
    "created_at": "2026-05-09T16:42:03.305876Z"
  }
]
```

But the frontend was typed to expect a **single message object**:
```typescript
// ❌ Wrong type
send: (conversationId: string, data: SendMessageRequest) =>
  fetchAPI<Message>(`/conversations/${conversationId}/messages`, { ... })
```

This caused the `onSuccess` handler to receive an array but treat it as a single message, leading to:
1. The array being added to the messages list instead of its contents
2. When trying to render, `message.created_at` was undefined (because we were accessing array properties)
3. `formatRelativeTime(undefined)` tried to call `.getTime()` on undefined → crash

## Solution

### File 1: `/frontend/src/lib/api-client.ts`
Changed the return type from `Message` to `Message[]`:

```typescript
// ✅ Correct type
send: (conversationId: string, data: SendMessageRequest) =>
  fetchAPI<Message[]>(`/conversations/${conversationId}/messages`, { ... })
```

### File 2: `/frontend/src/hooks/use-api.ts`
Updated `useSendMessage` to handle array response:

**Before:**
```typescript
export function useSendMessage(
  conversationId: string,
  options?: UseMutationOptions<Message, Error, SendMessageRequest>
) {
  // ...
  onSuccess: (assistantMessage) => {
    queryClient.setQueryData<Message[]>(
      queryKeys.messages(conversationId),
      (old) => {
        const filtered = old?.filter((msg) => !msg.id.startsWith('temp-')) || []
        return [...filtered, assistantMessage]  // ❌ Adding array as single item
      }
    )
  }
}
```

**After:**
```typescript
export function useSendMessage(
  conversationId: string,
  options?: UseMutationOptions<Message[], Error, SendMessageRequest>
) {
  // ...
  onSuccess: (newMessages) => {
    // Backend returns [userMessage, assistantMessage]
    queryClient.setQueryData<Message[]>(
      queryKeys.messages(conversationId),
      (old) => {
        // Remove temporary optimistic messages
        const filtered = old?.filter((msg) => !msg.id.startsWith('temp-')) || []
        // Add the real messages from the backend
        return [...filtered, ...newMessages]  // ✅ Spread array contents
      }
    )
  }
}
```

## How It Works Now

1. User types "Hello" and clicks send
2. **Optimistic update**: Temporary user message added to UI immediately
3. **API call**: POST to `/conversations/{id}/messages`
4. **Backend response**: Returns array `[userMessage, assistantMessage]`
5. **onSuccess handler**:
   - Removes temporary optimistic message
   - Spreads the array contents into the messages list
   - Both real messages (user + assistant) are added
6. **UI renders**: Both messages display correctly with proper timestamps

## Testing
1. Open http://localhost:5174
2. Login with `demo@example.com` / `password123`
3. Create a new chat or select existing one
4. Type a message and send
5. Should see:
   - Your message appears immediately (optimistic)
   - Assistant response appears after ~100ms
   - Both messages have proper timestamps
   - No errors in console

## Related Files
- `/frontend/src/lib/api-client.ts` - API client with corrected return type
- `/frontend/src/hooks/use-api.ts` - TanStack Query hook with array handling
- `/frontend/src/pages/chat-page.tsx` - Chat UI that renders messages
- `/frontend/src/lib/utils.ts` - `formatRelativeTime` utility function

## Status
✅ **FIXED** - Chat messages now send and display correctly without errors
