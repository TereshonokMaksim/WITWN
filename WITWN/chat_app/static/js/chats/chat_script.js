let connection = null
let selfAdmin = false
let personalChat = false

function processMessageTime(text){
    let date = new Date(text)
    console.log(date, date.toLocaleString())
    let dateText = `${date.getHours()}:${date.getMinutes()}`
    return dateText
}

document.querySelectorAll(".time-message").forEach((obj) => {
    let correctTime = processMessageTime(obj.textContent)
    obj.textContent = correctTime
})

const noChatText = document.querySelector(".chat-p-div")
const chatBox = document.querySelector(".chat-selected-box")
const messages = document.querySelector(".chat-messages")
const checkmarkSrc = document.querySelector("#checkmarkURL").value
const messageTextInput = document.querySelector(".chat-main-input");
const messageForm = document.querySelector(".chat-send-options");
const newImageReader = new FileReader()

function addMessage(message){
    if (document.querySelector(".message-box") != null){
        // console.log(document.querySelector(".message-box"))
        messages.insertBefore(message, document.querySelector(".message-box"))
    }
    else{
        messages.appendChild(message)
    }
    message.scrollTop = 0
}

function makeConnection(groupId, personal = true){
    let id = ""
    personalChat = personal
    if (personal){
        id = `${document.querySelector("#selfID").value}-${groupId}`
    }
    else {
        id = `${groupId}`
    }
    let SOCKET_URL = `ws://${window.location.host}/chat/${id}&${personal}`
    connection = new WebSocket(SOCKET_URL)
    // console.log(id, personal)

    connection.addEventListener("open",() => {
        connection.addEventListener("message", (event) => {
            let data = JSON.parse(event.data);
            console.log(data)
            if (data.type == "chatting"){
                let messageClass = ""
                if (data.sender != " "){
                    messageClass = "friend-message"
                }
                else{
                    messageClass = "self-message"
                }
                let timeText = processMessageTime(data.datetime)
                let newMessage = document.createElement("div")
                // new part - images
                let imageMessage = document.createElement("img")
                if (data.image != "0"){
                    imageMessage.src = data.image
                    imageMessage.classList.add("message-image")
                }
                else{
                    imageMessage.classList.add("hidden")
                }
                newMessage.classList.add("message-box")
                let messageDiv = document.createElement("div"); messageDiv.classList.add(messageClass, "message")
                messageDiv.innerHTML = `<div class = "message-text"><div class = "message-main-info"><p class = "message-sender">${data.sender}</p><p class = "message-content">${data.message}</p></div><div class = "message-add-info"><p class = "data-time">${timeText}</p><img class = "checkmark-img" src = ${checkmarkSrc}></div></div>`;
                messageDiv.appendChild(imageMessage)
                newMessage.appendChild(messageDiv)
                addMessage(newMessage)
            }
            else if (data.type == "load"){
                selfAdmin = data.self_admin
                for (let message of data.message_data){
                    let messageClass = ""
                    let username = " "
                    console.log(message)
                    if (message.sender != " "){
                        messageClass = "friend-message"
                        username = message.sender
                        console.log("friends")
                    }
                    else{
                        messageClass = "self-message"
                    }
                    // new part - images
                    let imageMessage = document.createElement("img")
                    if (message.image != "0"){
                        imageMessage.src = message.image
                        imageMessage.classList.add("message-image")
                    }
                    else{
                        imageMessage.classList.add("hidden")
                    }
                    let timeText = processMessageTime(message.datetime)
                    let newMessage = document.createElement("div")
                    newMessage.classList.add("message-box")
                    let messageDiv = document.createElement("div"); messageDiv.classList.add(messageClass, "message")
                    messageDiv.innerHTML = `<div class = "message-text"><div class = "message-main-info"><p class = "message-sender">${message.sender}</p><p class = "message-content">${message.message}</p></div><div class = "message-add-info"><p class = "data-time">${timeText}</p><img class = "checkmark-img" src = ${checkmarkSrc}></div></div>`;
                    messageDiv.appendChild(imageMessage)
                    newMessage.appendChild(messageDiv)
                    addMessage(newMessage)
                }
            }
            else if (data.type == "quit_report"){
                if (data.success){
                    let chat = document.querySelector(".selected-chat")
                    if (!chat.classList.contains("single-contact-div")){
                        console.log("Deleted, no?", chat)
                        chat.remove()
                    }
                    closeChat()
                }
            }
        })

        let JSONString = JSON.stringify({"request": "load"});
        connection.send(JSONString);
    })
}


messageForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendWebsocketMessage()
})
document.querySelector(".message-send").addEventListener("click", sendWebsocketMessage)

function sendWebsocketMessage(){
    if (messageImageInput.files.length > 0){
        newImageReader.onload = (event) => {
            let imageData = arrayBufferToBase64(event.target.result)
            sendMessage(imageData)
            messageImageInput.value = ""
            imagePreviewBox.classList.add("hidden")
        }
        newImageReader.readAsArrayBuffer(messageImageInput.files[0])
    }
    else{
        sendMessage(0)
    }
}

function sendMessage(byteData){
    let message = messageTextInput.value;
    if (message != "" && message != " " && message != null){
        let dataToSend = {"message": message, "image": byteData, "request": "message"};
        let JSONString = JSON.stringify(dataToSend);
        connection.send(JSONString);
        messageForm.reset()
    }
    else{
        messageTextInput.classList.add("errorlight")
    }
}

messageTextInput.addEventListener("input", () => {
    messageTextInput.classList.remove("errorlight")
})

let chatAvatar = document.querySelector(".chat-avatar")
let chatName = document.querySelector(".chat-name")
let chatMembersOnline = document.querySelector(".chat-members-online")

document.querySelectorAll(".friend-chat").forEach(obj => {
    obj.addEventListener("click", () => {
        if (connection != null){
            connection.close()
        }
        document.querySelector(".chat-messages").innerHTML = ""
        makeConnection(obj.id, 1)
        if (document.querySelector(".selected-chat") != null){
            document.querySelector(".selected-chat").classList.remove("selected-chat")
        }
        obj.classList.add("selected-chat")
        noChatText.classList.add("hidden")
        chatBox.classList.remove("hidden")

        chatAvatar.src = obj.querySelector("img").src
        chatName.textContent = obj.querySelector(".contact-name-p").innerHTML
        getChatInfo()
        messageTextInput.focus()
    })
})

// !2

document.querySelectorAll(".group-chat").forEach(obj => {
    obj.addEventListener("click", () => {
        if (connection != null){
            connection.close()
        }
        document.querySelector(".chat-messages").innerHTML = ""
        makeConnection(obj.id, 0)
        if (document.querySelector(".selected-chat") != null){
            document.querySelector(".selected-chat").classList.remove("selected-chat")
        }
        obj.classList.add("selected-chat")
        noChatText.classList.add("hidden")
        chatBox.classList.remove("hidden")

        chatAvatar.src = obj.querySelector("img").src
        chatName.textContent = obj.querySelector(".contact-name-p").innerHTML
        getChatInfo()

        messageTextInput.focus()
    })
})

function closeChat(){
    if (connection != null){
        connection.close()
        connection = null
    }
    document.querySelector(".chat-messages").innerHTML = ""
        if (document.querySelector(".selected-chat") != null){
            document.querySelector(".selected-chat").classList.remove("selected-chat")
        }
    chatBox.classList.add("hidden")
    noChatText.classList.remove("hidden")
}

document.querySelector(".chat-back").addEventListener("click", closeChat)

function loadChat(chatId){
    
    // const messageTimes = document.querySelectorAll(".message-time")
    // for (let messageTime of messageTimes){
    //     let text = messageTime.textContent
    //     messageTime.textContent = processMessageTime(text)
    // }
}

let statusConnection = new WebSocket(`ws://${window.location.host}/status/`)

statusConnection.addEventListener("open", () => {
    console.log("status websocket opened")
})

