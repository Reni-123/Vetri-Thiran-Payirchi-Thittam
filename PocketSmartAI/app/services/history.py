import json

from app.db import get_db


def save_recommendation(
    user_id: int,
    planner: str,
    request_data: dict,
    response_data: dict,
):

    with get_db() as db:

        db.execute(
            """
            INSERT INTO recommendations
            (
                user_id,
                planner,
                request_json,
                response_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                planner,
                json.dumps(
                    request_data,
                    ensure_ascii=False,
                ),
                json.dumps(
                    response_data,
                    ensure_ascii=False,
                ),
            ),
        )


def list_history(
    user_id: int,
    limit: int = 30,
):

    with get_db() as db:

        rows = db.execute(
            """
            SELECT
                id,
                planner,
                request_json,
                response_json,
                created_at
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                user_id,
                limit,
            ),
        ).fetchall()

    return [

        {
            "id": row["id"],

            "planner":
                row["planner"],

            "request":
                json.loads(
                    row["request_json"]
                ),

            "response":
                json.loads(
                    row["response_json"]
                ),

            "created_at":
                row["created_at"],
        }

        for row in rows
    ]