from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List, Optional
from . import schemas, services

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED)
def alta_cliente(cliente: schemas.ClienteCreate):
    return services.crear(cliente)

@router.get("/", response_model=List[schemas.ClienteRead], status_code=status.HTTP_200_OK)
def listar_clientes(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, le=50),
    nombre: Optional[str] = Query(None, description="Filtro por parte del nombre")
):
    return services.obtener_todos(skip, limit, nombre)

@router.get("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def detalle_cliente(id: int = Path(..., gt=0)):
    cliente = services.obtener_por_id(id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente

@router.put("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def actualizar_cliente(cliente: schemas.ClienteCreate, id: int = Path(..., gt=0)):
    actualizado = services.actualizar_total(id, cliente)
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return actualizado

@router.put("/{id}/desactivar", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return desactivado

@router.post("/{id}/beneficio-premium", response_model=schemas.ClientePremiumResponse, status_code=status.HTTP_200_OK)
def aplicar_beneficio_premium(id: int = Path(..., gt=0)):
    """Ejecuta la regla de negocio para aplicar beneficios a un cliente."""
    resultado = services.verificar_y_aplicar_beneficio_premium(id)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return resultado
