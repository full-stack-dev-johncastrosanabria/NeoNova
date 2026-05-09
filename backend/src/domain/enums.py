"""Domain enums for NeoNova AI Assistant."""

from enum import Enum


class MessageRole(Enum):
    """Role of a message in a conversation."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MemoryType(Enum):
    """Type of a memory entry."""

    PREFERENCE = "preference"
    FACT = "fact"
    INSTRUCTION = "instruction"
    CORRECTION = "correction"
    PROJECT_CONTEXT = "project_context"


class MemoryImportance(Enum):
    """Importance level of a memory entry."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
