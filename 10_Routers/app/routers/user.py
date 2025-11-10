from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["USERS"],
    responses={404: {"Description":"Not found"}}
)

users_list = [
    {"id":1, "name":"Toni", "lastname":"Vives"},
    {"id":2, "name":"Marc", "lastname":"garcia"}
]

@router.get("/", tags=["Get all"])
async def get_users():
    return users_list


@router.get("/{user_id}", tags=["Get user by id"])
async def get_user_by_id(user_id:int):
    return next((user for user in users_list if user["id"] == user_id), {"error":"user not found"})