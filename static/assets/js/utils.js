function attachFormSpinner(formSelector, buttonSelector, spinnerSelector) {
    const form = document.querySelector(formSelector);
    const button = document.querySelector(buttonSelector);
    const spinner = button.querySelector(spinnerSelector);

    if (form && button && spinner) {
        form.addEventListener("submit", function () {
            spinner.classList.remove("d-none");
            button.disabled = true;
        });
    }
}


document.addEventListener("DOMContentLoaded", function () {
    attachFormSpinner("#myform", "#submitbtn", ".spinner-border");
});