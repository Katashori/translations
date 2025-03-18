from pydantic import BaseModel, Field

class ChapterBase(BaseModel):
    title_id: int
    chapter_number: int

class Chapter(ChapterBase):
    id: int

class ChapterAssignmentBase(BaseModel):
    worker_id: int
    chapter_id: int

class ChapterAssignment(ChapterAssignmentBase):
    id: int

class RoleBase(BaseModel):
    role_name: str = Field(max_length=100)

class Role(RoleBase):
    id: int

class TitleBase(BaseModel):
    title_name: str = Field(max_length=100)

class Title(TitleBase):
    id: int

class TitleAssignmentBase(BaseModel):
    worker_id: int
    title_id: int

class TitleAssignment(ChapterAssignmentBase):
    id: int

class WorkerBase(BaseModel):
    role_id: int
    nickname: str = Field(max_length=20)

class Worker(WorkerBase):
    id: int
