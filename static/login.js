document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginform");
    
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();

        // Get form values
        const email = document.getElementById("n1").value.toLowerCase().trim();
        const password = document.getElementById("n2").value;

        // Basic validation
        if (!email || !password) {
        Swal.fire({
            text: "All fields are mandatory to fill.",
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
        });

        const formData = new FormData(loginForm);
        
        fetch('/login', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network Error');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                swal.fire({
                    title: "Login Successful",
                    icon: "success",
                    confirmButtonText: "OK"
                }).then(() => {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                });
            } else {
                swal.fire({
                    title: "Login Failed",
                    text: data.message,
                    icon: "error",
                    confirmButtonText: "OK"
                });
            }
        })
        .catch(error => {
            swal.close();
            if (error.message) {
                swal("Error", error.message, "error");
            } else {
                swal("Error", "Could not connect to server", "error");
            }
            console.error("Login error", error);
        });
    });
});