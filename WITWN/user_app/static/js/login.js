// Password eye button

const FORM = document.querySelector(".reg-form");
const PASSWORD_FIELD = document.querySelector("#id_password");
const ERROR_TEXT = document.querySelector(".error-text");
const ICON_LINKS_INPUT = document.querySelector("#iconLinks");
const ICON_LINKS = {"show": ICON_LINKS_INPUT.name, "close": ICON_LINKS_INPUT.value}

document.querySelectorAll(".look").forEach((element) => {
    console.log("Adding button " + element.id)
    element.addEventListener("mousedown", () => {
        document.querySelector(`#${element.id.split("-")[0]}`).type = "text"
        element.querySelector("img").src = ICON_LINKS["show"]
    })
    element.addEventListener("mouseup", () => {
        document.querySelector(`#${element.id.split("-")[0]}`).type = "password"
        element.querySelector("img").src = ICON_LINKS["close"]
    })
})

// Submit button logic


const USERNAME_FIELD = document.querySelector("#id_username")
const NEXT_BUTTON = document.querySelector(".login-button")
const ALL_FIELDS = [USERNAME_FIELD, PASSWORD_FIELD]

function validateField(field){
    if (4 > field.value.length || 256 < field.value.length){
        return false
    }
    return true
}

function validate(){
    let can = true
    for (let field of ALL_FIELDS){
        if (!validateField(field)){
            can = false
            break
        } 
    }
    return can
}

ALL_FIELDS.forEach((field) => {
    field.addEventListener('input', (event) => {
        console.log(validate())
        if (validate()){
            NEXT_BUTTON.disabled = false
        }
        else{
            NEXT_BUTTON.disabled = true
        }
    })
})