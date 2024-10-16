function validateForm() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const errorElement = document.getElementById("error-msg");
    
    errorElement.innerHTML = "";
    
    const usernamePattern = /^[a-zA-Z0-9]+$/;
    if (!usernamePattern.test(username)) {
        errorElement.innerHTML = "Username tidak boleh mengandung karakter khusus.";
        return false;
    }
    
    if (password.length < 8) {
        errorElement.innerHTML = "Password harus lebih dari 8 karakter.";
        return false;
    }
    
    const uppercasePattern = /[A-Z]/;
    const specialCharPattern = /[_!@#$%^&*(),.?":{}|<>]/;
    if (!uppercasePattern.test(password) || !specialCharPattern.test(password)) {
        errorElement.innerHTML = "Password harus mengandung setidaknya satu huruf besar dan satu karakter unik.";
        return false;
    }
    
    return true;
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