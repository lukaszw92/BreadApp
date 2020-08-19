let button = document.querySelector(".next")
let fields = document.querySelector(".fields")
let form = document.querySelector("form")
let submit = document.querySelector(".submit")

function next_flour(event) {
    let new_flour = fields.cloneNode(true)
    form.appendChild(new_flour)
    submit.remove()
    form.appendChild(submit)


}
button.addEventListener('click', next_flour)