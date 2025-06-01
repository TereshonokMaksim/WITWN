const FORM = document.querySelector(".reg-form");
const CODE_FIELDS = [];
console.log("start")
for (let i = 1; i < 7; i++){
    console.log(i)
    CODE_FIELDS.push(document.querySelector(`#id_symbol${i}`))
}
let numbers = []
for (let i = 0; i < 10; i++) {
    numbers.push(String(i))
}
const NEXT_BUTTON = document.querySelector(".next-button")

console.log(CODE_FIELDS)

CODE_FIELDS.forEach((inputField) => {
    inputField.addEventListener("keydown", (event) => {
        let curIndex = CODE_FIELDS.indexOf(inputField)
        if (event.key == "Backspace"){
            if (inputField.value.length == 0){
                if (curIndex > 0){
                    CODE_FIELDS[curIndex - 1].focus()
                    CODE_FIELDS[curIndex - 1].setSelectionRange(1, 1)
                }
            }
        }
        passValidation()
    })
    inputField.addEventListener("input", (event) => {
        let curIndex = CODE_FIELDS.indexOf(inputField)
        if (inputField.value.length != 0) {
            if (!numbers.includes(inputField.value)){
                inputField.value = ""
            }
            else if (curIndex < CODE_FIELDS.length - 1){
                CODE_FIELDS[curIndex + 1].focus()
            }
        }
        passValidation()
})})

function validateField(field){
    if (field.value.length != 1){
        console.log(`error at ${field.id} field`)
        return false
    }
    return true
}

function validate(){
    let can = true
    for (let field of CODE_FIELDS){
        if (!validateField(field)){
            can = false
            break
        } 
    }
    return can
}

function passValidation(){
    if (validate()){
        NEXT_BUTTON.disabled = false
    }
    else{
        NEXT_BUTTON.disabled = true
    }
}

passValidation()

// CODE_FIELDS.forEach((field) => {
//     field.addEventListener('input', (event) => {
//         if (validate()){
//             NEXT_BUTTON.disabled = false
//         }
//         else{
//             NEXT_BUTTON.disabled = true
//         }
//     })
// })