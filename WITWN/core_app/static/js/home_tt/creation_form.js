const makePostButton = document.querySelector(".form-button")
const dimmer = document.querySelector(".form-dimmer")
const creationFormClose = document.querySelector(".creation-form-close")
const publicationForm = document.querySelector(".form-creation-post")
let sendImgTextTag = `<img src = "${document.querySelector("[name='sendImgURL']").value}">`

function closeForm(){
    dimmer.classList.replace("show", "hidden")
    publicationForm.querySelector("[name='specific_id']").value = -1
    publicationForm.reset()
    resizeScroll()
    setContentScroll(0)
    for (let imgBox of document.querySelectorAll(".creation-image-box")){
        if (imgBox.id != "originalImgTemplate"){
            imgBox.remove()
            delete filesObject[imgBox.id]
        }
    }
    publicationForm.querySelector(".creation-form-title").innerHTML = "Створення публікації"
    publicationForm.querySelector(".creation-form-send").innerHTML = `Публікація ${sendImgTextTag}`
    // Tag cleaning
    for (let tagElement of document.querySelectorAll(".create-tag-name")){
        tagElement.remove()
    }
    updateTagsPreviewText()
    let linkBlocks = Array.from(document.querySelectorAll(".creation-link-box"))
    linkBlocks.splice(0, 1)
    console.log(linkBlocks)
    for (let linkBlock of linkBlocks){
        linkBlock.remove()
    }
    document.querySelector(".creation-link-box").querySelector(".creation-link-input").value = ""
    document.querySelector(".creation-link-box").querySelector(".creation-link-create").classList.remove("hidden")
}

publicationForm.addEventListener("submit", (event) => {
    event.preventDefault()
    let data = new FormData(publicationForm)
    
    data.delete("files")
    let fileTransfer = new DataTransfer()
    for (let file of Object.values(filesObject)){
        fileTransfer.items.add(file)
    }
    IMAGES_INPUT.files = fileTransfer.files

    let tagsText = tagsTextPreview.innerHTML
    document.querySelector("#id_tags").value = tagsText

    let linksText = ""
    for (let linksTag of document.querySelectorAll(".creation-link-input")){
        linksText += `${linksTag.value} `
    }
    document.querySelector("#id_links").value = linksText

    publicationForm.submit()
})

makePostButton.addEventListener("click", () => {
    dimmer.classList.replace("hidden", "show");
    let origText = document.querySelector("#publication-text")
    publicationForm.querySelector("#id_text").value = origText.value
    origText.value = ""
})

// По неведомой мне причине, код, который написан дальше, 
// отказывается делать что угодно, если следующая линия будет отсутствовать 
// Обновление 29.05.2025: Оно все еще не работает без этого
typeof makePostButton;


[dimmer, creationFormClose].forEach((el) => {
    el.addEventListener("click", (event) => {
        if (event.target == el){
            closeForm()
        }
    }
)})

// New Technical Task - Tags 'N Links
// Code cleaned of commented code after successfull commit

let createTagButton = document.querySelector('.create-tag-button')
let createTagInput = document.querySelector('#createTagInput')
let createTagDiv = document.querySelector('#createTagDiv')
let createFormBox = document.querySelector(".create-tag-box")
let showTagButton = document.querySelector(".show-tag-button")
let tagsTextPreview = document.querySelector(".create-tag-preview")
let mainTextArea = document.querySelector("#id_text")


publicationForm.querySelector(".creation-form-inputs").insertBefore(createTagDiv, document.querySelector("#id_text").parentElement)
mainTextArea.parentElement.appendChild(tagsTextPreview)

function textAreaContentHeight(textArea){
    let copy = document.getElementById("areaTextCopy")
    let orStyle = window.getComputedStyle(textArea)
    copy.style.padding = orStyle.padding
    copy.style.width = orStyle.width
    copy.style.fontSize = orStyle.fontSize
    copy.style.border = orStyle.border
    copy.style.lineHeight = orStyle.lineHeight
    if (copy.innerHTML != ""){
        copy.innerHTML = textArea.value
    }
    else{
        copy.innerHTML = " "
    }
    return copy.scrollHeight
}

function px2vw(px){
    return px / window.innerWidth * 100
}

function px2vh(px){
    console.log(px)
    return px / window.innerHeight * 100
}

