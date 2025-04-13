document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerform");

    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("n1").value.trim();
        const username = document.getElementById("n2").value.trim();
        const email = document.getElementById("n3").value.toLowerCase().trim();
        const password = document.getElementById("n4").value;

        if (!name || !username || !email || !password) {
            Swal.fire({
                text: "All fields are mandatory to fill.",
                icon: "warning",
                confirmButtonText: "OK"
            });
            return;
        }

        if (!name.match(/^[A-Za-z]+(?: [A-Za-z]+)*$/)) {
            Swal.fire({
                title: "INVALID NAME",
                text: "Name should contain only alphabets.",
                icon: "warning",
                confirmButtonText: "OK"
            });
            return;
        }

        if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            Swal.fire({
                title: "INVALID EMAIL ADDRESS",
                text: "Please enter the correct email address.",
                icon: "warning",
                confirmButtonText: "OK"
            });
            return;
        }

        if (password.length < 8) {
            Swal.fire({
                title: "WEAK PASSWORD",
                text: "Use at least 8 Characters.",
                icon: "warning",
                confirmButtonText: "OK"
            });
            return;
        }

        Swal.fire({
            title: "Processing",
            text: "Please wait...",
            icon: "info",
            showConfirmButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const formData = new FormData(registerForm);

        fetch('/register', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(async response => {
            Swal.close();

            if (!response.ok) {
                throw new Error('Server returned an error');
            }

            const data = await response.json();

            if (data.success) {
                Swal.fire({
                    title: "Account Created Successfully, Please Login",
                    icon: "success",
                    confirmButtonText: "OK"
                }).then(() => {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                });
            } else {
                Swal.fire({
                    title: "Registration Failed, Please try again.",
                    text: data.message,
                    icon: "error",
                    confirmButtonText: "OK"
                });
            }
        })
        .catch(error => {
            Swal.close();
            console.error("Registration error", error);

            Swal.fire({
                title: "Error",
                text: error.message || "Could not connect to server",
                icon: "error",
                confirmButtonText: "OK"
            });
        });
    });
});