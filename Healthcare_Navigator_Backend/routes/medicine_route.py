from fastapi import APIRouter
from schemas.medicine_schema import MedicineRequest, MedicinePriceResponse

router = APIRouter()

@router.post("/medicine-price", response_model=MedicinePriceResponse)
async def get_medicine_price(request: MedicineRequest):

    prices = [
        {"pharmacy": "1mg", "price": 25.0},
        {"pharmacy": "PharmEasy", "price": 22.5},
        {"pharmacy": "Apollo", "price": 27.0}
    ]

    return {
        "medicine_name": request.name,
        "prices": prices,
        "cheapest_pharmacy": "PharmEasy"
    }