const formBlur = document.querySelector(".blur")
const newGroupMembers = document.querySelector("#newGroupMembers")
const newGroupMemNum = document.querySelector("#newGroupMemNum")
const newGroupForm = document.querySelector("#createNewGroup")
const trashbinSrc = document.querySelector("#trashbinSrc").value
const createGroupMembers = document.querySelector('.create-group-members')
const groupCreationType = newGroupForm.querySelector("#groupCreationType")
const addNewMemberButton = newGroupForm.querySelector("#addMemberButton")

const createGroupButton = document.querySelector(".create-chat-button")
let choosedMembers = []

createGroupButton.addEventListener("click", () => {
    groupCreationType.name = "create"
    newGroupForm.querySelector(".new-group-p").textContent = "Нова група"
    newGroupForm.querySelector(".create-button").textContent = "Створити групу"
    formBlur.classList.remove("hidden")
    newGroupMembers.classList.remove("hidden")
    addNewMemberButton.classList.add("hidden")
    updateMemNum()
})

function updateMemNum(){
    newGroupMemNum.textContent = choosedMembers.length
    if (choosedMembers.length == 0){
        newGroupMembers.querySelector(".create-button").disabled = true
    }
    else {
        newGroupMembers.querySelector(".create-button").disabled = false
    }
}

let allCheckBoxes = newGroupMembers.querySelectorAll(".chekbox-input")

function clearMemberList(){
    choosedMembers = []
    newGroupForm.querySelector(".create-group-members").innerHTML = ""
    newGroupMembers.querySelectorAll("input").forEach(obj => {obj.checked = false})
    updateMemNum()
}

allCheckBoxes.forEach(obj => {
    obj.addEventListener("click", () => {
        let id = obj.parentNode.parentNode.id
        if (obj.checked) {
            choosedMembers.push(id)
            let member = newGroupMembers.querySelector(`[id='${id}']`).cloneNode(true)
            member.querySelector(".name-and-input-div").removeChild(member.querySelector(".chekbox-input"))
            let trashbinIcon = document.createElement("img")
            trashbinIcon.src = trashbinSrc
            trashbinIcon.classList.add("bin-img")
            member.querySelector(".name-and-input-div").appendChild(trashbinIcon)
            trashbinIcon.addEventListener("click", () => {
                choosedMembers.splice(choosedMembers.indexOf(trashbinIcon.parentNode.parentNode.id), 1)
                trashbinIcon.parentNode.parentNode.remove()
            })
            newGroupForm.querySelector(".create-group-members").appendChild(member)
        }
        else{
            choosedMembers.splice(choosedMembers.indexOf(id), 1)
            console.log(newGroupForm.querySelector(`[id='${id}']`))
            newGroupForm.querySelector(`[id='${id}']`).remove()
        }
        updateMemNum()
    })
})

newGroupMembers.querySelector(".decline-button").addEventListener("click", () => {
    for (let checkbox of allCheckBoxes){
        checkbox.checked = false
    }
    choosedMembers = []
    formBlur.classList.add("hidden")
    newGroupMembers.classList.add("hidden")
    clearMemberList()
})

newGroupMembers.querySelector(".cross-image").addEventListener("click", () => {
    for (let checkbox of allCheckBoxes){
        checkbox.checked = false
    }
    choosedMembers = []
    formBlur.classList.add("hidden")
    newGroupMembers.classList.add("hidden")
    clearMemberList()
})

newGroupMembers.querySelector(".create-button").addEventListener("click", () => {
    if (choosedMembers.length > 0){
        for (let checkbox of allCheckBoxes){
            checkbox.checked = false
        }
        newGroupMembers.classList.add("hidden")
        newGroupForm.classList.remove("hidden")
        // for (let id of choosedMembers){
        //     if (newGroupForm.querySelector(`[id='${id}']`) == null){
        //     }
        // }
    }
})

newGroupForm.querySelector(".decline-button").addEventListener("click", () => {
    newGroupForm.classList.add("hidden")
    newGroupMembers.classList.remove("hidden")
    for (let id of choosedMembers){
        newGroupMembers.querySelector(`[id='${id}']`).querySelector("input").checked = true
    }
    updateMemNum()
})

