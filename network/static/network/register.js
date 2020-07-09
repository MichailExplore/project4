document.addEventListener('DOMContentLoaded', () => {
    manage_register_button();
});

// Function to manage log in button
function manage_register_button() {
    const but = document.querySelector('#register-button');
    const first_name_input = document.querySelector('#first-name-input');
    const last_name_input = document.querySelector('#last-name-input');
    const email_input = document.querySelector('#email-input');
    const password_input = document.querySelector('#password-input');
    const confirmation_input = document.querySelector('#confirmation-input');

    but.disabled = true;
    confirmation_input.onkeyup = () => {
        if (first_name_input.value.length > 0
            && last_name_input.value.length > 0
            && email_input.value.length > 0
            && password_input.value.length > 0
            && confirmation_input.value.length > 0)
            but.disabled = false;
        else
            but.disabled = true;
    };
};
