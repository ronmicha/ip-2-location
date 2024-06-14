from fastapi import APIRouter, Depends

from src.api.dependencies import get_dal_instance, validate_ip_address
from src.api.models import FindCountryResponse
from src.dal.base_dal import BaseDAL

router = APIRouter(prefix="/v1", tags=["IP2Country V1 Router"])


@router.get("/find-country")
def find_country(
    ip: str = Depends(validate_ip_address),
    dal: BaseDAL = Depends(get_dal_instance),
) -> FindCountryResponse:
    city, country = dal.get_location_by_ip(ip)
    return FindCountryResponse(country=country, city=city)
