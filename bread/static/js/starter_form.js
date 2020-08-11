let button = document.querySelector("#next")
let form = document.querySelector("#leaven_form")

console.log(form.firstElementChild)


function next_flour(event) {
    let new_flour = form.firstElementChild.cloneNode(true)
    form.appendChild(new_flour)


}

button.addEventListener('click', next_flour)


