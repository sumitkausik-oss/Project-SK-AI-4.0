"""
SK Enterprises | SKAI OS Control REST Endpoints
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src_backend.app.database.base import get_db
from src_backend.app.services.os_control_service import OSControlService
from src_backend.app.services.permission_service import PermissionService
from src_backend.app.repositories.memory_repo import AuditRepository

router = APIRouter(prefix="/os", tags=["OS Control & Actuators"])

# Request Schemas
class OpenAppRequest(BaseModel):
    app: str = Field(..., example="notepad")

class CloseAppRequest(BaseModel):
    target: str = Field(..., example="notepad")

class FileCreateRequest(BaseModel):
    file_path: str = Field(..., example="Desktop/test.txt")
    content: str = Field(default="", example="Hello from SKAI")

class FolderCreateRequest(BaseModel):
    folder_path: str = Field(..., example="Desktop/MyProject")

class FileReadRequest(BaseModel):
    file_path: str = Field(..., example="Desktop/test.txt")

class FileWriteRequest(BaseModel):
    file_path: str = Field(..., example="Desktop/test.txt")
    content: str = Field(...)
    append: bool = Field(default=False)

class FileDeleteRequest(BaseModel):
    target_path: str = Field(..., example="Desktop/test.txt")

class TerminalCommandRequest(BaseModel):
    command: str = Field(..., example="dir")
    cwd: Optional[str] = Field(default=None)
    timeout_sec: int = Field(default=30)

class SearchFilesRequest(BaseModel):
    query: str = Field(..., example="python")
    base_dir: Optional[str] = Field(default=None)
    content_search: bool = Field(default=True)
    max_results: int = Field(default=25)

# Endpoints
@router.post("/app/open", summary="Open an Application")
def open_app(req: OpenAppRequest, db: Session = Depends(get_db)):
    res = OSControlService.open_app(req.app)
    AuditRepository.log_event(db, "OPEN_APP", f"Opened app {req.app}. Success: {res.get('success')}", "INFO", "API")
    return res

@router.post("/app/close", summary="Close an Application")
def close_app(req: CloseAppRequest, db: Session = Depends(get_db)):
    res = OSControlService.close_app(req.target)
    AuditRepository.log_event(db, "CLOSE_APP", f"Closed app {req.target}. Success: {res.get('success')}", "WARNING", "API")
    return res

@router.get("/app/running", summary="List Running Applications")
def list_running_apps():
    return OSControlService.list_running_apps()

@router.post("/file/create", summary="Create a File")
def create_file(req: FileCreateRequest, db: Session = Depends(get_db)):
    res = OSControlService.create_file(req.file_path, req.content)
    AuditRepository.log_event(db, "CREATE_FILE", f"Created file {req.file_path}", "INFO", "API")
    return res

@router.post("/folder/create", summary="Create a Folder")
def create_folder(req: FolderCreateRequest, db: Session = Depends(get_db)):
    res = OSControlService.create_folder(req.folder_path)
    AuditRepository.log_event(db, "CREATE_FOLDER", f"Created folder {req.folder_path}", "INFO", "API")
    return res

@router.get("/file/read", summary="Read a File")
def read_file(path: str = Query(..., description="Path to file")):
    return OSControlService.read_file(path)

@router.post("/file/write", summary="Write or Append to a File")
def write_file(req: FileWriteRequest, db: Session = Depends(get_db)):
    res = OSControlService.write_file(req.file_path, req.content, req.append)
    AuditRepository.log_event(db, "WRITE_FILE", f"Wrote to file {req.file_path}", "INFO", "API")
    return res

@router.delete("/file/delete", summary="Delete a File or Folder")
def delete_file(path: str = Query(..., description="Target path to delete"), db: Session = Depends(get_db)):
    res = OSControlService.delete_file(path)
    AuditRepository.log_event(db, "DELETE_FILE", f"Deleted {path}", "WARNING", "API")
    return res

@router.get("/folder/list", summary="List Folder Contents")
def list_folder(path: str = Query("Desktop", description="Folder path")):
    return OSControlService.list_folder(path)

@router.post("/terminal/run", summary="Execute Terminal Command")
def run_terminal(req: TerminalCommandRequest, db: Session = Depends(get_db)):
    res = OSControlService.run_terminal_command(req.command, req.cwd, req.timeout_sec)
    AuditRepository.log_event(db, "TERMINAL_COMMAND", f"Ran cmd '{req.command}'. Exit: {res.get('exit_code')}", "INFO", "API")
    return res

@router.get("/search", summary="Intelligent Local Search")
def search_files(
    q: str = Query(..., description="Search query"),
    base_dir: Optional[str] = Query(None, description="Base directory to search"),
    content: bool = Query(True, description="Enable content search")
):
    return OSControlService.search_local_files(q, base_dir, content_search=content)

@router.post("/screenshot", summary="Capture Display Screenshot")
def take_screenshot(filename: Optional[str] = Query(None), db: Session = Depends(get_db)):
    res = OSControlService.take_screenshot(filename)
    AuditRepository.log_event(db, "TAKE_SCREENSHOT", f"Captured screenshot: {res.get('filename')}", "INFO", "API")
    return res

@router.get("/code/tree", summary="Scan Project Tree")
def get_project_tree(path: str = Query(..., description="Project root path")):
    return OSControlService.code_assist_read_project(path)
