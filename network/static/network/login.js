document.addEventListener('DOMContentLoaded', () => {
    manage_login_button();
});

// Function to manage log in button
function manage_login_button() {
    const but = document.querySelector('#log-in-button');
    const email_input = document.querySelector('#email-input');
    const password_input = document.querySelector('#password-input');

    but.disabled = true;
    password_input.onkeyup = () => {
        if (email_input.value.length > 0 && password_input.value.length > 0)
            but.disabled = false;
        else
            but.disabled = true;
    };
};
