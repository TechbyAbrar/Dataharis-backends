from django.db import models
import uuid

class AI_User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AI_ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="New Consultation")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(AI_User, related_name="chat_sessions", to_field="email", db_column="email", on_delete=models.CASCADE)

class AI_ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AI_ChatSession, related_name="messages", on_delete=models.CASCADE)
    query_text = models.TextField()
    response_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    references = models.TextField(blank=True, null=True)

class AI_Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(AI_User, related_name="documents", to_field="email", db_column="admin_email", on_delete=models.CASCADE)
    document_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024)
    upload_on = models.DateTimeField(auto_now_add=True, db_index=True)
    processed = models.BooleanField(default=False)
    page_count = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

class AI_DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(AI_Document, related_name="chunks", on_delete=models.CASCADE)
    chunk_text = models.TextField()
    page_number = models.IntegerField(blank=True, null=True)
    chunk_index = models.IntegerField(blank=True, null=True)
    embedding_id = models.CharField(max_length=255, unique=True)
    chapter_name = models.CharField(max_length=255, blank=True, null=True)
    section_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    relevance_score = models.FloatField(blank=True, null=True)
    last_accessed = models.DateTimeField(blank=True, null=True)
