# After
# Before
# Wrap

from pydantic import BaseModel, model_validator
from typing_extensions import Self

class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Las contraseñas no son iguales")
        return self
    
usuario1: UserModel = UserModel(username="Edu",password="asdf", password_repeat="asdf")