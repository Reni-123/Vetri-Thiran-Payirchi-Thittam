from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.models.schemas import (
    HomeRequest,
    JewelryRequest,
    PartyRequest,
    RecommendationResponse,
)

from app.security import (
    get_current_user,
)

from app.services.gemini_service import (
    generate,
)

from app.services.history import (
    save_recommendation,
)


router = APIRouter(
    prefix="/api",
    tags=["planners"],
)


def _save(
    user,
    planner,
    request_data,
    response,
):

    save_recommendation(
        user["id"],
        planner,
        request_data,
        response.model_dump(),
    )

    return response


@router.post(
    "/generate-home",
    response_model=RecommendationResponse,
)
def generate_home(
    data: HomeRequest,
    user=Depends(get_current_user),
):

    response = generate(
        "home",
        data,
    )

    return _save(
        user,
        "home",
        data.model_dump(),
        response,
    )


@router.post(
    "/generate-party",
    response_model=RecommendationResponse,
)
def generate_party(
    data: PartyRequest,
    user=Depends(get_current_user),
):

    response = generate(
        "party",
        data,
    )

    return _save(
        user,
        "party",
        data.model_dump(),
        response,
    )


@router.post(
    "/generate-jewelry",
    response_model=RecommendationResponse,
)
async def generate_jewelry(
    data: str = Form(...),
    outfit_image: UploadFile | None = File(
        default=None
    ),
    user=Depends(get_current_user),
):

    try:

        payload = JewelryRequest.model_validate_json(
            data
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=f"Invalid jewelry data: {exc}",
        )

    image_bytes = None
    mime = None

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPEG, PNG, and WEBP "
                    "images are supported"
                ),
            )

        image_bytes = (
            await outfit_image.read()
        )

        if len(image_bytes) > (
            5 * 1024 * 1024
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Image must be 5 MB or smaller"
                ),
            )

        mime = outfit_image.content_type

    response = generate(
        "jewelry",
        payload,
        image_bytes,
        mime,
    )

    return _save(
        user,
        "jewelry",
        payload.model_dump(),
        response,
    )