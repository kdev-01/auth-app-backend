from pydantic import BaseModel, ConfigDict, PositiveInt


class SportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sport_id: PositiveInt
    name: str
    