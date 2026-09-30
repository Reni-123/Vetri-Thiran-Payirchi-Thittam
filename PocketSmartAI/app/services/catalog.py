from urllib.parse import quote_plus


PLATFORMS = {

    "Amazon":
        "https://www.amazon.in/s?k={q}",

    "Flipkart":
        "https://www.flipkart.com/search?q={q}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={q}",

    "Swiggy":
        "https://www.swiggy.com/search?query={q}",

    "Zomato":
        "https://www.zomato.com/chennai/restaurants?query={q}",

    "OYO":
        "https://www.oyorooms.com/search?location={q}",
}


def link(
    platform: str,
    query: str,
) -> str:

    template = PLATFORMS.get(
        platform,
        PLATFORMS["Amazon"],
    )

    return template.format(
        q=quote_plus(query)
    )


def home_fallback(req):

    base = max(
        req.budget
        / max(len(req.items), 1),
        1,
    )

    items = []

    platforms = [
        "IKEA",
        "Amazon",
        "Flipkart",
    ]

    for index, item in enumerate(
        req.items
    ):

        platform = platforms[
            index % len(platforms)
        ]

        price = round(
            min(
                base,
                req.budget * 0.28,
            ),
            2,
        )

        items.append(
            {
                "name":
                    f"{req.style.title()} "
                    f"{item.item}",

                "category":
                    item.category,

                "platform":
                    platform,

                "estimated_price":
                    price,

                "reason":
                    (
                        f"Fits a "
                        f"{req.style} setup "
                        "and keeps room for "
                        "the other requested "
                        "items."
                    ),

                "link":
                    link(
                        platform,
                        item.item,
                    ),

                "quantity":
                    item.quantity,
            }
        )

    return items


def party_fallback(req):

    per_guest = (
        req.budget
        / req.guests
    )

    return [

        {
            "name":
                f"{req.event_type.title()} "
                "catering package",

            "category":
                "food",

            "platform":
                "Swiggy",

            "estimated_price":
                round(
                    req.budget * 0.45,
                    2,
                ),

            "reason":
                (
                    f"Keeps catering "
                    f"near 45% of the "
                    f"budget for "
                    f"{req.guests} guests."
                ),

            "link":
                link(
                    "Swiggy",
                    req.event_type
                    + " catering",
                ),

            "quantity": 1,
        },

        {
            "name":
                f"{req.event_type.title()} "
                "decoration package",

            "category":
                "decoration",

            "platform":
                "Amazon",

            "estimated_price":
                round(
                    req.budget * 0.20,
                    2,
                ),

            "reason":
                (
                    "A moderate "
                    "decoration allowance "
                    "leaves room for food "
                    "and entertainment."
                ),

            "link":
                link(
                    "Amazon",
                    req.event_type
                    + " party decorations",
                ),

            "quantity": 1,
        },

        {
            "name":
                f"{req.venue.title()} "
                "venue option",

            "category":
                "venue",

            "platform":
                (
                    "OYO"
                    if req.venue != "home"
                    else "Amazon"
                ),

            "estimated_price":
                round(
                    req.budget * 0.25,
                    2,
                ),

            "reason":
                (
                    "Designed around "
                    "the selected venue "
                    "type and an "
                    f"approximate ₹"
                    f"{per_guest:,.0f} "
                    "budget per guest."
                ),

            "link":
                link(
                    (
                        "OYO"
                        if req.venue != "home"
                        else "Amazon"
                    ),
                    req.city
                    + " event venue",
                ),

            "quantity": 1,
        },
    ]


def jewelry_fallback(req):

    return [

        {
            "name":
                f"{req.style.title()} "
                "earrings",

            "category":
                "earrings",

            "platform":
                "Amazon",

            "estimated_price":
                round(
                    req.budget * 0.25,
                    2,
                ),

            "reason":
                (
                    f"Coordinates with "
                    f"a {req.outfit_color} "
                    f"outfit and "
                    f"{req.occasion} "
                    "occasion."
                ),

            "link":
                link(
                    "Amazon",
                    (
                        f"{req.style} "
                        f"earrings "
                        f"{req.outfit_color}"
                    ),
                ),

            "quantity": 1,
        },

        {
            "name":
                f"{req.style.title()} "
                "necklace set",

            "category":
                "necklace",

            "platform":
                "Flipkart",

            "estimated_price":
                round(
                    req.budget * 0.45,
                    2,
                ),

            "reason":
                (
                    "A balanced "
                    "statement piece "
                    "for the selected "
                    "occasion."
                ),

            "link":
                link(
                    "Flipkart",
                    (
                        f"{req.style} "
                        f"necklace "
                        f"{req.outfit_color}"
                    ),
                ),

            "quantity": 1,
        },

        {
            "name":
                f"{req.style.title()} "
                "bracelet",

            "category":
                "bracelet",

            "platform":
                "Amazon",

            "estimated_price":
                round(
                    req.budget * 0.15,
                    2,
                ),

            "reason":
                (
                    "Adds a coordinated "
                    "accent without "
                    "using too much of "
                    "the budget."
                ),

            "link":
                link(
                    "Amazon",
                    f"{req.style} bracelet",
                ),

            "quantity": 1,
        },
    ]