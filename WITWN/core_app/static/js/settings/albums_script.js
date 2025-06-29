const newAlbumButton = document.querySelector(".album-new-album")
const dimmer = document.querySelector(".dimmer")
const templates = document.querySelector("#templates")
const albumTemplate = templates.querySelector(".album-div")
const imageTemplate = templates.querySelector(".album-image-box")
const elementsWithEvents = []

newAlbumButton.addEventListener("click", () => {
    dimmer.classList.remove("hidden")
    console.log("log")
})

dimmer.addEventListener("click", (event) => {
    if (event.target == dimmer){
        dimmer.classList.add("hidden")
    }
})

function cutBackOfLink(link){
    link = link.split("/")
    link.splice(link.length - 1, 1)
    link = link.join("/")
    return link
}

const deleteImageLink = cutBackOfLink(document.querySelector("#deleteImage").value)
const deleteAvatarLink = cutBackOfLink(document.querySelector("#deleteAvatar").value)
const deleteAlbumLink = cutBackOfLink(document.querySelector("#deleteAlbum").value)
const visibilityImageLink = cutBackOfLink(document.querySelector("#visibilityImage").value)
const visibilityAlbumLink = cutBackOfLink(document.querySelector("#visibilityAlbum").value)
const createAlbumLink = document.querySelector("#createAlbum").value
const createImageLink = document.querySelector("#createImage").value
const form = document.querySelector(".new-album-form")

form.addEventListener("submit", (event) => {
    event.preventDefault()
    let dataRaw = new FormData(form)
    let dataObject = Object.fromEntries(dataRaw.entries())
    console.log(dataObject)

    postData(createAlbumLink, dataRaw).then((data) => {
        dimmer.classList.add("hidden")
        let newAlbum = albumTemplate.cloneNode(true)
        newAlbum.id = data["id"]
        newAlbum.querySelector(".album-title").textContent = dataObject["name"]
        // let options = document.querySelectorAll("option")
        // let theme = options[Number(dataObject["theme"])].innerHTML
        let theme = document.getElementById("id_topic").querySelectorAll("option")[Number(document.getElementById("id_topic").value) + 1].textContent.split("#")[1]
        // newAlbum.querySelector(".album-additional-info").innerHTML = `${theme} <span class = "album-year">${dataObject["year"]} рік</span>`
        newAlbum.querySelector(".album-additional-info").innerHTML = `${theme} <span class = "album-year">2025 рік</span>`

        document.querySelector(".content-div").insertBefore(newAlbum, document.querySelector(".new-album-creation"))
        controlInit()
        let firstThemeOption = document.getElementById("id_topic").querySelector("option")
        firstThemeOption.selected = true
        document.getElementById("id_topic").value = ''
        document.getElementById("id_name").value = ""
    })
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

const openedEye = document.querySelector("#openedEye").value
const closedEye = document.querySelector("#closedEye").value

const imageInput = document.querySelector("#imageInput")

function addImage(id){
    console.log("huh")
    imageInput.name = id
    imageInput.click()
}

imageInput.addEventListener("input", () => {
    let rawData = new FormData()
    rawData.append("album_id", imageInput.name)
    rawData.append("file", imageInput.files[0])
    postData(createImageLink, rawData).then((data) => {
        let image = imageTemplate.cloneNode(true)
        image.querySelector(".album-image").src = URL.createObjectURL(imageInput.files[0])
        image.id = data["id"]
        let selectedAlbum = 0
        for (let album of document.querySelectorAll(`.album-div`)){
            if (album.id == imageInput.name){
                selectedAlbum = album
                break
            }
        }

        let selectedAlbumPhotos = selectedAlbum.querySelector(".album-images-block")

        selectedAlbumPhotos.insertBefore(image, selectedAlbumPhotos.querySelector(".album-new-imagebox"))
        controlInit()
    })
})

document.querySelector(".new-album-cancel").addEventListener("click", () => {
        dimmer.classList.add("hidden")
        elementsWithEvents.push(document.querySelector(".new-album-cancel"))
})

function controlInit(){
    document.querySelectorAll(".album-new-image").forEach((object) => {
        if (!elementsWithEvents.includes(object)){
            object.addEventListener("click", () => {
            addImage(object.parentNode.parentNode.id)
            elementsWithEvents.push(object)
            })
        }
    })
    document.querySelectorAll(".album-new-createbox").forEach((object) => {
        if (!elementsWithEvents.includes(object)){
            object.addEventListener("click", () => {
            addImage(object.parentNode.parentNode.parentNode.id)
            elementsWithEvents.push(object)
            })
        }
    })

    document.querySelectorAll(".album-image-visibility").forEach((object) => {object.addEventListener("click", () => {
        if (!elementsWithEvents.includes(object)){
            object.addEventListener("click", () => {
            if (object.id == "0"){
                object.id = "1"
                object.src = openedEye
                fetch(`${visibilityImageLink}/${object.parentNode.parentNode.id}&1`).then(console.log("Changed"))
            }
            else{
                object.id = "0"
                object.src = closedEye
                fetch(`${visibilityImageLink}/${object.parentNode.parentNode.id}&0`).then(console.log("Changed"))
            }
        })
        }
    })

    document.querySelectorAll(".album-image-delete").forEach((object) => {
        if (!elementsWithEvents.includes(object)){
            object.addEventListener("click", (event) => {
            let id = object.parentNode.parentNode.id
            if (event.currentTarget.closest(".album-div").id != "-1"){
                fetch(`${deleteImageLink}/${id}`).then(console.log("Deleted successfully (?)"))
            }
            else {
                console.log("djosadjaodjosajd")
                fetch(`${deleteAvatarLink}/${id}`).then(console.log("Deleted successfully (?)"))
            }
            elementsWithEvents.push(object)
            object.parentNode.parentNode.remove()
            })
        }
    })})

    document.querySelectorAll(".album-visibility").forEach((object) => {
        if (!elementsWithEvents.includes(object)){
            object.addEventListener("click", () => {
            let album = object.parentNode.parentNode.parentNode.id
            if (object.id == "0"){
                object.id = "1"
                object.src = openedEye
                fetch(`${visibilityAlbumLink}/${album}&1`).then(console.log("Changed"))
            }
            else{
                object.id = "0"
                object.src = closedEye
                fetch(`${visibilityAlbumLink}/${album}&0`).then(console.log("Changed"))
            }
            elementsWithEvents.push(object)
        })
        }
    })

    document.querySelectorAll(".album-delete").forEach((object) => {
        if (!elementsWithEvents.includes(object)){
            object.addEventListener("click", () => {
            let id = object.parentNode.parentNode.parentNode.id
            object.parentNode.parentNode.parentNode.remove()
            fetch(`${deleteAlbumLink}/${id}`).then(console.log("Deleted successfully (?)"))
            elementsWithEvents.push(object)
            })
        }
    })
}

controlInit()