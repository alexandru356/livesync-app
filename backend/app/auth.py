from typing import Annotated
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User, get_db
from schemas import SignUp, Token

SECRET_KEY = "d10e9b956ba7f3221d129e6e3dfed8c4bba6fd048783c4d387eda99ba6222828"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db_dependency = Annotated[Session,Depends(get_db)]

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: SignUp):
    create_user_model = User(
        email = create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = 'Could not validate user.')
    token = create_access_token(user.email, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(email: str, password: str,db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        email: str = payload.get('email')
        if user_id is None or email is None:
            raise credentials_exception
        return {'email': email, 'id': user_id}
    except jwt.PyJWTError:
        raise credentials_exception


