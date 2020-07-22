document.addEventListener('DOMContentLoaded', () => {
    manage_post_button();

});

document.addEventListener('click', event => {
    var element = event.target;
    if (element.classList.contains('emoji'))
        element = event.target.parentElement;

    const post_id = element.parentElement.id;
    const parent = element.parentElement;
    if (element.classList.contains('like-button')) {
        const sentiment = 1;
        update_emotion(sentiment, post_id, parent);
    };
    if (element.classList.contains('dislike-button')) {
        const sentiment = 2;
        update_emotion(sentiment, post_id, parent);
    };
});

// Function to update Emotion model
function update_emotion(sentiment, post_id, parent) {
    const request = new XMLHttpRequest();
    request.open('GET', `/api/adjust-emotion/${sentiment}/${post_id}`);
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        update_buttons(data[0], parent);
    };
    request.send();
}

// Function to update buttons
function update_buttons(content, parent) {
    const buttons_template = Handlebars.compile(document.querySelector('#buttons-template').innerHTML);
    const buttons = buttons_template(content);
    parent.innerHTML = buttons;
};

// Function to manage post button
function manage_post_button() {
    const but = document.querySelector('#post-button')
    const input = document.querySelector('#post-input')

    but.disabled = true;
    input.onkeyup = () => {
        if (input.value.length > 0)
            but.disabled = false;
        else
            but.disabled = true;
    }
}
