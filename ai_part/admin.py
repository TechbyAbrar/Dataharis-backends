from django.contrib import admin
from .models import (
    AI_User,
    AI_ChatSession,
    AI_ChatMessage,
    AI_Document,
    AI_DocumentChunk,
)


@admin.register(AI_User)
class AIUserAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    ordering = ("-created_at",)


@admin.register(AI_ChatSession)
class AIChatSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "last_updated")
    search_fields = ("title", "user__email")
    list_filter = ("created_at",)
    ordering = ("-last_updated",)


@admin.register(AI_ChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ("session", "timestamp")
    search_fields = ("query_text", "response_text", "session__title")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)


@admin.register(AI_Document)
class AIDocumentAdmin(admin.ModelAdmin):
    list_display = ("document_name", "admin", "upload_on", "processed", "is_public", "page_count")
    search_fields = ("document_name", "admin__email", "author", "category")
    list_filter = ("processed", "is_public", "upload_on")
    ordering = ("-upload_on",)


@admin.register(AI_DocumentChunk)
class AIDocumentChunkAdmin(admin.ModelAdmin):
    list_display = ("document", "page_number", "chunk_index", "embedding_id", "relevance_score")
    search_fields = ("chunk_text", "document__document_name", "embedding_id")
    list_filter = ("document__upload_on",)
    ordering = ("document", "chunk_index")
