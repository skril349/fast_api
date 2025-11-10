from fastapi import APIRouter

router = APIRouter()

users_list = [
    {"id":1, "name":"Toni", "lastname":"Vives"},
    {"id":2, "name":"Marc", "lastname":"garcia"}
]

@router.get("/users/")
async def get_users():
    return users_list