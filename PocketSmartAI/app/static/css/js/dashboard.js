(async function () {

    if (!token()) {

        location.href = "/login";

        return;
    }


    try {

        const response =
            await fetch(
                "/api/session-data",
                {
                    headers:
                        authHeaders()
                }
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load dashboard"
            );
        }


        const data =
            await response.json();


        document.getElementById(
            "welcome"
        ).textContent =
            `Welcome, ${data.user.name}. Your latest plans are below.`;


        const history =
            document.getElementById(
                "history"
            );


        if (
            data.recent_recommendations
                .length
        ) {

            history.innerHTML =
                data.recent_recommendations
                    .map(
                        (item) => `

                        <div class="rec-card">

                            <div class="rec-top">

                                <b>
                                    ${item.response.title}
                                </b>

                                <span class="pill">
                                    ${item.planner}
                                </span>

                            </div>

                            <p>
                                ${item.response.summary}
                            </p>

                            <small>
                                ${item.created_at}
                            </small>

                        </div>
                        `
                    )
                    .join("");

        } else {

            history.innerHTML =
                `
                <p>
                    No plans yet.
                    Start with a planner above.
                </p>
                `;
        }

    } catch (error) {

        document.getElementById(
            "welcome"
        ).textContent =
            "Please sign in again.";
    }

})();