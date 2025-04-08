import re
import json
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, validator, AliasChoices


class User(BaseModel):
    _id: str
    name: str
    email: str
    createdAt: str
    birthdate: str

    @validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Email inválido')
        return v


class Customer(BaseModel):
    _id: str
    fantasyName: str
    cnpj: int
    status: str
    segment: str

    @validator('cnpj')
    def validate_cnpj(cls, v):
        # Converte para string para validar o tamanho
        cnpj_str = str(v)
        if len(cnpj_str) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        
        # Verifica se todos os caracteres são números
        if not cnpj_str.isdigit():
            raise ValueError('CNPJ deve conter apenas números')
        
        return v


class Transaction(BaseModel):
    _id: str
    tenantId: str
    userId: str
    createdAt: str
    updatedAt: str
    favoriteFruit: str
    isFraud: bool
    document: Dict[str, Any]

    @validator('document', pre=True)
    def parse_document(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