function updateTagsPreviewPosition(){
    let areaStyle = window.getComputedStyle(mainTextArea)
    let offsetLeft = px2vw(Number(areaStyle.paddingLeft.split("px")[0]))
    let offsetTop = px2vh(mainTextArea.parentElement.querySelector("label").clientHeight)
    offsetTop += px2vh(Number(window.getComputedStyle(mainTextArea.parentElement).gap.split("px")[0]))
    offsetTop += Math.max(0.5, textAreaContentHeight(mainTextArea))
    offsetTop -= px2vh(10)
    offsetTop -= px2vh(mainTextArea.scrollTop)
    console.log(offsetLeft, offsetTop, window.innerHeight, window.innerWidth)
    tagsTextPreview.style.left = `calc(${offsetLeft * 0.6}vw + )`
    tagsTextPreview.style.top = `${offsetTop}vh`
}

function updateTagsPreviewText(){
    let tagsText = ''
    for (let tagTag of document.querySelectorAll(".create-tag-name")){
        tagsText += `${tagTag.innerHTML} `
    }
    tagsTextPreview.innerHTML = tagsText
    updateTagsPreviewPosition()
}

showTagButton.addEventListener("click", () => {
    createFormBox.classList.remove("hidden")
    showTagButton.classList.add("hidden")
    createTagInput.focus()
})

function closeTagCreation(){
    createTagInput.value = ""
    createFormBox.classList.add("hidden")
    showTagButton.classList.remove("hidden")
}

function createTag(text = null){
    if (text == null){
        if (createTagInput.value.includes(" ")){
            return false
        }
        tagText = `#${createTagInput.value}`
    }
    else{
        tagText = text
    }
    let newTag = document.createElement("p")
    newTag.classList.add("create-tag-name")
    newTag.textContent = tagText
    newTag.addEventListener("click", () => {
        newTag.remove()
        updateTagsPreviewText()
    })
    createTagDiv.insertBefore(newTag, createFormBox)
    closeTagCreation()
    updateTagsPreviewText()
    return true
}

document.addEventListener("mousedown", (event) => {
    let allLinkBoxes = document.querySelectorAll(".creation-link-box")
    if (![createFormBox, createTagButton, createTagInput].includes(event.target)){
        closeTagCreation()
    }
    if (![allLinkBoxes[allLinkBoxes.length - 1], ...document.querySelectorAll(".creation-link-create")].includes(event.target)){
        allLinkBoxes[allLinkBoxes.length - 1].querySelector(".creation-link-confirm").classList.add("hidden")
        allLinkBoxes[allLinkBoxes.length - 1].querySelector(".creation-link-create").classList.remove("hidden")
    }
})

createTagInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter"){
        event.preventDefault(); 
        createTag();
    }
})


mainTextArea.addEventListener("input", updateTagsPreviewPosition)
mainTextArea.addEventListener("scroll", updateTagsPreviewPosition)
createTagButton.addEventListener("click", () => {createTag()})

// Form creation: Links

let linksBlock = document.querySelector(".creation-links-block")

function createLinkBlock(){
    let newBlock = document.querySelector(".creation-link-box").cloneNode(true)
    linksBlock.appendChild(newBlock)
    let confirmButton = newBlock.querySelector(".creation-link-confirm")
    let deleteButton = newBlock.querySelector(".creation-link-delete")
    let createButton = newBlock.querySelector(".creation-link-create")
    let linkInput = newBlock.querySelector(".creation-link-input")
    linkInput.focus()
    confirmButton.classList.remove("hidden")
    deleteButton.classList.remove("hidden")
    createButton.classList.add("hidden")
    linkInput.value = ""
    confirmButton.addEventListener("click", () => {
        confirmButton.classList.add("hidden")
        for (let createLinkButton of document.querySelectorAll(".creation-link-create")){
            if (!createLinkButton.classList.contains("hidden")){
                return
            }
        }
        createButton.classList.remove("hidden")
    })
    deleteButton.addEventListener("click", () => {
        if (!createButton.classList.contains("hidden") || !confirmButton.classList.contains("hidden")){
            newBlock.previousElementSibling.querySelector(".creation-link-create").classList.remove("hidden")
        }
        newBlock.remove()
    })  
    createButton.addEventListener('click', () => {
        createButton.classList.add("hidden")
        createLinkBlock()
    })
    return newBlock
}

