let pageName = document.querySelector("#pageNameString")
if (pageName != undefined){
    document.querySelector(`#${pageName.value}Link`).classList.add("choosed-link")
}