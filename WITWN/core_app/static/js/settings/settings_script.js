const mainInfoBox = document.querySelector(".self-info-editbox")
const inputBoxList = document.querySelectorAll(".input-box")
const mainInfoInputs = []
const initialValues = []
let formOn = false
const closedEyeURL = document.querySelector("#URLs").value
const openEyeURL = document.querySelector("#URLs").name
for (let inputBox of inputBoxList){
    mainInfoInputs.push(inputBox.querySelector("input"))
    initialValues.push(inputBox.querySelector("input").value)
    inputBox.querySelector("input").disabled = true
}

document.querySelectorAll(".show-password").forEach((button) => {
    button.addEventListener("click", () => {
        if (formOn){
            if (button.id == "hidden"){
                button.id = 'show'
                button.parentElement.querySelector("input").type = "text"
                button.src = openEyeURL
            }
            else{
                button.id = "hidden"
                button.parentElement.querySelector("input").type = "password"
                button.src = closedEyeURL
            }
        }
    })
})

const buttonOpenEdit = document.querySelector(".settings-open-editing")
const buttonCloseEdit = document.querySelector(".settings-cancel-button")
const buttonSubmitEdit = document.querySelector(".settings-save-button")
const mainInfoInputArea = document.querySelector(".self-info-editbox")

buttonOpenEdit.addEventListener("click", () => {
    buttonOpenEdit.classList.add("hidden")
    buttonCloseEdit.classList.remove("hidden")
    buttonSubmitEdit.classList.remove("hidden")
    formOn = true
    mainInfoInputs.forEach((input) => {input.disabled = false})
    mainInfoInputArea.classList.remove("half-visible")
    for (let eye of document.querySelectorAll(".non-interactive")){
        eye.classList.replace("non-interactive", "interactive")
        console.log(eye)
    }
})

buttonCloseEdit.addEventListener("click", () => {
    buttonOpenEdit.classList.remove("hidden")
    buttonCloseEdit.classList.add("hidden")
    buttonSubmitEdit.classList.add("hidden")
    formOn = true
    for (let inputIndex = 0; inputIndex < mainInfoInputs.length; inputIndex++){
        let input = mainInfoInputs[inputIndex]
        input.value = initialValues[inputIndex]
        input.disabled = true
    }
    mainInfoInputArea.classList.add("half-visible")
    for (let eye of document.querySelectorAll(".interactive")){
        eye.classList.replace("interactive", "non-interactive")
    }
    mainInfoInputArea.querySelector("[name='password']").type = "password"
})