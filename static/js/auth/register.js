// Fungsi untuk memvalidasi form login
function validateForm() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const errorElement = document.getElementById("error-msg");

    // Menghapus pesan error sebelumnya
    errorElement.innerHTML = "";

    // Validasi username
    const usernamePattern = /^[a-zA-Z0-9]+$/; // Pola untuk username
    if (!usernamePattern.test(username)) {
        errorElement.innerHTML = "Username tidak boleh mengandung karakter khusus.";
        return false; // Menghentikan eksekusi jika validasi gagal
    }

    // Validasi password
    if (password.length < 8) {
        errorElement.innerHTML = "Password harus lebih dari 8 karakter.";
        return false;
    }

    const uppercasePattern = /[A-Z]/; // Pola untuk huruf besar
    const specialCharPattern = /[_!@#$%^&*(),.?":{}|<>]/; // Pola untuk karakter unik
    if (!uppercasePattern.test(password) || !specialCharPattern.test(password)) {
        errorElement.innerHTML = "Password harus mengandung setidaknya satu huruf besar dan satu karakter unik.";
        return false;
    }

    return true; // Form valid
}

// Fungsi untuk toggle visibilitas password
function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    const iconElement = icon.querySelector('i');

    // Mengubah tipe input dan ikon sesuai dengan status visibilitas
    if (input.type === "password") {
        input.type = "text"; // Menampilkan password
        iconElement.classList.replace('fa-lock', 'fa-lock-open'); // Mengubah ikon
    } else {
        input.type = "password"; // Menyembunyikan password
        iconElement.classList.replace('fa-lock-open', 'fa-lock'); // Mengubah ikon kembali
    }
}
