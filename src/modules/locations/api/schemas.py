from pydantic import BaseModel, ConfigDict


class CityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    city_id: int
    name: str
    