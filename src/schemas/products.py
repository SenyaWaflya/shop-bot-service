from pydantic import BaseModel


class Product(BaseModel):
    id: int
    brand: str
    title: str
    price: int
    quantity: int
    image_path: str | None
