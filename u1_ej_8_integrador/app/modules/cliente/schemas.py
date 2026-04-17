from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
import re

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, example="Juan Perez")
    email: EmailStr = Field(..., example="juan@example.com")
    cuit: str = Field(..., example="20-12345678-9")
    saldo: float = Field(default=0.0, ge=0.0, example=1500.0)
    activo: bool = True

    @field_validator('cuit')
    @classmethod
    def validar_cuit(cls, v: str) -> str:
        # Validación estricta con regex para cuit: XX-XXXXXXXX-X
        if not re.match(r"^\d{2}-\d{8}-\d{1}$", v):
            raise ValueError('El CUIT debe tener el formato XX-XXXXXXXX-X')
        return v

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = None
    cuit: Optional[str] = None
    saldo: Optional[float] = Field(None, ge=0.0)
    activo: Optional[bool] = None

    @field_validator('cuit')
    @classmethod
    def validar_cuit(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^\d{2}-\d{8}-\d{1}$", v):
            raise ValueError('El CUIT debe tener el formato XX-XXXXXXXX-X')
        return v

class ClienteRead(ClienteBase):
    id: int

class ClientePremiumResponse(BaseModel):
    cliente_id: int
    es_premium: bool
    descuento_aplicado: float
    saldo_anterior: float
    saldo_nuevo: float