document.querySelector(".creation-link-create").addEventListener("click", () => {
    document.querySelector(".creation-link-create").classList.add("hidden")
    createLinkBlock()
})

// Form creation: Images

const IMAGES_BUTTON = document.querySelector(".creation-images-button")
const IMAGES_INPUT = document.querySelector("#id_files")
const IMAGE_BOX_TEMPLATE = document.querySelector("#originalImgTemplate")
let filesObject = Object()

IMAGES_BUTTON.addEventListener("click", (event) => {
    IMAGES_INPUT.click()
})

function addImage(imageFile, fileName){
    let imageBox = IMAGE_BOX_TEMPLATE.cloneNode(true)
    imageBox.querySelector("img").src = URL.createObjectURL(imageFile)
    imageBox.id = fileName
    imageBox.classList.remove("hidden")
    imageBox.querySelector(".creation-image-delete").addEventListener("click", (event) => {
        imageBox.remove()
        delete filesObject[imageBox.id]
    })
    document.querySelector(".creation-image-grid").appendChild(imageBox)
}

IMAGES_INPUT.addEventListener("change", (event) => {
    let files = IMAGES_INPUT.files
    for (let file of files){
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
    }
})

// SCROLLLLL

const SCROLL_TRACK = document.querySelector(".creation-textarea-scrolltrack")
const SCROLL = document.querySelector(".creation-textarea-scroll")
const SCROLLABLE_AREA = document.querySelector(".creation-input-area")
// in pixels
const MIN_SCROLL_HEIGHT = 10

function resizeScroll(){
    let height = (SCROLLABLE_AREA.clientHeight / SCROLLABLE_AREA.scrollHeight) * SCROLL_TRACK.clientHeight
    height = Math.max(MIN_SCROLL_HEIGHT, Math.min(height, SCROLL_TRACK.clientHeight))
    SCROLL.style.height = `${height / window.innerHeight * 100}vh`
    let top = Math.min(SCROLL_TRACK.clientHeight - height, Math.max(0, height))
    SCROLL.style.top = `${top}px`
    adaptScroll()
}

function moveContent(yDifference){
    let yMultiplier = (SCROLLABLE_AREA.clientHeight - SCROLLABLE_AREA.scrollHeight) / (SCROLL_TRACK.clientHeight - SCROLL.clientHeight)
    let yScroll = yMultiplier * yDifference
    SCROLLABLE_AREA.scrollTop += yScroll
}   

function setContentScroll(percentScrolled){
    SCROLLABLE_AREA.scrollTop = Math.min(SCROLLABLE_AREA.scrollHeight - SCROLLABLE_AREA.clientHeight, 0) * percentScrolled
    SCROLL.style.top = `${(SCROLL_TRACK.clientHeight - SCROLL.clientHeight) * percentScrolled}px`
}

function adaptScroll(){
    if (SCROLLABLE_AREA.scrollHeight - SCROLLABLE_AREA.clientHeight > 0){
        let percentScrolled = SCROLLABLE_AREA.scrollTop / (SCROLLABLE_AREA.scrollHeight - SCROLLABLE_AREA.clientHeight)
        console.log(percentScrolled)
        SCROLL.style.top = `${(SCROLL_TRACK.clientHeight - SCROLL.clientHeight) * percentScrolled}px`
    }
    else {
        SCROLL.style.top = `0px`
        SCROLL.style.height = `${SCROLL_TRACK.clientHeight}px`
    }
}

let clicked = false
let lastMouseY = 0

document.addEventListener("mousemove", (event) => {
    let yDifference = lastMouseY - event.clientY
    let originalTop = Number(SCROLL.style.top.split('px')[0])
    let top = originalTop - yDifference
    top = Math.min(SCROLL_TRACK.clientHeight - SCROLL.clientHeight + 2, Math.max(-2, top))
    if (clicked){
        moveContent(originalTop - top)
        SCROLL.style.top = `${top}px`
    }
    lastMouseY = event.clientY
})

SCROLL.addEventListener("mousedown", (event) => {
    clicked = true
    lastMouseY = event.clientY
})

document.addEventListener("mouseup", (event) => {
    clicked = false
})

SCROLLABLE_AREA.addEventListener("input", () => {
    setTimeout(resizeScroll, 0.03)
})
SCROLLABLE_AREA.addEventListener("scroll", adaptScroll)
