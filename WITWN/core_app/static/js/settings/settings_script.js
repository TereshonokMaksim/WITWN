const mainInfoBox = document.querySelector(".self-info-editbox")
const inputBoxList = mainInfoBox.querySelectorAll(".input-box")
const mainInfoInputs = []
const initialValues = []
const changePasswordLink = document.querySelector("#changePasswordLink").value
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

// avatar

const showHeadSettings = document.querySelector(".header-readonly")
const editHeadSettings = document.querySelector(".header-edit")

const openEditHeader = document.querySelector(".settings-edit-header")
const cancelEditHeader = document.querySelector("#headerEditCancel")
const saveEditHeader = document.querySelector("#headerEditSend")
const realAvatarImage = showHeadSettings.querySelector(".prof-pic")
const realUsername = showHeadSettings.querySelector(".self-username")
const mainInfoLink = document.querySelector("#mainInfoLink").value
let avatarChanged = false

openEditHeader.addEventListener("click", () => {
    showHeadSettings.classList.add("hidden")
    editHeadSettings.classList.remove("hidden")
    openEditHeader.classList.add("hidden")
    cancelEditHeader.classList.remove("hidden")
    saveEditHeader.classList.remove("hidden")
})

function closeEditingHeader(){
    showHeadSettings.classList.remove("hidden")
    editHeadSettings.classList.add("hidden")
    openEditHeader.classList.remove("hidden")
    cancelEditHeader.classList.add("hidden")
    saveEditHeader.classList.add("hidden")
    previewUsernameInput.placeholder = realUsername.innerHTML
    previewAvatarImage.src = realAvatarImage.src
    avatarChanged = false
}

function sendData(){
    let dataForm = new FormData(editHeadSettings)
    dataForm.append("change_photo", avatarChanged)
    postData(mainInfoLink, dataForm).then((data) => {
        realUsername.innerHTML = data["username"]
        previewUsernameInput.placeholder = data["username"]
        realAvatarImage.src = previewAvatarImage.src
        closeEditingHeader()
        previewUsernameInput.value = ""
    })
}

cancelEditHeader.addEventListener("click", closeEditingHeader)
saveEditHeader.addEventListener("click", sendData)

const avatarInput = document.querySelector("#newAvatarDownload")
const avatarDownloadButton = document.querySelector("#avatarEditAdd")
const previewAvatarImage = editHeadSettings.querySelector(".prof-pic")
const previewUsernameInput = editHeadSettings.querySelector(".username-input")

avatarDownloadButton.addEventListener("click", () => {
    avatarInput.click()
})

avatarInput.addEventListener("input", () => {
    previewAvatarImage.src = URL.createObjectURL(avatarInput.files[0])
    avatarChanged = true
})

async function postData(url, formData) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
        'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    });
    return response.json()
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}

// passwords

const passwordButtonBlock = document.querySelector(".password-header").querySelector(".settings-edit-options")
const mainPasswordBlock = document.querySelector(".password-editbox")
const openPassword = passwordButtonBlock.querySelector(".password-open-button")
const cancelPassword = passwordButtonBlock.querySelector(".password-cancel-button")
const savePassword = passwordButtonBlock.querySelector(".password-save-button")
const showPasswordBox = document.querySelector(".password-box-show")
const editPasswordBox = document.querySelector(".password-box-edit")
const mainPasswordInput = document.querySelector("#mainPassword")
const confirmPasswordInput = document.querySelector("#additionalPassword")
const badPasswordText = editPasswordBox.querySelector(".errortext")

openPassword.addEventListener('click', () => {
    openPassword.classList.add("hidden")
    cancelPassword.classList.remove("hidden")
    savePassword.classList.remove("hidden")
    showPasswordBox.classList.add("hidden")
    editPasswordBox.classList.remove("hidden")
    mainPasswordBlock.classList.remove("half-visible")
})

function closePasswordEditing(){
    cancelPassword.classList.add("hidden")
    savePassword.classList.add("hidden")
    openPassword.classList.remove("hidden")
    mainPasswordInput.value = ""
    confirmPasswordInput.value = ""
    badPasswordText.classList.add("hidden")
    showPasswordBox.classList.remove("hidden")
    editPasswordBox.classList.add("hidden")
    mainPasswordBlock.classList.add("half-visible")
}

cancelPassword.addEventListener("click", closePasswordEditing)
savePassword.addEventListener("click", () => {
    if (mainPasswordInput.value.length > 6){
        if (mainPasswordInput.value == confirmPasswordInput.value){
            const passwordFormData = new FormData()
            passwordFormData.append("password", mainPasswordInput.value)
            postData(changePasswordLink, passwordFormData).then(() => {console.log("Successfull password change")})
            closePasswordEditing()
        }
        else {
            badPasswordText.classList.remove("hidden")
        }
    }
})