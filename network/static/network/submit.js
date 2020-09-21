document.addEventListener('DOMContentLoaded', () => {
  manage_submit_button();
  add_loading_spinner();
});

// Function to manage submit button
function manage_submit_button() {
  const but = document.querySelector('#submit-button');
  const inputs = document.querySelectorAll('.input');

  but.disabled = true;
  for (var i = 0; i < inputs.length; i++) {
    inputs[i].onkeyup = () => {
      let length_status = true;
      for (var j = 0; j < inputs.length; j++) {
        if (inputs[j].value.length === 0) {
          length_status = false;
        };
      };

      if (length_status === true) {
        but.disabled = false;
      } else {
        but.disabled = true;
      }
    };
  };
};

// Function to add loading spinner
function add_loading_spinner() {
  const but = document.querySelector('#submit-button');
  const f = document.querySelector('form');

  f.onsubmit = () => {
    let submit_ls_but_template = document.querySelector('#submit-ls-but-template');
    submit_ls_but_template = Handlebars.compile(submit_ls_but_template.innerHTML);
    const submit_ls_but = submit_ls_but_template();
    but.innerHTML = submit_ls_but;
  }
};
