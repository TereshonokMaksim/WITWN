const makePostButton = document.querySelector(".form-button")
const dimmer = document.querySelector(".form-dimmer")
const creationFormClose = document.querySelector(".creation-form-close")
const publicationForm = document.querySelector(".form-creation-post")
let sendImgTextTag = `<img src = "${document.querySelector("[name='sendImgURL']").value}">`
// const createPostURL = document.querySelector("[name='postUrl']").value


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
}

function sendForm(){
    // let inputs = publicationForm.querySelectorAll("input")
    // for (let input of inputs){
    //     if (!input.hidden){
    //         data.append(input.name, input.value)
    //     }
    // }
    // let areaTexts = publicationForm.querySelectorAll("textarea")
    // for (let areaText of areaTexts){
    //     data.append(areaText.name, areaText.value)
    // }
    // for (let file of Object.values(filesObject)){
    //     data.append("files[]", file)
    // }
}

publicationForm.addEventListener("submit", (event) => {
    event.preventDefault()
    // IMAGES_INPUT.type = "text"
    // IMAGES_INPUT.files = FileList(Object.values(filesObject))
    // IMAGES_INPUT.type = "file"
    // publicationForm.querySelector(".creation-form-inputs").innerHTML += '<input type="file" name="files" class="hidden" multiple="" id="id_files">'

    let data = new FormData(publicationForm)
    
    
    // let inputs = publicationForm.querySelectorAll("input")
    // for (let input of inputs){
    //     if (!input.hidden){
    //         data.append(input.name, input.value)
    //     }
    // }
    // let areaTexts = publicationForm.querySelectorAll("textarea")
    // for (let areaText of areaTexts){
    //     data.append(areaText.name, areaText.value)
    // }
    data.delete("files")
    let fileTransfer = new DataTransfer()
    for (let file of Object.values(filesObject)){
        fileTransfer.items.add(file)
    }
    IMAGES_INPUT.files = fileTransfer.files

    publicationForm.submit()

    // closeForm()

    // fetch(createPostURL, {
    //     "method": "POST",
    //     "body": data
    // }).then(response => console.log(`Response to the form: ${response}`))
    
    // for (const [key, value] of data.entries()) {
    //     console.log(key, value);
    // }
    // data

    // console.log(data)
    // console.log(publicationForm)
})

makePostButton.addEventListener("click", () => {
    dimmer.classList.replace("hidden", "show");
    let origText = document.querySelector("#publication-text")
    publicationForm.querySelector("#id_text").value = origText.value
    origText.value = ""
})

// По неведомой мне причине, код, который написан дальше, 
// отказывается делать что угодно, если следующая линия будет отсутствовать 
typeof makePostButton;


[dimmer, creationFormClose].forEach((el) => {
    el.addEventListener("click", (event) => {
        if (event.target == el){
            closeForm()
        }
    }
)})

// publicationForm.addEventListener("click", () => {console.log("Am i being clicked?")})

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
        // document.querySelector("#testImg").src = URL.createObjectURL(IMAGES_INPUT.files[0])
    }
})

// SCROLLLLL

const SCROLL_TRACK = document.querySelector(".creation-textarea-scrolltrack")
const SCROLL = document.querySelector(".creation-textarea-scroll")
const SCROLLABLE_AREA = document.querySelector(".creation-input-area")
// in pixels
const MIN_SCROLL_HEIGHT = 10

// let textActualHeight = 0

function resizeScroll(){
    let height = (SCROLLABLE_AREA.clientHeight / SCROLLABLE_AREA.scrollHeight) * SCROLL_TRACK.clientHeight
    height = Math.max(MIN_SCROLL_HEIGHT, Math.min(height, SCROLL_TRACK.clientHeight))
    SCROLL.style.height = `${height}px`
    let top = Math.min(SCROLL_TRACK.clientHeight - height, Math.max(0, height))
    SCROLL.style.top = `${top}px`
    adaptScroll()
    // console.log(height, SCROLL_TRACK.clientHeight, MIN_SCROLL_HEIGHT)
    // console.log(SCROLLABLE_AREA.clientHeight / SCROLLABLE_AREA.scrollHeight, SCROLLABLE_AREA.clientHeight, SCROLLABLE_AREA.scrollHeight)
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
    // console.log(`${}px`, lastMouseY - event.clientY, Number(SCROLL.style.top.split('px')[0]) + (lastMouseY - event.clientY), Number(SCROLL.style.top.split('px')[0]))
    let yDifference = lastMouseY - event.clientY
    let originalTop = Number(SCROLL.style.top.split('px')[0])
    let top = originalTop - yDifference
    top = Math.min(SCROLL_TRACK.clientHeight - SCROLL.clientHeight + 2, Math.max(-2, top))
    if (clicked){
        // console.lo
        moveContent(originalTop - top)
        SCROLL.style.top = `${top}px`
    }
    lastMouseY = event.clientY
})

SCROLL.addEventListener("mousedown", (event) => {
    clicked = true
    lastMouseY = event.clientY
    // console.log('soadka[]')
})

document.addEventListener("mouseup", (event) => {
    clicked = false
})

SCROLLABLE_AREA.addEventListener("input", () => {
    // setContentScroll(1)
    setTimeout(resizeScroll, 0.03)
    // adaptScroll()
})
SCROLLABLE_AREA.addEventListener("scroll", adaptScroll)