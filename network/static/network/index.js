document.addEventListener('DOMContentLoaded', () => {
    manage_post_button();
    add_posts('all');

    const create_post_form = document.querySelector('#create-post-form');
    create_post_form.onsubmit = () => {
        add_loading_spinner();

        const request = new XMLHttpRequest();
        request.open('POST', '/api/create-post');
        request.onload = () => {
            const status = request.status;
            if (status === 200) {
                add_posts('all');
                document.querySelector('#post-input').value = '';
                manage_post_button();
            };
        };
        const data = new FormData(create_post_form);
        request.send(data);

        return false;
    };
});

document.addEventListener('click', event => {
    var element = event.target;
    if (element.classList.contains('fa'))
        element = event.target.parentElement;

    const parent = element.parentElement;
    const outer_parent = parent.parentElement;

    if (element.classList.contains('like-button')) {
        const post_id = outer_parent.id;
        const sentiment = 1;
        update_emotion(sentiment, post_id, parent);
    };
    if (element.classList.contains('dislike-button')) {
        const post_id = outer_parent.id;
        const sentiment = 2;
        update_emotion(sentiment, post_id, parent);
    };

    if (element.classList.contains('edit-post-button')) {
        const post_id = outer_parent.parentElement.parentElement.parentElement.id;

        const request = new XMLHttpRequest();
        request.open('GET', `/api/get-post/${post_id}`);
        request.onload = () => {
            const data = JSON.parse(request.responseText);

            const edit_post_template = Handlebars.compile(document.querySelector('#edit-post-template').innerHTML);
            const edit_post = edit_post_template(data[0]);
            document.querySelector('#message-'.concat(post_id)).innerHTML = edit_post;

            const edit_post_buttons_template = Handlebars.compile(document.querySelector('#edit-post-buttons-template').innerHTML);
            const edit_post_buttons = edit_post_buttons_template();
            document.querySelector('#edit-post-button-'.concat(post_id)).innerHTML = edit_post_buttons;
        };
        request.send();
    };

    if (element.classList.contains('delete-button')) {
        const eldest_parent = outer_parent.parentElement.parentElement.parentElement;
        const post_id = eldest_parent.id;

        const request = new XMLHttpRequest();
        request.open('GET', `/api/delete-post/${post_id}`)
        request.onload = () => {
            const status_code = request.status;
            if (status_code === 200) {
                eldest_parent.style.animationPlayState = 'running';
                eldest_parent.addEventListener('animationend', () => {
                    outer_parent.parentElement.parentElement.parentElement.remove();
                });
            };
        };
        request.send();
    };

    if (element.classList.contains('update-button')) {
        const eldest_parent = outer_parent.parentElement;
        const post_id = eldest_parent.id;

        const request = new XMLHttpRequest();
        request.open('POST', `/api/update-post/${post_id}`);
        request.onload = () => {
            console.log(request.status);
        };

        let formData = document.querySelector('#update-post-'.concat(post_id));
        const data = new FormData(formData);
        request.send(data);

        return false;
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
};

// Function to update buttons
function update_buttons(content, parent) {
    const buttons_template = Handlebars.compile(document.querySelector('#buttons-template').innerHTML);
    const buttons = buttons_template(content);
    parent.innerHTML = buttons;
};

// Function to manage post button
function manage_post_button() {
    const but = document.querySelector('#post-button');
    const input = document.querySelector('#post-input');

    but.disabled = true;
    input.onkeyup = () => {
        if (input.value.length > 0)
            but.disabled = false;
        else
            but.disabled = true;
    };
};

// Function to add all posts
function add_posts() {
    document.querySelector('#posts').innerHTML = '';
    add_loading_spinner();

    const request = new XMLHttpRequest();
    request.open('GET', '/api/get-posts/all')
    request.onload = () => {
        document.querySelector('#posts').innerHTML = '';

        const data = JSON.parse(request.responseText);
        data.forEach(add_post);
    };
    request.send();

};

// Function to add loading spinner
function add_loading_spinner() {
    let loading_spinner_template = document.querySelector('#loading-spinner-template');
    loading_spinner_template = Handlebars.compile(loading_spinner_template.innerHTML);
    const loading_spinner = loading_spinner_template();
    document.querySelector('#posts').innerHTML = loading_spinner;
};

// Function to add post
function add_post(content) {
    let post_component_template = document.querySelector('#post-component-template');
    post_component_template = Handlebars.compile(post_component_template.innerHTML);
    const post_component = post_component_template(content);
    document.querySelector('#posts').innerHTML = post_component + document.querySelector('#posts').innerHTML;
}
