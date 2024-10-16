function validateForm() {
    const username = document.forms["loginForm"]["username"].value;
    const password = document.forms["loginForm"]["password"].value;
    const errorElement = document.getElementById("error-msg");

    errorElement.innerHTML = "";

    if (username === "") {
        errorElement.innerHTML = "Username harus diisi.";
        return false;
    }

    const usernameRegex = /^[a-zA-Z0-9]+$/;
    if (!usernameRegex.test(username)) {
        errorElement.innerHTML = "Username hanya boleh mengandung huruf dan angka.";
        return false;
    }

    if (password === "") {
        errorElement.innerHTML = "Password harus diisi.";
        return false;
    }

    if (username !== "admin" && password.length < 8) {
        errorElement.innerHTML = "Password harus minimal 8 karakter";
        return false;
    }

    return true;
}

function showResetPassword() {
    document.getElementById("resetPasswordForm").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function hideResetPassword() {
    document.getElementById("resetPasswordForm").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    const iconElement = icon.querySelector('i');
    
    if (input.type === "password") {
        input.type = "text";
        iconElement.classList.remove('fa-lock');
        iconElement.classList.add('fa-lock-open');
    } else {
        input.type = "password";
        iconElement.classList.remove('fa-lock-open');
        iconElement.classList.add('fa-lock');
    }
}

function validateResetForm() {
    const resetUsername = document.getElementById("resetUsername").value;
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const resetErrorElement = document.getElementById("reset-error-msg");

    resetErrorElement.innerHTML = "";

    if (newPassword.length < 8) {
        resetErrorElement.innerHTML = "Password baru harus minimal 8 karakter.";
        return false;
    }

    const upperCaseRegex = /[A-Z]/;
    const specialCharRegex = /[_!@#$%^&*(),.?":{}|<>]/; 
    if (!upperCaseRegex.test(newPassword) || !specialCharRegex.test(newPassword)) {
        resetErrorElement.innerHTML = "Password harus mengandung minimal 1 huruf besar dan 1 karakter unik.";
        return false;
    }

    if (newPassword !== confirmPassword) {
        resetErrorElement.innerHTML = "Password baru dan konfirmasi password harus sama.";
        return false;
    }

    fetch('/reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: resetUsername,
            new_password: newPassword
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            hideResetPassword();
        } else {
            resetErrorElement.innerHTML = data.message;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        resetErrorElement.innerHTML = "Terjadi kesalahan. Silakan coba lagi.";
    });

    return false;
}