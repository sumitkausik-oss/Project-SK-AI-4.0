"""
SK Enterprises | Education, Data & Cloud Endpoints
Inventor & Sole Architect: Sumeet Kumar
"""
from fastapi import APIRouter
from src_backend.app.schemas.education import EducationTestRequest, EducationLectureRequest
from src_backend.app.schemas.data import DataAnalyzeRequest, DataSqlRequest
from src_backend.app.schemas.admin import CloudTaskRequest
from src_backend.app.services.education_service import EducationService
from src_backend.app.services.data_service import DataService
from src_backend.app.services.cloud_service import CloudService

router_education = APIRouter(prefix="/education", tags=["Universal STEM & Education"])

@router_education.post("/test", summary="Generate Automated Assessment Test")
def generate_education_test(req: EducationTestRequest):
    return EducationService.generate_assessment(req.subject, req.standard, req.difficulty, req.topic)

@router_education.post("/lecture", summary="Generate First-Principles Lecture Notes")
def generate_education_lecture(req: EducationLectureRequest):
    return EducationService.generate_lecture(req.topic)

router_data = APIRouter(prefix="/data", tags=["Autonomous Data Analyst"])

@router_data.post("/analyze", summary="Analyze and Clean Dataset")
def analyze_data(req: DataAnalyzeRequest):
    return DataService.analyze_dataset(req.dataset_name, req.columns)

@router_data.post("/sql", summary="Synthesize Optimized SQL Query")
def generate_sql(req: DataSqlRequest):
    return DataService.generate_sql(req.query_intent, req.dialect)

router_cloud = APIRouter(prefix="/cloud", tags=["Cloud DevOps & Zero-Trust"])

@router_cloud.post("/execute", summary="Execute Zero-Trust DevOps Actuation")
def execute_cloud_task(req: CloudTaskRequest):
    return CloudService.execute_task(req.action, req.target_user)
