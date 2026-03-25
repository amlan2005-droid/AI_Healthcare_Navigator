from pydantic import BaseModel
from typing import List, Optional


class DoctorSearchRequest(BaseModel):
    specialization: str
    latitude: float
    longitude: float
    radius_km: Optional[int] = 5


class DoctorInfo(BaseModel):
    name: str
    specialization: str
    hospital: Optional[str] = None
    address: str
    distance_km: Optional[float] = None
    consultation_fee: Optional[int] = None


class DoctorSearchResponse(BaseModel):
    doctors: List[DoctorInfo]