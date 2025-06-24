let pageName = document.querySelector("#pageNameString")
if (pageName != undefined){
    document.querySelector(`#${pageName.value}Link`).classList.add("choosed-link")
}

const connectionLink = `ws://${window.location.host}/user_status/`
const connectionUserStatus = new WebSocket(connectionLink)

connectionUserStatus.addEventListener("open", (event) => {
    console.log("User marked as online.")
    connectionUserStatus.send(JSON.stringify({"request": "ping"}))
    setInterval(() => {
        console.log("Pinging.")
        connectionUserStatus.send(JSON.stringify({"request": "ping"}))
    }, 25000)
})  