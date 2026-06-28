from pydantic import BaseModel


class UserDto(BaseModel):
    tg_id: int
    username: str | None


class UserResponse(UserDto):
    id: int
