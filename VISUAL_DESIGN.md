# Conversation Management - Visual Guide

## Desktop View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌──────────────────┐  ┌────────────────────────────────────────────────┐  │
│  │  SIDEBAR         │  │           CHAT APPLICATION                     │  │
│  │  (Dark Theme)    │  │                                                │  │
│  │                  │  │  Multi-turn conversation with AI              │  │
│  ├──────────────────┤  ├────────────────────────────────────────────────┤  │
│  │                  │  │                                                │  │
│  │  ┌────────────┐  │  │  ┌──────────────────────────────────────┐    │  │
│  │  │ + New Chat │  │  │  │  👤 User                             │    │  │
│  │  └────────────┘  │  │  │  What is machine learning?           │    │  │
│  │                  │  │  └──────────────────────────────────────┘    │  │
│  │  Conversations:  │  │                                                │  │
│  │                  │  │  ┌──────────────────────────────────────┐    │  │
│  │  ┌────────────┐  │  │  │  🤖 AI                               │    │  │
│  │  │ • What is  │🗑│  │  │  Machine learning is a subset of     │    │  │
│  │  │ machine... │  │  │  │  artificial intelligence that...     │    │  │
│  │  │ 2 mins ago │  │  │  └──────────────────────────────────────┘    │  │
│  │  └────────────┘  │  │                                                │  │
│  │   ↑ Active      │  │  ┌──────────────────────────────────────┐    │  │
│  │                  │  │  │  👤 User                             │    │  │
│  │  ┌────────────┐  │  │  │  Tell me more about neural networks  │    │  │
│  │  │ ○ Explain  │🗑│  │  └──────────────────────────────────────┘    │  │
│  │  │ Python...  │  │  │                                                │  │
│  │  │ 5 mins ago │  │  │  ┌──────────────────────────────────────┐    │  │
│  │  └────────────┘  │  │  │  🤖 AI                               │    │  │
│  │                  │  │  │  Neural networks are...              │    │  │
│  │  ┌────────────┐  │  │  │  • • •                               │    │  │
│  │  │ ○ CSV data │🗑│  │  └──────────────────────────────────────┘    │  │
│  │  │ analysis   │  │  │                                                │  │
│  │  │ 1 hour ago │  │  │                                                │  │
│  │  └────────────┘  │  │                                                │  │
│  │                  │  ├────────────────────────────────────────────────┤  │
│  │                  │  │  ┌────────────────────────────────────────┐  │  │
│  │                  │  │  │ Type your message...            [📎][📊]│  │  │
│  │                  │  │  └────────────────────────────────────────┘  │  │
│  │                  │  │                                   [Send →]    │  │
│  └──────────────────┘  └────────────────────────────────────────────────┘  │
│   256px wide              Flexible width (max 1280px)                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Mobile View (< 768px)

### Sidebar Closed (Default)
```
┌────────────────────────┐
│  ☰  CHAT APPLICATION   │
│                        │
├────────────────────────┤
│                        │
│  👤 User               │
│  Hello!                │
│                        │
│  🤖 AI                 │
│  Hi! How can I help?   │
│                        │
│                        │
│                        │
├────────────────────────┤
│ Type message...  [Send]│
└────────────────────────┘
```

### Sidebar Open
```
┌────────────────────────┐
│ ┌──────────────┐       │
│ │  SIDEBAR     │ ████  │ ← Dark overlay
│ │              │ ████  │
│ │ + New Chat   │ ████  │
│ │              │ ████  │
│ │ • Conv 1  🗑 │ ████  │
│ │ • Conv 2  🗑 │ ████  │
│ │ • Conv 3  🗑 │ ████  │
│ │              │ ████  │
│ └──────────────┘ ████  │
│                  ████  │
└────────────────────────┘
       ↑
   Click outside
   to close
```

## Sidebar Component Details

### Header Section
```
┌────────────────────────┐
│  ┌──────────────────┐  │
│  │                  │  │
│  │   + New Chat     │  │ ← Button (hover: lighter)
│  │                  │  │
│  └──────────────────┘  │
└────────────────────────┘
```

### Conversation Item (Normal)
```
┌────────────────────────┐
│ ○ Conversation Title   │
│   3 minutes ago        │ ← Hover: Shows delete
└────────────────────────┘
```

### Conversation Item (Active)
```
┌────────────────────────┐
│ • What is machine...   │ ← Highlighted background
│   2 minutes ago        │   Current conversation
└────────────────────────┘
```

### Conversation Item (Hover)
```
┌────────────────────────┐
│ ○ Explain Python    🗑 │ ← Delete button visible
│   5 minutes ago        │   Click to delete
└────────────────────────┘
```

