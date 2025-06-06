
// First login form

let dimmer = document.querySelector(".form-dimmer")
let autoDimmer = document.querySelector("[name='auto-dimmer']")

console.log(autoDimmer)

if (autoDimmer != undefined){
    console.log("wh")
    console.log(dimmer.classList)
    dimmer.classList.remove("hidden")
    console.log(dimmer.classList)
    dimmer.removeEventListener("click", (event) => {
        if (event.target == el){
            closeForm()
        }
    })
}