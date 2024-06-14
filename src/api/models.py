from pydantic import BaseModel


class FindCountryResponse(BaseModel):
    country: str
    city: str
