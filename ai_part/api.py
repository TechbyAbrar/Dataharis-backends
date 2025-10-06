from ninja import NinjaAPI, Schema
from typing import List, Optional, Dict
from datetime import datetime
from .models import AI_User, AI_ChatSession, AI_ChatMessage
from django.db import transaction
from ninja.errors import HttpError
import logging
from ninja.files import UploadedFile
from ninja import File, Form
from django.utils import timezone
import openai
import os

logger = logging.getLogger(__name__)

api = NinjaAPI(title="MS Assistant API with Mycotoxin Testing (Django Ninja)")

from decouple import config

client = openai.OpenAI(api_key=config("OPENAI_API_KEY"))

# Schemas (ported from FastAPI/Pydantic models)
class MessageRequest(Schema):
    session_id: Optional[str] = None
    message: str
    email: str

class MessageResponse(Schema):
    session_id: str
    message: str
    response: str
    timestamp: datetime

class SessionInfo(Schema):
    session_id: str
    email: str
    title: str
    created_at: datetime
    last_updated: datetime

class ChatMessageInfo(Schema):
    id: str
    session_id: str
    message: str
    response: str
    timestamp: datetime

# class MycotoxinTestResult(Schema):
#     test_name: str
#     value: float
#     unit: Optional[str] = None

# class MycotoxinTestRequest(Schema):
#     session_id: str
#     email: str
#     test_results: List[MycotoxinTestResult]

# class MycotoxinTestResponse(Schema):
#     session_id: str
#     analysis: str
#     recommendations: List[str]
#     test_interpretations: Dict[str, str]

# class SymptomAnalysisRequest(Schema):
#     symptoms: List[str]

# class SymptomAnalysisResponse(Schema):
#     recommend_testing: bool
#     matching_symptoms: List[str]
#     suggested_tests: List[str]
#     message: str

class EmailRequest(Schema):
    email: str

class SessionResponse(Schema):
    session_id: str
    created_at: datetime
    email: str
    title: str

class SessionListResponse(Schema):
    sessions: List[SessionResponse]

# Endpoints will be added here in the next step 

@api.post("/session/create", response=SessionResponse)
def create_session(request, data: EmailRequest):
    """Create a new session for a user."""
    try:
        with transaction.atomic():
            user, created = AI_User.objects.get_or_create(email=data.email)
            session = AI_ChatSession.objects.create(
                title="New MS Consultation",
                user=user
            )
            return SessionResponse(
                session_id=str(session.id),
                created_at=session.created_at,
                email=user.email,
                title=session.title
            )
    except Exception as e:
        logger.error(f"Unexpected error in create_session: {str(e)}")
        raise HttpError(500, f"Unexpected error: {str(e)}")

@api.post("/chat", response=MessageResponse)
def process_message(request, data: MessageRequest):
    try:
        if not data.session_id:
            user, _ = AI_User.objects.get_or_create(email=data.email)
            session = AI_ChatSession.objects.create(
                title="New MS Consultation",
                user=user
            )
        else:
            session = AI_ChatSession.objects.get(id=data.session_id)
        
        # Only fetch the last 10 exchanges for memory
        previous_messages = AI_ChatMessage.objects.filter(session=session).order_by("-timestamp")[:10]
        # Reverse to maintain chronological order
        previous_messages = list(previous_messages)[::-1]
        
        

        
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant specialized in Multiple Sclerosis (MS)."}
        ]
        for msg in previous_messages:
            messages.append({"role": "user", "content": msg.query_text})
            messages.append({"role": "assistant", "content": msg.response_text})
        # Add the current user message
        messages.append({"role": "user", "content": data.message})

        # Call OpenAI API with optimized memory
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=messages
        )
        ai_response = response.choices[0].message.content

        chat_message = AI_ChatMessage.objects.create(
            session=session,
            query_text=data.message,
            response_text=ai_response
        )
        
        #####
        try:
            all_messages = AI_ChatMessage.objects.filter(session=session).order_by("timestamp")[:5]
            summary_prompt = [
                {"role": "system", "content": "Summarize the following chat into a very short 4–6 word title."},
                {"role": "user", "content": "\n".join([f"User: {m.query_text}\nAssistant: {m.response_text}" for m in all_messages])}
            ]
            summary_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=summary_prompt,
                max_tokens=20
            )
            new_title = summary_response.choices[0].message.content.strip()
            if new_title:
                session.title = new_title
                session.save(update_fields=["title", "last_updated"])
        except Exception as e:
            logger.warning(f"Failed to auto-update session title: {str(e)}")
            #########
 
        
        
        
        
        
        return MessageResponse(
            session_id=str(session.id),
            message=data.message,
            response=ai_response,
            timestamp=chat_message.timestamp
        )
    except AI_ChatSession.DoesNotExist:
        raise HttpError(404, "Session not found")
    except Exception as e:
        logger.error(f"Unexpected error in process_message: {str(e)}")
        raise HttpError(500, f"Unexpected error: {str(e)}")

