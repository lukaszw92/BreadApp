let button = document.querySelector(".next")
let fields = document.querySelector(".fields")
let form = document.querySelector("form")
let submit = document.querySelector(".submit")
let del = document.querySelector(".delete")


function next_flour(event) {
    event.preventDefault()
    let new_flour = fields.cloneNode(true)
    form.appendChild(new_flour)
    submit.remove()
    form.appendChild(submit)
}

function delete_last(event){
    event.preventDefault()
    let last = submit.previousElementSibling
    last.remove()
}

button.addEventListener('click', next_flour)

del.addEventListener('click', delete_last)
