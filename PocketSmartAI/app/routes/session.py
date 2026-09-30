from fastapi import (
    APIRouter,
    Depends,
)

from app.security import get_current_user

from app.services.history import (
    list_history,
)


router = APIRouter(
    prefix="/api",
    tags=["session"],
)


@router.get("/session-info")
def session_info(
    user=Depends(get_current_user),
):

    return {
        "logged_in": True,
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
    }


@router.get("/session-data")
def session_data(
    user=Depends(get_current_user),
):

    history = list_history(
        user["id"],
        10,
    )

    return {
        "user": user,
        "recent_recommendations": history,
    }


@router.get("/history")
def history(
    user=Depends(get_current_user),
):

    return {
        "items": list_history(
            user["id"],
            50,
        )
    }


@router.get(
    "/recommendations-details/{recommendation_id}"
)
def recommendation_details(
    recommendation_id: int,
    user=Depends(get_current_user),
):

    history_items = list_history(
        user["id"],
        100,
    )

    for item in history_items:

        if item["id"] == recommendation_id:

            return item

    return {
        "detail": "Recommendation not found"
    }