addNewMemberButton.addEventListener("click", () => {
    newGroupForm.classList.add("hidden")
    newGroupMembers.classList.remove("hidden")
    for (let id of choosedMembers){
        newGroupMembers.querySelector(`[id='${id}']`).querySelector("input").checked = true
    }
    updateMemNum()
})

// group avatar

const avatarInput = document.querySelector("#groupAvatarInput")
const avatarDownloadButton = document.querySelector("#addAvatarCreateGroup")
const previewAvatarImage = document.querySelector(".create-group-avatar")

avatarDownloadButton.addEventListener("click", () => {
    avatarInput.click()
})

avatarInput.addEventListener("input", () => {
    previewAvatarImage.src = URL.createObjectURL(avatarInput.files[0])
    avatarChanged = true
})

// group creation - sending

const groupCreateButton = newGroupForm.querySelector(".create-button")
const usernameInput = newGroupForm.querySelector(".group-name-input")
const reader = new FileReader()

function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

function handleData(data){
    avatarBinary = data
}

function sendGroupData(avatarToSend){
    let requestType = "groupCreation"
    if (groupCreationType.name == "edit"){
        requestType = "groupEditing"
    }
    let rawData = {"request_type": requestType, "name": usernameInput.value, "avatar": avatarToSend, "members": choosedMembers, "group_id": groupCreationType.value}
    let cookedData = JSON.stringify(rawData)
    console.log("Sending!", cookedData, rawData)
    statusConnection.send(cookedData)
    newGroupForm.classList.add("hidden")
    formBlur.classList.add("hidden")
    newGroupForm.querySelector(".create-group-members").innerHTML = ""
    avatarInput.value = ""
    usernameInput.value = ""
    clearMemberList()
}

groupCreateButton.addEventListener("click", () => {
    if (avatarInput.files.length > 0){
        let file = avatarInput.files[0]
        reader.readAsArrayBuffer(file)
        reader.onload = function (event) {
            const arrayBuffer = event.target.result
            let avatarToSend = arrayBufferToBase64(arrayBuffer)
            sendGroupData(avatarToSend)
        }
    }
    else{
        sendGroupData("0")
    }
})

// Message images!
// :)

const messageImageInput = document.querySelector("#uploadImageInput")
const addImageButton = document.querySelector(".message-img")
const imagePreviewBox = document.querySelector(".new-photo-box")
const imagePreview = imagePreviewBox.querySelector(".new-message-photo")
const deleteNewPhoto = imagePreviewBox.querySelector(".delete-new-photo")

addImageButton.addEventListener("click", () => {
    messageImageInput.click()
})

messageImageInput.addEventListener("input", () => {
    let fileURL = URL.createObjectURL(messageImageInput.files[0])
    imagePreview.src = fileURL
    imagePreviewBox.classList.remove("hidden")
})

deleteNewPhoto.addEventListener("click", () => {
    imagePreviewBox.classList.add("hidden")
    messageImageInput.value = ""
})

// Chat additional
// This part includes:
// 1. Chat editing
// 2. Leaving chat
// 3. All media (not neccessary - probably going to be skipped)

let tripleDot = document.querySelector(".chat-additional")
let personalChatDetails = document.querySelector("#personalChatDetail")
let memberGroupDetails = document.querySelector("#groupMemberDetail")
let adminGroupDetails = document.querySelector("#groupAdminDetail")

tripleDot.addEventListener("click", () => {
    if (personalChat){
        personalChatDetails.classList.remove("hidden")
    }
    else if (selfAdmin){
        adminGroupDetails.classList.remove("hidden")
    }
    else{
        memberGroupDetails.classList.remove("hidden")
    }
})

document.addEventListener("click", (event) => {
    if (![personalChatDetails, memberGroupDetails, adminGroupDetails, tripleDot].includes(event.target)){
        personalChatDetails.classList.add("hidden")
        memberGroupDetails.classList.add("hidden")
        adminGroupDetails.classList.add("hidden")
    }
})

document.querySelector("#editChat").addEventListener("click", () => {
    statusConnection.send(JSON.stringify({"request_type": "groupEdit", "group_id": document.querySelector('.selected-chat').id}))
})

