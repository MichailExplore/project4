document.addEventListener("DOMContentLoaded", () => {
    get_posts();
    manage_post_button();
});

// Function to fetch existing posts
function get_posts() {
    const request = new XMLHttpRequest();
    request.open('GET', '/api/get-posts');
    request.onload = () => {
        if (request.status !== 200)
            console.log('Could not load posts')
        const data = JSON.parse(request.responseText);
        data.forEach(content => {
            add_post(content);
        });
    };
    request.send();
};

// Function to add post to DOM
function add_post(content) {
    const post_template = Handlebars.compile(document.querySelector('#post-template').innerHTML);
    // This feels silly: should not have to type out key-value pairs
    const post = post_template({'first_name': content['user__first_name'],
                                'last_name': content['user__last_name'],
                                'message': content['message'],
                                'date': content['date'],
                                'time': content['time'],
                                'likes': content['likes'],
                                'own_post': content['own_post'],
                                'dislikes': content['dislikes'],
                                'avatar': content['user__avatar']});
    document.querySelector('#posts').innerHTML += post;
};

Handlebars.registerHelper('if_eq', function(a, b, opts) {
    if (a == b)
        return opts.fn(this);
});

// Function to create post in DB
// function create_post(message) {
//     const request = new XMLHttpRequest();
//     request.open('POST', '/api/create-post');
//     request.onload() => {
//
//     }
//
//     const data = new FormData();
//     data.append('message', message);
//     request.send(data);
// }


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
