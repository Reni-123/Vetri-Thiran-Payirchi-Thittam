function requireAuth() {
    const token = localStorage.getItem("pocketsmart_token");

    if (!token) {
        window.location.href = "/login";
        return false;
    }

    return true;
}


function authHeaders(extraHeaders = {}) {
    const token = localStorage.getItem("pocketsmart_token");

    const headers = {
        ...extraHeaders
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    return headers;
}


function money(value) {
    return "₹" + Number(value || 0).toLocaleString("en-IN", {
        maximumFractionDigits: 0
    });
}


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function renderResult(data) {
    const result = document.getElementById("result");

    if (!result) {
        return;
    }

    const recommendations = Array.isArray(data.recommendations)
        ? data.recommendations
        : [];

    const tips = Array.isArray(data.tips)
        ? data.tips
        : [];

    result.innerHTML = `
        <div class="summary">

            <b>
                ${escapeHtml(data.title || "PocketSmart AI Plan")}
            </b>

            <p>
                ${escapeHtml(data.summary || "")}
            </p>

            <span class="pill">
                ${
                    data.ai_generated
                        ? "Gemini generated"
                        : "Local fallback"
                }
            </span>

        </div>


        <div class="result-grid">

            <div class="stat">
                <small>Budget</small>
                <b>${money(data.budget)}</b>
            </div>

            <div class="stat">
                <small>Estimated total</small>
                <b>${money(data.estimated_total)}</b>
            </div>

            <div class="stat">
                <small>Remaining</small>
                <b>${money(data.remaining_budget)}</b>
            </div>

        </div>


        <h3>Recommendations</h3>

        ${
            recommendations.length
                ? recommendations.map((item) => {

                    const quantity =
                        Number(item.quantity || 1);

                    const price =
                        Number(item.estimated_price || 0);

                    return `
                        <div class="rec-card">

                            <div class="rec-top">

                                <b>
                                    ${escapeHtml(
                                        item.name || "Item"
                                    )}
                                </b>

                                <b>
                                    ${money(price * quantity)}
                                </b>

                            </div>


                            <span class="pill">

                                ${escapeHtml(
                                    item.platform || ""
                                )}

                                ·

                                ${escapeHtml(
                                    item.category || ""
                                )}

                            </span>


                            <p>
                                ${escapeHtml(
                                    item.reason || ""
                                )}
                            </p>


                            ${
                                item.link
                                    ? `
                                        <a
                                            class="btn ghost"
                                            href="${escapeHtml(item.link)}"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            Search platform
                                        </a>
                                      `
                                    : ""
                            }

                        </div>
                    `;

                }).join("")
                : `
                    <p>No recommendations available.</p>
                  `
        }


        <h3>Tips</h3>

        ${
            tips.length
                ? `
                    <ul>
                        ${
                            tips.map(
                                tip =>
                                    `<li>${escapeHtml(tip)}</li>`
                            ).join("")
                        }
                    </ul>
                  `
                : `
                    <ul>
                        <li>Plan within your available budget.</li>
                    </ul>
                  `
        }
    `;
}


async function send(url, options = {}) {

    const headers = authHeaders(
        options.headers || {}
    );

    const response = await fetch(url, {
        ...options,
        headers: headers
    });


    let data;

    try {
        data = await response.json();
    } catch (error) {
        throw new Error(
            `Server returned ${response.status}`
        );
    }


    if (response.status === 401) {

        localStorage.removeItem(
            "pocketsmart_token"
        );

        window.location.href = "/login";

        return;
    }


    if (!response.ok) {

        throw new Error(
            data.detail ||
            data.message ||
            `Request failed (${response.status})`
        );
    }


    return data;
}


/* =========================================================
   HOME PLANNER
========================================================= */

const homeForm =
    document.getElementById("homeForm");


if (homeForm) {

    const addItem =
        document.getElementById("addItem");


    if (addItem) {

        addItem.onclick = () => {

            const row =
                document.createElement("div");

            row.className =
                "item-row";


            row.innerHTML = `
                <input
                    class="category"
                    value="decor"
                    placeholder="Category"
                >

                <input
                    class="item"
                    value="Wall art"
                    placeholder="Item"
                >

                <input
                    class="qty"
                    type="number"
                    value="1"
                    min="1"
                >

                <input
                    class="itemstyle"
                    value="modern"
                    placeholder="Style"
                >
            `;


            const items =
                document.getElementById("items");

            if (items) {
                items.appendChild(row);
            }
        };
    }


    homeForm.onsubmit =
        async (event) => {

            event.preventDefault();


            if (!requireAuth()) {
                return;
            }


            const rows =
                [
                    ...document.querySelectorAll(
                        "#items .item-row"
                    )
                ];


            const items =
                rows.map((row) => {

                    return {

                        category:
                            row.querySelector(
                                ".category"
                            )?.value || "",

                        item:
                            row.querySelector(
                                ".item"
                            )?.value || "",

                        quantity:
                            Number(
                                row.querySelector(
                                    ".qty"
                                )?.value || 1
                            ),

                        style:
                            row.querySelector(
                                ".itemstyle"
                            )?.value || ""
                    };
                });


            const payload = {

                budget:
                    Number(
                        document.getElementById(
                            "budget"
                        )?.value || 0
                    ),

                city:
                    document.getElementById(
                        "city"
                    )?.value || "",

                style:
                    document.getElementById(
                        "style"
                    )?.value || "",

                rooms:
                    (
                        document.getElementById(
                            "rooms"
                        )?.value || ""
                    )
                    .split(",")
                    .map(item => item.trim())
                    .filter(Boolean),

                items:
                    items
            };


            try {

                const data =
                    await send(
                        "/api/generate-home",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    );


                renderResult(data);

            } catch (error) {

                console.error(
                    "HOME ERROR:",
                    error
                );

                alert(
                    error.message
                );
            }
        };
}


/* =========================================================
   PARTY PLANNER
========================================================= */

const partyForm =
    document.getElementById("partyForm");


if (partyForm) {

    partyForm.onsubmit =
        async (event) => {

            event.preventDefault();


            if (!requireAuth()) {
                return;
            }


            const budget =
                Number(
                    document.getElementById(
                        "budget"
                    )?.value || 0
                );


            const guests =
                Number(
                    document.getElementById(
                        "guests"
                    )?.value || 0
                );


            const eventType =
                document.getElementById(
                    "event_type"
                )?.value || "";


            const venue =
                document.getElementById(
                    "venue"
                )?.value || "";


            const city =
                document.getElementById(
                    "city"
                )?.value || "";


            const foodPreference =
                document.getElementById(
                    "food_preference"
                )?.value || "";


            if (!budget || budget <= 0) {

                alert(
                    "Please enter a valid party budget."
                );

                return;
            }


            if (!guests || guests <= 0) {

                alert(
                    "Please enter the number of guests."
                );

                return;
            }


            const payload = {

                budget:
                    budget,

                guests:
                    guests,

                event_type:
                    eventType,

                venue:
                    venue,

                city:
                    city,

                food_preference:
                    foodPreference
            };


            console.log(
                "PARTY PAYLOAD:",
                payload
            );


            try {

                const data =
                    await send(
                        "/api/generate-party",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    );


                console.log(
                    "PARTY RESPONSE:",
                    data
                );


                renderResult(data);

            } catch (error) {

                console.error(
                    "PARTY ERROR:",
                    error
                );

                alert(
                    "Party generation failed: " +
                    error.message
                );
            }
        };
}


/* =========================================================
   JEWELRY PLANNER
========================================================= */

const jewelryForm =
    document.getElementById("jewelryForm");


if (jewelryForm) {

    jewelryForm.onsubmit =
        async (event) => {

            event.preventDefault();


            if (!requireAuth()) {
                return;
            }


            const budget =
                Number(
                    document.getElementById(
                        "budget"
                    )?.value || 0
                );


            const occasion =
                document.getElementById(
                    "occasion"
                )?.value || "";


            const style =
                document.getElementById(
                    "style"
                )?.value || "";


            const outfitColor =
                document.getElementById(
                    "outfit_color"
                )?.value || "";


            const outfitDescription =
                document.getElementById(
                    "outfit_description"
                )?.value || "";


            if (!budget || budget <= 0) {

                alert(
                    "Please enter a valid jewelry budget."
                );

                return;
            }


            const payload = {

                budget:
                    budget,

                occasion:
                    occasion,

                style:
                    style,

                outfit_color:
                    outfitColor,

                outfit_description:
                    outfitDescription
            };


            console.log(
                "JEWELRY PAYLOAD:",
                payload
            );


            const formData =
                new FormData();


            /*
             * IMPORTANT:
             * planners.py expects:
             *
             * data = Form(...)
             *
             * therefore the JSON must be
             * sent under the field "data".
             */

            formData.append(
                "data",
                JSON.stringify(payload)
            );


            const imageInput =
                document.getElementById(
                    "outfit_image"
                );


            if (
                imageInput &&
                imageInput.files &&
                imageInput.files.length > 0
            ) {

                formData.append(
                    "outfit_image",
                    imageInput.files[0]
                );
            }


            try {

                const data =
                    await send(
                        "/api/generate-jewelry",
                        {
                            method: "POST",

                            /*
                             * DO NOT set Content-Type.
                             * Browser creates the multipart
                             * boundary automatically.
                             */

                            body:
                                formData
                        }
                    );


                console.log(
                    "JEWELRY RESPONSE:",
                    data
                );


                renderResult(data);

            } catch (error) {

                console.error(
                    "JEWELRY ERROR:",
                    error
                );

                alert(
                    "Jewelry generation failed: " +
                    error.message
                );
            }
        };
}