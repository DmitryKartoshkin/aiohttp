from pydantic import BaseModel, ValidationError
from error import HttpError


class ValidAdvertisement(BaseModel):
    heading: str
    description:  str
    owner: str


def validation_date(date: dict, validation_model):
    try:
        model_items = validation_model(**date)
        return model_items.dict()
    except ValidationError as err:
        raise HttpError(404, err.errors())