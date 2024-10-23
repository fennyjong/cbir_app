// Fungsi untuk memvalidasi form login
function validateForm() {
    const usernameOrEmail = document.forms["loginForm"]["username_or_email"].value.trim();
    const password = document.forms["loginForm"]["password"].value;
    const errorElement = document.getElementById("error-msg");

    // Menghapus pesan error sebelumnya
    errorElement.innerHTML = "";

    // Validasi username atau email
    if (!usernameOrEmail) {
        errorElement.innerHTML = "Username atau Email harus diisi.";
        return false;
    }
    
    // Validasi username
    const usernameRegex = /^[a-zA-Z0-9]+$/;
    const isEmail = usernameOrEmail.includes('@');
    if (!isEmail && !usernameRegex.test(usernameOrEmail)) {
        errorElement.innerHTML = "Username hanya boleh mengandung huruf dan angka.";
        return false;
    }
    
    // Validasi password
    if (!password) {
        errorElement.innerHTML = "Password harus diisi.";
        return false;
    }

    // Cek untuk admin
    if (usernameOrEmail === "admin" && password === "admin") {
        return true; // Admin login is valid
    }

    // Validasi panjang password untuk pengguna biasa (tidak admin)
    if (!isEmail && password.length < 8) {
        errorElement.innerHTML = "Password harus minimal 8 karakter.";
        return false;
    }

    return true; // Form valid
}

// Fungsi untuk menampilkan form reset password
function showResetPassword() {
    document.getElementById("resetPasswordForm").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

// Fungsi untuk menyembunyikan form reset password
function hideResetPassword() {
    document.getElementById("resetPasswordForm").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

// Fungsi untuk toggle visibilitas password
function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    const iconElement = icon.querySelector('i');

    if (input.type === "password") {
        input.type = "text";
        iconElement.classList.replace('fa-lock', 'fa-lock-open');
    } else {
        input.type = "password";
        iconElement.classList.replace('fa-lock-open', 'fa-lock');
    }
}

// Fungsi untuk memvalidasi form reset password
function validateResetForm() {
    const resetUsernameOrEmail = document.getElementById("resetUsernameOrEmail").value.trim(); // Updated to include username or email
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const resetErrorElement = document.getElementById("reset-error-msg");

    // Menghapus pesan error sebelumnya
    resetErrorElement.innerHTML = "";

    // Validasi password baru
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

    // Validasi konfirmasi password
    if (newPassword !== confirmPassword) {
        resetErrorElement.innerHTML = "Password baru dan konfirmasi password harus sama.";
        return false;
    }

    // Mengirim data reset password ke server
    fetch('/reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username_or_email: resetUsernameOrEmail, // Update to send the combined input
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

    return false; // Mencegah form submit secara default
}
