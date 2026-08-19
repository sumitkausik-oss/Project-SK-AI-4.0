"""
SK Enterprises | Autonomous Data Analyst Schemas
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class DataAnalyzeRequest(BaseModel):
    dataset_name: str = Field(default="enterprise_metrics.csv", example="enterprise_metrics.csv")
    columns: Optional[List[str]] = Field(default=["revenue", "clv", "churn_rate", "cac"])

class DataSqlRequest(BaseModel):
    query_intent: str = Field(default="Summarize monthly recurring revenue by customer segment")
    dialect: str = Field(default="BigQuery", example="BigQuery")

class DataCleanStep(BaseModel):
    step: str
    result: str

class DataAnalyzeResponse(BaseModel):
    dataset: str
    status: str
    cleaning_pipeline: List[DataCleanStep]
    charts: List[Dict[str, Any]]
    architect: str

class DataSqlResponse(BaseModel):
    intent: str
    dialect: str
    sql: str
    optimization: str
