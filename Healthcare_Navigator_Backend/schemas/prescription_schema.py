from pydantic import BaseModel
from typing import List, Optional


class PrescriptionUploadRequest(BaseModel):
    session_id: Optional[str] = None
    image_url: Optional[str] = None


class MedicineItem(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None


class PrescriptionExtractResponse(BaseModel):
    medicines: List[MedicineItem]
    notes: Optional[str] = None