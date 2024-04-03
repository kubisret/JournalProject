$(document).ready(function () {
    $("#label-password-reset").keyup(function () {
        var password = $("#label-password-reset").val();

        let strength = check(password);
        let color = getColor(strength);

        document.getElementById('progressBar').style.width = strength + '%';
        document.getElementById('progressBar').classList = "progress-bar progress-bar-striped " + color;

    });

    function check(password) {
        let strength = 0;

        // Проверяем длину пароля
        if (password.length < 8) {
            return 0;
        }

        // Проверяем наличие цифр
        if (/\d/.test(password)) {
            strength += 25;
        }

        // Проверяем наличие букв верхнего регистра
        if (/[A-Z]/.test(password)) {
            strength += 25;
        }

        // Проверяем наличие букв нижнего регистра
        if (/[a-z]/.test(password)) {
            strength += 25;
        }

        // Проверяем наличие специальных символов
        if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
            strength += 25;
        }

        return strength;
    }

    function getColor(strength) {
            if (strength >= 75) {
                return "bg-success";
            } else if (strength >= 50) {
                return "bg-warning";
            } else {
                return "bg-danger";
            }
        }

});