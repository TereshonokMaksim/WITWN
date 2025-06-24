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
const deleteRecomendationLink = cutBackOfLink(document.querySelector("#deleteRecomendationLink").value)

document.querySelectorAll(".req-conf-button").forEach((obj) => {obj.addEventListener("click", () => {
    if (document.querySelector(".friends-block") != undefined){
        document.querySelector(".friends-block").insertBefore(obj.parentNode.parentNode, document.querySelector(".single-friend-div"))
        obj.parentNode.parentNode.classList.add(".single-friend-div")
        obj.innerHTML = "Повідомлення"
        obj.classList.remove("req-conf-button")
        obj.classList.add("send-message-button")
        let delButton = obj.parentNode.querySelectorAll("button")[1]
        delButton.classList.remove("req-del-button")
        delButton.classList.add("del-friend-button")
    }
    else{
        obj.parentNode.parentNode.remove()
    }
    fetch(`${addFriendLink}/${obj.parentNode.parentNode.id}`).then(data => {data})
})})
document.querySelectorAll(".req-del-button").forEach((obj) => {obj.addEventListener("click", () => {
    obj.parentNode.parentNode.remove()
    fetch(`${denyRequestLink}/${obj.parentNode.parentNode.id}`).then(data => {data})
})})
document.querySelectorAll(".conf-rec-button").forEach((obj) => {obj.addEventListener("click", () => {
    obj.parentNode.parentNode.remove()
    fetch(`${sendRequestLink}/${obj.parentNode.parentNode.id}`).then(data => {data})
})})
document.querySelectorAll(".del-rec-button").forEach((obj) => {obj.addEventListener("click", () => {
    obj.parentNode.parentNode.remove()
    fetch(`${deleteRecomendationLink}/${obj.parentNode.parentNode.id}`).then(data => {data})
})})
document.querySelectorAll(".del-friend-button").forEach((obj) => {obj.addEventListener("click", () => {
    obj.parentNode.parentNode.remove()
    fetch(`${removeFriendLink}/${obj.parentNode.parentNode.id}`).then(data => {data})
})})