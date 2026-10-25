from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import SessionDep
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserRead, Token
from app.core.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: SessionDep):
    repo = UserRepository(session)
    existing = await repo.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await repo.create(data)

@router.post("/login", response_model=Token)
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    repo = UserRepository(session)
    user = await repo.get_by_email(form_data.username) # username здесь это email
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}