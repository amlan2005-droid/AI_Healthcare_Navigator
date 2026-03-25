from pydantic import BaseModel
from typing import List, Optional


class MedicineRequest(BaseModel):
    name: str
    dosage: Optional[str] = None


class MedicinePrice(BaseModel):
    pharmacy: str
    price: float
    availability: Optional[bool] = True


class MedicinePriceResponse(BaseModel):
    medicine_name: str
    prices: List[MedicinePrice]
    cheapest_pharmacy: Optional[str] = None