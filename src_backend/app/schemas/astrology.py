"""
SK Enterprises | Vedic Astrology & Kundali Schemas
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class KundaliPayload(BaseModel):
    name: str = Field(default="Sumeet Kumar", example="Sumeet Kumar")
    dob: str = Field(default="1993-09-09", example="1993-09-09")
    tob: str = Field(default="12:00", example="12:00")
    pob: str = Field(default="New Delhi, India", example="New Delhi, India")

class AstrologyRequest(BaseModel):
    dob: str = Field(default="1998-05-15")
    tob: str = Field(default="10:30")
    location: str = Field(default="New Delhi, India")
    ayanamsa: str = Field(default="Lahiri")

class KundaliResponse(BaseModel):
    native_name: str
    dob: str
    tob: str
    pob: str
    lagna_rashi: str
    nakshatra: str
    dasha_system: str
    planetary_chart: Dict[str, Any]
    lifelong_predictions: List[str]
    vedic_remedies: List[str]
    calculated_by: str
