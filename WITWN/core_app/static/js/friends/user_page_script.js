function cutBackOfLink(link){
    link = link.split("/")
    link.splice(link.length - 1, 1)
    link = link.join("/")
    return link
}

const addFriendLink = cutBackOfLink(document.querySelector("#addFriendLink").value)
const removeFriendLink = cutBackOfLink(document.querySelector("#removeFriendLink").value)
const denyRequestLink = cutBackOfLink(document.querySelector("#denyRequestLink").value)
const sendRequestLink = cutBackOfLink(document.querySelector("#sendRequestLink").value)

const relation = document.querySelector("#userRelation").value
const successButton = document.querySelector(".profile-header-confirm")
const failButton = document.querySelector(".profile-header-deny")
let successLink = ""
let failLink = ""

if (relation == "none"){
    successButton.innerHTML = "Додати"
    failButton.classList.add("hidden")
    successLink = sendRequestLink
}
else if (relation == "requested"){
    successButton.classList.add("hidden")
    failButton.classList.add("hidden")
    document.querySelector("#headerSendReqText")
}
else if (relation == "request"){
    successButton.innerHTML = "Підвердити"
    failButton.innerHTML = "Відхилити"
    successLink = addFriendLink
    failLink = denyRequestLink
}
else if (relation == "friend"){
    successButton.innerHTML = "Повідомлення"
    failButton.innerHTML = "Видалити"
    failLink = removeFriendLink
}

successButton.addEventListener("click", () => {
    if (relation != "friend"){
        fetch(`${successLink}/${obj.parentNode.id}`).then(data => {data})
        if (relation == "none"){
            successButton.classList.add("hidden")
            document.querySelector("#headerSendReqText").classList.remove("hidden")
        }
        else if (relation == "request"){
            successButton.innerHTML = "Повідомлення"
            failButton.innerHTML = "Видалити"
            successLink = ""
            failLink = removeFriendLink
        }
    }
})

failButton.addEventListener("click", () => {
    fetch(`${failLink}/${obj.parentNode.id}`).then(data => {data})
    if (relation == "request"){
        document.querySelector("#headerDelReqText").classList.remove("hidden")
        successButton.classList.add("hidden")
        failButton.classList.add("hidden")
    }
    else if (relation == "friend"){
        document.querySelector("#headerDelFriendText").classList.remove("hidden")
        successButton.classList.add("hidden")
        failButton.classList.add("hidden")
    }
})