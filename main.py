# IMPORT DEPENDENCIES
from fastapi import FastAPI
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import config


api = FastAPI(docs_url="/api/docs")
# INITIATE AUTHENTICATION SCHEME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

# DEFINE SETTINGS
settings = config.Settings() # SETTINGS FROM CONFIG.PY WHERE VARIABLES ARE STORED IN ONE ENVIRONMENT

# GIVE PERMISSION TO FRONTEND
origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# IMPORT MODELS
from routers.auth_router import models
from routers.user_router import models
models.Base.metadata.create_all(bind=engine)

# IMPORT ALL ROUTERS


from routers.auth_router import main as auth
from routers.user_router import main as user


# CUSTOMIZE ALL ENDPOINT HEADERS
api.include_router(auth.router, prefix="/auth", tags=["User Login"])
api.include_router(user.router, prefix="/user", tags=["User"])


# DEFAULT ENDPOINT
@api.get("/")
def welcome():
    return "BACKEND OF FARMERLYNKZ APPLICATION"