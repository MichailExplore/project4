document.addEventListener("DOMContentLoaded", () => {
    get_posts();
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
// Function to add post
function add_post(content) {
    const post_template = Handlebars.compile(document.querySelector('#post-template').innerHTML);
    const post = post_template({'first_name': content['user__first_name'],
                                'last_name': content['user__last_name'],
                                'message': content['message'],
                                'date': content['date'],
                                'time': content['time'],
                                'avatar': content['user__avatar']});
    console.log(content['user__first_name']);
    document.querySelector('#posts').innerHTML += post;
};
