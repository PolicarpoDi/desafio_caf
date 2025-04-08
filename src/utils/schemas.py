import re
import json
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, validator, AliasChoices


class User(BaseModel):
    id: str = Field(..., validation_alias=AliasChoices('_id', 'id'))
    name: str
    email: str
    password: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Email inválido')
        return v


class Customer(BaseModel):
    id: str = Field(..., validation_alias=AliasChoices('_id', 'id'))
    fantasy_name: Optional[str] = None
    cnpj: str = Field(..., min_length=14, max_length=14)
    status: str
    segment: str

    @validator('cnpj', pre=True)
    def convert_cnpj_to_string(cls, v):
        if isinstance(v, (int, float)):
            return str(v)
        return v


class Transaction(BaseModel):
    id: str = Field(..., validation_alias=AliasChoices('_id', 'id'))
    tenantId: str
    userId: str
    createdAt: datetime
    updatedAt: datetime
    favoriteFruit: str
    isFraud: bool
    document: Dict[str, Any]

    @validator('createdAt', 'updatedAt', pre=True)
    def parse_datetime(cls, v):
        if isinstance(v, str):
            # Remove o espaço antes do sinal do timezone
            v = v.replace(' +', '+').replace(' -', '-')
            return datetime.fromisoformat(v)
        return v

    @validator('document', pre=True)
    def parse_document(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
