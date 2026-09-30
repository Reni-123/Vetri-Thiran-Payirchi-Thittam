from typing import Literal

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


Planner = Literal[
    "home",
    "party",
    "jewelry",
]


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80,
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128,
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class UserOut(BaseModel):

    id: int

    name: str

    email: EmailStr


class HomeItem(BaseModel):

    category: str

    item: str

    quantity: int = Field(
        ge=1
    )

    style: str = "modern"


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    rooms: list[str] = Field(
        min_length=1
    )

    items: list[HomeItem] = Field(
        min_length=1
    )

    style: str = "modern"

    city: str = "Chennai"


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    guests: int = Field(
        gt=0,
        le=10_000,
    )

    event_type: str = Field(
        min_length=2,
        max_length=80,
    )

    venue: str = "home"

    city: str = "Chennai"

    food_preference: str = "mixed"


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    occasion: str = Field(
        min_length=2,
        max_length=80,
    )

    style: str = "elegant"

    outfit_color: str = "not specified"

    outfit_description: str = ""


class RecommendationItem(BaseModel):

    name: str

    category: str

    platform: str

    estimated_price: float = Field(
        ge=0
    )

    reason: str

    link: str

    quantity: int = Field(
        default=1,
        ge=1,
    )


class RecommendationResponse(BaseModel):

    planner: Planner

    title: str

    summary: str

    budget: float

    estimated_total: float = Field(
        ge=0
    )

    remaining_budget: float

    allocation: dict[str, float]

    recommendations: list[
        RecommendationItem
    ]

    tips: list[str]

    ai_generated: bool = False

    model: str | None = None