from pydantic import BaseModel, EmailStr, ConfigDict


class Token(BaseModel):
    """JWT Token response."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """JWT Token payload."""
    sub: str  # subject (user email)
    exp: int  # expiration timestamp


class UserCreate(BaseModel):
    """User creation schema."""
    email: EmailStr
    password: str
    full_name: str
    organization_id: int


class UserRegister(BaseModel):
    """User registration schema with organization creation."""
    email: EmailStr
    password: str
    full_name: str
    organization_name: str


class UserPublic(BaseModel):
    """User public schema (no sensitive data)."""
    id: int
    email: str
    full_name: str
    organization_id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
