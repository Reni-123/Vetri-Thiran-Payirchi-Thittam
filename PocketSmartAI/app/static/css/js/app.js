const API = "";

/* =========================
   TOKEN FUNCTIONS
========================= */

function token() {
    return localStorage.getItem("pocketsmart_token");
}

function authHeaders(extra = {}) {
    if (token()) {
        return {
            ...extra,
            Authorization: `Bearer ${token()}`
        };
    }

    return {
        ...extra
    };
}

function logout() {
    localStorage.removeItem("pocketsmart_token");
    window.location.href = "/login";
}


/* =========================
   COMMON PAGE SETUP
========================= */

document.addEventListener("DOMContentLoaded", () => {

    /* Footer year */
    const year = document.getElementById("year");

    if (year) {
        year.textContent = new Date().getFullYear();
    }


    /* Login / Logout navigation */
    const authLink = document.getElementById("authLink");

    if (authLink && token()) {

        authLink.textContent = "Logout";
        authLink.href = "#";

        authLink.onclick = (event) => {
            event.preventDefault();
            logout();
        };
    }


    /* =========================
       LOGIN FORM
    ========================= */

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {

        loginForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const message = document.getElementById("message");

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;

            if (!email || !password) {

                if (message) {
                    message.textContent = "Please enter email and password.";
                    message.className = "message";
                }

                return;
            }

            try {

                if (message) {
                    message.textContent = "Signing in...";
                    message.className = "message";
                }


                const response = await fetch(
                    "/api/auth/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );


                const data = await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail || "Invalid email or password"
                    );
                }


                /* Save JWT token */

                localStorage.setItem(
                    "pocketsmart_token",
                    data.access_token
                );


                if (message) {
                    message.textContent = "Login successful!";
                    message.className = "message success";
                }


                /* Go to dashboard */

                window.location.href = "/dashboard";

            } catch (error) {

                console.error("Login error:", error);

                if (message) {
                    message.textContent =
                        error.message || "Login failed.";

                    message.className = "message";
                }
            }
        });
    }


    /* =========================
       REGISTER FORM
    ========================= */

    const registerForm =
        document.getElementById("registerForm");

    if (registerForm) {

        registerForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                const message =
                    document.getElementById("message");

                const name =
                    document.getElementById("name").value.trim();

                const email =
                    document.getElementById("email").value.trim();

                const password =
                    document.getElementById("password").value;


                if (!name || !email || !password) {

                    message.textContent =
                        "Please fill in all fields.";

                    return;
                }


                try {

                    message.textContent =
                        "Creating account...";


                    const response =
                        await fetch(
                            "/api/auth/register",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    name: name,
                                    email: email,
                                    password: password
                                })
                            }
                        );


                    const data =
                        await response.json();


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Registration failed"
                        );
                    }


                    message.textContent =
                        "Account created successfully!";

                    message.className =
                        "message success";


                    setTimeout(() => {

                        window.location.href =
                            "/login";

                    }, 800);


                } catch (error) {

                    console.error(
                        "Registration error:",
                        error
                    );

                    message.textContent =
                        error.message ||
                        "Registration failed.";
                }
            }
        );
    }


    /* =========================
       LOGOUT BUTTON
    ========================= */

    const logoutBtn =
        document.getElementById("logoutBtn");


    if (logoutBtn) {

        logoutBtn.addEventListener(
            "click",
            (event) => {

                event.preventDefault();

                logout();
            }
        );
    }

});