### Footer Section
```
┌────────────────────────┐
│  💬 Multi-Modal Chat   │
│  Image • CSV • Text    │
└────────────────────────┘
```

## Color Scheme

### Sidebar (Dark Theme)
```
Background: #1F2937 (gray-900)
Text: #FFFFFF (white)
Hover: #374151 (gray-800)
Active: #374151 (gray-800)
Border: #4B5563 (gray-700)
```

### Main Chat (Light Theme)
```
Background: #FFFFFF (white)
Header: #3B82F6 (blue-600)
User Message: #DBEAFE (blue-100)
AI Message: #F3F4F6 (gray-100)
Text: #1F2937 (gray-900)
```

## Interaction States

### Conversation List Item States

**Normal:**
```
○ Title
  timestamp
```

**Hover:**
```
○ Title                🗑
  timestamp
  ↑ Slightly lighter background
```

**Active:**
```
• Title
  timestamp
  ↑ Highlighted with darker background
```

**Deleting (with confirmation):**
```
┌─────────────────────────┐
│ Delete this             │
│ conversation?           │
│                         │
│ [Cancel]  [Delete]      │
└─────────────────────────┘
```

## Responsive Breakpoints

```
< 768px  → Mobile (sidebar hidden by default)
≥ 768px  → Desktop (sidebar always visible)
```

## UI Flow Examples

### Example 1: First Time User

**Step 1: Initial Load**
```
┌──────────┬─────────────────┐
│          │  Start a        │
│ + New    │  conversation!  │
│ Chat     │                 │
│          │  Upload CSV or  │
│ (Empty)  │  chat normally  │
└──────────┴─────────────────┘
```

**Step 2: After Sending First Message**
```
┌──────────┬─────────────────┐
│ + New    │  👤 What is AI? │
│ Chat     │                 │
│          │  🤖 AI is...    │
│ • What   │     ...         │
│   is AI? │                 │
└──────────┴─────────────────┘
         ↑
    Auto-generated title
```

### Example 2: Power User with Multiple Conversations

```
┌──────────────┬──────────────────┐
│ + New Chat   │  Active Conv:    │
│              │                  │
│ • ML basics  │  👤 Question     │
│   now        │                  │
│              │  🤖 Answer       │
│ ○ Python     │                  │
│   tutorial   │  👤 Follow-up    │
│   2 hrs ago  │                  │
│              │  🤖 Response     │
│ ○ CSV sales  │                  │
│   data       │  [Plot showing]  │
│   1 day ago  │                  │
│              │                  │
│ ○ Image      │                  │
│   analysis   │                  │
│   2 days ago │                  │
└──────────────┴──────────────────┘
```

## Animation Effects

### Sidebar Slide (Mobile)
```
Closed → Open
[-]  →  [-]  →  [-]  →  [━]
        ━        ━━      ━━━
        
Duration: 300ms
Easing: ease-in-out
```

### Loading State
```
🤖 AI
   ● ● ●  → Bounce animation
   ↑ ↑ ↑
   Delay: 0ms, 100ms, 200ms
```

### Delete Confirmation
```
[Hover]  →  [Show] 🗑  →  [Click]  →  [Confirm?]
```

## Accessibility Features

### Keyboard Navigation
```
Tab       → Move between conversations
Enter     → Select conversation
Delete    → Delete (with confirmation)
Esc       → Close sidebar (mobile)
Ctrl+N    → New chat (future)
```

### Screen Reader Support
```
<button aria-label="New Chat">
<button aria-label="Delete conversation: {title}">
<nav aria-label="Conversations">
```

## Edge Cases Handled

### Long Titles
```
○ This is a very long conversation title that needs to be truncated...
  2 minutes ago
  ↑ Truncated at 50 chars with "..."
```

### No Conversations
```
┌──────────────┐
│ + New Chat   │
│              │
│ No convers-  │
│ ations yet   │
│              │
│ Click "New   │
│ Chat" to     │
│ start        │
└──────────────┘
```

### Many Conversations
```
┌──────────────┐
│ + New Chat   │
│ ↕ Scroll     │ ← Scrollable area
│ • Conv 1     │
│ ○ Conv 2     │
│ ○ Conv 3     │
│ ○ ...        │
│ ○ Conv 50    │
└──────────────┘
```

## Summary

The UI provides:
✅ Clean, modern design
✅ Intuitive interactions
✅ Smooth animations
✅ Responsive layout
✅ Accessible controls
✅ Professional appearance

The visual design makes it feel like a production-ready application! 🎨
