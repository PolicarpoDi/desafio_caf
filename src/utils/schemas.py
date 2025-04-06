from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    _id: str
    name: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Customer(BaseModel):
    _id: str
    fantasy_name: str
    cnpj: str = Field(..., min_length=14, max_length=14)
    status: str
    segment: str


class Transaction(BaseModel):
    _id: str
    tenantId: str
    userId: str
    createdAt: datetime
    updatedAt: datetime
    favoriteFruit: str
    isFraud: bool
    document: dict
