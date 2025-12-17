from pydantic import BaseModel, Field



# 기본 구조 (공통 필드)

class ManufacturerBase(BaseModel):

    name: str = Field(..., title="제조사 이름")

    country: str | None = Field(None, title="국가")

    contact_info: str | None = Field(None, title="연락처")



# 생성할 때 사용하는 구조 (id 없음)

class ManufacturerCreate(ManufacturerBase):

    pass



# 응답할 때 사용하는 구조 (id 포함)

class Manufacturer(ManufacturerBase):

    id: int



    class Config:

        from_attributes = True  # SQLAlchemy 객체 자동 변환
