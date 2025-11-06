from fastapi import FastAPI
from pydantic import AfterValidator, BaseModel
from typing import Annotated

# ================== ANNOTATED ========================
def es_par(value:int) -> int:
    if value % 2 ==1:
        raise ValueError(f"{value} no es numero par")
    return value

app = FastAPI()

# After: corre despues de validaciones/transformaciones de pydantic
NumeroPar = Annotated[int, AfterValidator(es_par)]

class Model1(BaseModel):
    # my_number : Annotated[int, AfterValidator(es_par)]
    my_number:NumeroPar

ejemplo:Model1 = Model1(my_number = 2)

class Model2(BaseModel):
    other_number :Annotated[NumeroPar,AfterValidator(lambda v: v + 2)]


ejemplo2:Model2 = Model2(other_number = 4)
print(ejemplo2)


class Model3(BaseModel):
    lista_pares:list[NumeroPar]

ejemplo3:Model3 = Model3(lista_pares=[2,6,10])
print(ejemplo3)

# Before: corre antes de validaciones/transformaciones de pydantic
# Plain: Similar a before pero termina la validacion al retur del valor
# Wrap: Flexible, antes o despues de las valudaciones de pydantic