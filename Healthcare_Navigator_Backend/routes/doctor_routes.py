from fastapi import APIRouter
from schemas.doctor_schema import DoctorSearchRequest, DoctorSearchResponse

router = APIRouter()

@router.post("/find-doctors", response_model=DoctorSearchResponse)
async def find_doctors(request: DoctorSearchRequest):

    # temporary dummy response
    doctors = [
        {
            "name": "Dr. Rahul Sharma",
            "specialization": request.specialization,
            "hospital": "City Hospital",
            "address": "Kolkata",
            "distance_km": 3.2,
            "consultation_fee": 500
        }
    ]

    return {"doctors": doctors}