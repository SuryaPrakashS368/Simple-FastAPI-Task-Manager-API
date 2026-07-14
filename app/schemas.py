from pydantic import BaseModel

class TaskCreate(BaseModel):

    title: str

    description: str

    status: str


class TaskUpdate(BaseModel):

    title: str | None = None

    description: str | None = None

    status: str | None = None

class TaskResponse(TaskCreate):

    id: int

    class Config:

        from_attributes = True