$(document).ready(function () {
    $("#label-password-register").keyup(function () {
        var pass = $("#label-password-register").val();
        $("#result").text(pass);
    });
});