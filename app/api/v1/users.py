from fastapi import APIRouter
from app.api.deps import CurrentUserDep
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUserDep):
    return current_user