const standartAvatarSrc = document.querySelector("#standartAvatarSrc").value
const chatTemplate = document.querySelector(".templates").querySelector(".single-message-div")

// CHECKPOINT - STATUSCONNECTION RECEIVE - !1

statusConnection.addEventListener("message", (event) => {
    let data = JSON.parse(event.data);
    if (data.request_type == "groupEdit"){
        groupCreationType.value = document.querySelector(".selected-chat").id
        groupCreationType.name = "edit"
        formBlur.classList.remove("hidden")
        newGroupForm.classList.remove("hidden")
        newGroupForm.querySelector(".group-name-input").value = chatName.innerHTML
        newGroupForm.querySelector(".create-group-avatar").src = chatAvatar.src
        newGroupForm.querySelector(".new-group-p").textContent = "Редагування групи"
        newGroupForm.querySelector(".create-button").textContent = "Зберегти зміни"
        addNewMemberButton.classList.remove("hidden")
        for (let memberData of data.members){
            let avatarLink = memberData.avatar
            if (avatarLink == 0 || avatarLink == "0"){
                avatarLink = standartAvatarSrc
            }
            let member = document.createElement("div")
            member.classList.add("single-member-div")
            member.id = memberData.id
            console.log(memberData)
            let memberAvatarBox = document.createElement("div")
            memberAvatarBox.classList.add("contacts-image"); memberAvatarBox.innerHTML = `<div class = "profile-box"><img src = "${avatarLink}" class = "prof-pic"></div>`
            let memberMainInfo = document.createElement("div"); memberMainInfo.classList.add("name-and-input-div")
            let memberTextInfo = document.createElement("p"); memberTextInfo.textContent = memberData.name
            memberMainInfo.appendChild(memberTextInfo)
            if (memberData.id != document.querySelector("#selfID").value){
                let trashbinIcon = document.createElement("img")
                trashbinIcon.src = trashbinSrc
                trashbinIcon.classList.add("bin-img")
                memberMainInfo.appendChild(trashbinIcon)
                choosedMembers.push(memberData.id)
            }
            else{
                memberTextInfo.textContent = `${memberData.name} (Ви)`
            }
            member.appendChild(memberAvatarBox); member.append(memberMainInfo)
            newGroupForm.querySelector(".create-group-members").appendChild(member)
        }
    }
    else if (data.request_type == "infoPost"){
        console.log(data, "Got info data")
        let text = "?"
        if (!personalChat){
            text = `${data.online} у мережі, ${data.summary} учасників`
        }
        else {
            if (Boolean(data.online)){
                text = "У мережі"
            }
            else {
                text = "Не в мережі"
            }
        }
        chatMembersOnline.textContent = text
    }
    else if (data.request_type == "message_notification"){
        console.log("You got a message!")
        let friendBox = document.querySelector(".friend-messages")
        let groupBox = document.querySelector(".group-messages")
        if (data.chat_data.personal){
            console.log("It is a DM")
            let chat = friendBox.querySelector(`[id='${data.chat_data.id}']`)
            if (chat == null){
                let notifiedChat = chatTemplate.cloneNode(true)
                notifiedChat.classList.remove("group-chat")
                notifiedChat.id = data.chat_data.id
                let avatarSrc = data.chat_data.avatar
                if (avatarSrc == "0"){
                    avatarSrc = standartAvatarSrc
                }
                notifiedChat.querySelector(".prof-pic").src = avatarSrc
                notifiedChat.querySelector(".message-author-name").textContent = data.chat_data.name
                notifiedChat.querySelector(".time-message").textContent = processMessageTime(data.time)
                notifiedChat.querySelector(".message-text").textContent = data.message_content
                if (friendBox.querySelectorAll(".single-message-div").length > 0){
                    friendBox.insertBefore(notifiedChat, friendBox.querySelector(".single-message-div"))
                }
                else{
                    friendBox.appendChild(notifiedChat)
                }
                notifiedChat.addEventListener("click", () => {
                    if (connection != null){
                        connection.close()
                    }
                    document.querySelector(".chat-messages").innerHTML = ""
                    makeConnection(notifiedChat.id, 1)
                    if (document.querySelector(".selected-chat") != null){
                        document.querySelector(".selected-chat").classList.remove("selected-chat")
                    }
                    notifiedChat.classList.add("selected-chat")
                    noChatText.classList.add("hidden")
                    chatBox.classList.remove("hidden")

                    chatAvatar.src = notifiedChat.querySelector("img").src
                    chatName.textContent = notifiedChat.querySelector(".contact-name-p").innerHTML
                    getChatInfo()
                    messageTextInput.focus()
                })
            }
            else {
                chat.querySelector(".message-text").textContent = data.message_content
                chat.querySelector(".time-message").textContent = processMessageTime(data.time)
            }
        }
        else{
            console.log("It is a group message")
            let chat = groupBox.querySelector(`[id='${data.chat_data.id}']`)
            chat.querySelector(".message-text").textContent = data.message_content
            chat.querySelector(".time-message").textContent = processMessageTime(data.time)
        }
    }
    else if (data.request_type == "delete_chat"){
        let chatBox = null
        let chat = null
        if (data.personal){
            chatBox = document.querySelector(".friend-messages")
            chat = chatBox.querySelector(`[id='${data.chat_id}']`)
            if (document.querySelector(".contacts-list-div").querySelector(".selected-chat") != null){
                if (document.querySelector(".contacts-list-div").querySelector(".selected-chat").id == chat.id){
                    closeChat()
                }
            }
        }
        else{
            chatBox = document.querySelector(".group-messages")
            chat = chatBox.querySelector(`[id='${data.chat_id}']`)
            if (chat.id == data.chat_id){
                closeChat()
            }
        }
        chat.remove()
    }
    if (data.request_type == "added_to_group"){
        let groupBox = document.querySelector(".group-messages")
        let notifiedChat = chatTemplate.cloneNode(true)
        notifiedChat.classList.remove("friend-chat")
        notifiedChat.id = data.id
        let avatarSrc = data.avatar
        if (avatarSrc == "0"){
            avatarSrc = standartAvatarSrc
        }
        notifiedChat.querySelector(".prof-pic").src = avatarSrc
        notifiedChat.querySelector(".message-author-name").textContent = data.name
        notifiedChat.querySelector(".time-message").textContent = " "
        notifiedChat.querySelector(".message-text").textContent = " "
        if (groupBox.querySelectorAll(".single-message-div").length > 0){
            groupBox.insertBefore(notifiedChat, groupBox.querySelector(".single-message-div"))
        }
        else{
            groupBox.appendChild(notifiedChat)
        }
        notifiedChat.addEventListener("click", () => {
            if (connection != null){
                connection.close()
            }
            document.querySelector(".chat-messages").innerHTML = ""
            makeConnection(notifiedChat.id, 0)
            if (document.querySelector(".selected-chat") != null){
                document.querySelector(".selected-chat").classList.remove("selected-chat")
            }
            notifiedChat.classList.add("selected-chat")
            noChatText.classList.add("hidden")
            chatBox.classList.remove("hidden")

            chatAvatar.src = notifiedChat.querySelector("img").src
            chatName.textContent = notifiedChat.querySelector(".contact-name-p").innerHTML
            getChatInfo()
            messageTextInput.focus()
        })
    }
    else{
        console.log(`Unexpected websocket message detected.\nData: ${data}`)
    }
})

function getChatInfo(){
    let chat = document.querySelector(".selected-chat")
    if (chat != null){
        let data = JSON.stringify({"request_type": "infoGet", "group_id": chat.id, "personal": personalChat})
        statusConnection.send(data)
    }
}

setInterval(getChatInfo, 12500)

document.querySelectorAll(".delete-chat").forEach(obj => {obj.addEventListener("click", () => {
    connection.send(JSON.stringify({"request": "delete"}))
})
})
document.getElementById("quitChat").addEventListener("click", () => {
    connection.send(JSON.stringify({"request": "quit"}))
})