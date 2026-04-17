from typing import List, Optional
from .schemas import ClienteCreate, ClienteRead, ClienteUpdate

db_clientes: List[ClienteRead] = []
id_counter = 1

def crear(data: ClienteCreate) -> ClienteRead:
    global id_counter
    nuevo = ClienteRead(id=id_counter, **data.model_dump())
    db_clientes.append(nuevo)
    id_counter += 1
    return nuevo

def obtener_todos(skip: int = 0, limit: int = 10, nombre: Optional[str] = None) -> List[ClienteRead]:
    resultados = db_clientes
    if nombre:
        resultados = [c for c in resultados if nombre.lower() in c.nombre.lower()]
    return resultados[skip : skip + limit]

def obtener_por_id(id: int) -> Optional[ClienteRead]:
    for c in db_clientes:
        if c.id == id:
            return c
    return None

def actualizar_total(id: int, data: ClienteCreate) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            cliente_actualizado = ClienteRead(id=id, **data.model_dump())
            db_clientes[index] = cliente_actualizado
            return cliente_actualizado
    return None

def desactivar(id: int) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            c_dict = c.model_dump()
            c_dict["activo"] = False
            cliente_actualizado = ClienteRead(**c_dict)
            db_clientes[index] = cliente_actualizado
            return cliente_actualizado
    return None

def verificar_y_aplicar_beneficio_premium(id: int) -> Optional[dict]:
    """
    Regla de negocio: Si el cliente tiene un saldo acumulado mayor a 10000,
    se le bonifica un 10% de su saldo actual por ser 'Cliente Premium'.
    """
    cliente = obtener_por_id(id)
    if not cliente:
        return None

    es_premium = cliente.saldo > 10000
    descuento = 0.0
    saldo_anterior = cliente.saldo

    if es_premium:
        descuento = cliente.saldo * 0.10
        nuevo_saldo = cliente.saldo - descuento
        
        # Actualizamos el saldo
        for index, c in enumerate(db_clientes):
            if c.id == id:
                c_dict = c.model_dump()
                c_dict["saldo"] = nuevo_saldo
                cliente_actualizado = ClienteRead(**c_dict)
                db_clientes[index] = cliente_actualizado
                cliente = cliente_actualizado
                break

    return {
        "cliente_id": id,
        "es_premium": es_premium,
        "descuento_aplicado": descuento,
        "saldo_anterior": saldo_anterior,
        "saldo_nuevo": cliente.saldo
    }