# @api.post("/analyze-mycotoxin-tests", response=MycotoxinTestResponse)
# def analyze_mycotoxin_tests(request, data: MycotoxinTestRequest):
#     """Analyze mycotoxin test results and provide recommendations. (Stub, logic to be ported)"""
#     try:
#         # Stub logic for test interpretation
#         test_interpretations = {r.test_name: "Stub interpretation" for r in data.test_results}
#         recommendations = [f"Recommendation for {r.test_name}" for r in data.test_results]
#         analysis = "Stub analysis. Replace with AI logic."
#         return MycotoxinTestResponse(
#             session_id=data.session_id,
#             analysis=analysis,
#             recommendations=recommendations,
#             test_interpretations=test_interpretations
#         )
#     except Exception as e:
#         logger.error(f"Unexpected error in analyze_mycotoxin_tests: {str(e)}")
#         raise HttpError(500, f"Unexpected error: {str(e)}")

# @api.post("/analyze-symptoms", response=SymptomAnalysisResponse)
# def analyze_symptoms(request, data: SymptomAnalysisRequest):
#     """Analyze symptoms to determine if mycotoxin testing is recommended. (Stub, logic to be ported)"""
#     try:
#         # Stub logic for symptom analysis
#         recommend_testing = True
#         matching_symptoms = data.symptoms[:2]  # Just echo first two as matching
#         suggested_tests = ["Test A", "Test B"]
#         message = "Stub analysis. Replace with AI logic."
#         return SymptomAnalysisResponse(
#             recommend_testing=recommend_testing,
#             matching_symptoms=matching_symptoms,
#             suggested_tests=suggested_tests,
#             message=message
#         )
#     except Exception as e:
#         logger.error(f"Unexpected error in analyze_symptoms: {str(e)}")
#         raise HttpError(500, f"Unexpected error: {str(e)}") 

@api.post("/upload")
def upload_knowledge_files(request, files: list[UploadedFile] = File(...), author: str = Form(None), description: str = Form(None), category: str = Form(None), email: str = Form(...)):
    """Upload and process documents for the MS knowledge base (Stub, logic to be ported)"""
    try:
        # Stub: just return filenames and form data
        processed_files = []
        errors = []
        for file in files:
            if not file.name:
                errors.append({"file": "unknown", "error": "Filename is required"})
                continue
            processed_files.append({
                "filename": file.name,
                "status": "stub-success"
            })
        return {
            "uploaded": processed_files,
            "errors": errors,
            "author": author,
            "description": description,
            "category": category,
            "email": email
        }
    except Exception as e:
        logger.error(f"Unexpected error in upload_knowledge_files: {str(e)}")
        raise HttpError(500, f"Unexpected error: {str(e)}") 

# @api.get("/health")
# def health_check(request):
#     """Health check endpoint"""
#     return {"status": "healthy", "timestamp": timezone.now()}

@api.get("/sessions/{session_id}", response=SessionInfo)
def get_session(request, session_id: str):
    try:
        session = AI_ChatSession.objects.get(id=session_id)
        return SessionInfo(
            session_id=str(session.id),
            email=session.user.email,
            title=session.title,
            created_at=session.created_at,
            last_updated=session.last_updated
        )
    except AI_ChatSession.DoesNotExist:
        raise HttpError(404, "Session not found")
    except Exception as e:
        logger.error(f"Error getting session: {str(e)}")
        raise HttpError(500, "Internal server error")

@api.get("/session/{session_id}/chats", response=List[ChatMessageInfo])
def get_session_messages(request, session_id: str):
    try:
        messages = AI_ChatMessage.objects.filter(session__id=session_id).order_by("timestamp")
        return [
            ChatMessageInfo(
                id=str(msg.id),
                session_id=str(msg.session.id),
                message=msg.query_text,
                response=msg.response_text,
                timestamp=msg.timestamp
            ) for msg in messages
        ]
    except Exception as e:
        logger.error(f"Error getting session messages: {str(e)}")
        raise HttpError(500, "Internal server error")

@api.get("/user/{email}/sessions", response=List[SessionResponse])
def get_sessions_by_email(request, email: str):
    try:
        sessions = AI_ChatSession.objects.filter(user__email=email).order_by("-created_at")
        return [
            SessionResponse(
                session_id=str(session.id),
                created_at=session.created_at,
                email=session.user.email,
                title=session.title
            ) for session in sessions
        ]
    except Exception as e:
        logger.error(f"Error getting sessions by email: {str(e)}")
        raise HttpError(500, "Failed to get sessions") 

@api.delete("/sessions/{session_id}")
def delete_session(request, session_id: str):
    try:
        session = AI_ChatSession.objects.get(id=session_id)
        # Delete all chat messages associated with the session
        AI_ChatMessage.objects.filter(session=session).delete()
        # Delete the session itself
        session.delete()
        return {"success": True, "detail": f"Session {session_id} and its messages deleted."}
    except AI_ChatSession.DoesNotExist:
        return {"success": False, "detail": "Session not found."}
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        return {"success": False, "detail": f"Unexpected error: {str(e)}"} 