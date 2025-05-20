// Password eye button

const FORM = document.querySelector(".reg-form");
const PASSWORD_FIELD = document.querySelector("#id_password1");
const PASSWORD_CONFIRM_FIELD = document.querySelector("#id_password2");
const ICON_LINKS_INPUT = document.querySelector("#iconLinks");
const ICON_LINKS = {"show": ICON_LINKS_INPUT.name, "close": ICON_LINKS_INPUT.value}

document.querySelectorAll(".look").forEach((element) => {
    console.log("Adding button " + element.id)
    element.addEventListener("mousedown", () => {
        document.querySelector(`#${element.id.split("-")[0]}`).type = "text"
        element.src = ICON_LINKS["show"]
    })
    element.addEventListener("mouseup", () => {
        document.querySelector(`#${element.id.split("-")[0]}`).type = "password"
        element.src = ICON_LINKS["close"]
    })
})

// Submit button logic


const EMAIL_FIELD = document.querySelector("#id_email")
const NEXT_BUTTON = document.querySelector(".next-button")
const ALL_FIELDS = [EMAIL_FIELD, PASSWORD_FIELD, PASSWORD_CONFIRM_FIELD]

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
    if (PASSWORD_CONFIRM_FIELD.value != PASSWORD_FIELD.value){
        can = false
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

const START_DATA = document.querySelector("#startData").value
if (START_DATA!="&"){
    EMAIL_FIELD.value = START_DATA.split("&")[1]
}