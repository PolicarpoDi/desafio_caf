import re
from datetime import datetime

from pydantic import BaseModel, Field, validator


class User(BaseModel):
    _id: str
    name: str
    email: str
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Email inválido')
        return v


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
