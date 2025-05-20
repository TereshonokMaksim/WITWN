const detailsWindow = document.querySelector(".post-detail-box")
let detailButtons = []
let clickedDetailButtons = 0
let deleteURL = document.querySelector("[name='deleteURL']").value

// document.querySelector().parentElement

document.addEventListener("click", (event) => {
    if (!detailButtons.includes(event.target) && detailsWindow != event.target){
        detailsWindow.classList.add("hidden")
    }
})

function detailClickEvent(button){
    let detailsStyles = getComputedStyle(detailsWindow)
    let detailsWidth = Number(detailsStyles.width.split("px")[0])
    detailsWindow.style.top = `${button.parentElement.offsetTop + 4}px`
    detailsWindow.style.left = `${button.offsetLeft + 38 - detailsWidth}px`
    detailsWindow.classList.remove("hidden")
    detailsWindow.id = button.id.split("-")[1]
}

function getDetailButtons(){
    detailButtons = Array.from(document.querySelectorAll(".author-triple-dot"))
    detailButtons.forEach((button) => {button.addEventListener("click", () => {detailClickEvent(button)})})
}

document.querySelector("#deletePost").addEventListener("click", () => {
    console.log("Clicked")
    fetch(`${deleteURL}${detailsWindow.id}`).then(() => {
        console.log("deleted")
    })
    document.querySelector(`#post-${detailsWindow.id}`).remove()
    let profNum = document.querySelector("#profilePostsNum")
    profNum.innerHTML = Number(profNum.innerHTML) - 1
    detailsWindow.classList.add("hidden")
})

getDetailButtons()

const creationForm = document.querySelector(".form-creation-post")
const transferCanvas = document.querySelector(".image-transfer")
const canvasContext = transferCanvas.getContext("2d")

function imgTag2File(imgTag, imgName){
    transferCanvas.width = imgTag.naturalWidth
    transferCanvas.height = imgTag.naturalHeight

    canvasContext.drawImage(imgTag, 0, 0)
    transferCanvas.toBlob(blob => {
        let file = new File([blob], imgName, {"type": blob.type})
        
        let id = 0
        let idNum = 0
        while (id == 0){
            let name = `${file.name}_${idNum}`
            if (filesObject[name] == undefined){
                id = name
            }
            idNum++
        }
        filesObject[id] = file
        addImage(file, id)
    })
}

document.querySelector("#editPost").addEventListener("click", () => {
    creationForm.querySelector(`[name="specific_id"]`).value = detailsWindow.id
    let origPost = document.querySelector(`#post-${detailsWindow.id}`)
    creationForm.querySelector("#id_title").value = origPost.querySelector(".content-title").innerHTML
    creationForm.querySelector("#id_theme").value = origPost.querySelector(".content-theme").innerHTML
    creationForm.querySelector("#id_text").value = origPost.querySelector(".content-text").innerHTML
    let links = ""
    for (let linkTag of origPost.querySelectorAll(".content-link")){
        links += `${linkTag.href} `
    }
    creationForm.querySelector("#id_links").value = links  
    for (let imageBox of origPost.querySelectorAll(".post-content-img")){
        imgTag2File(imageBox)
    }
    creationForm.querySelector(".creation-form-title").innerHTML = "Редагування публікації"
    creationForm.querySelector(".creation-form-send").innerHTML = `Оновити ${sendImgTextTag}`
    dimmer.classList.replace("hidden", "show")
})