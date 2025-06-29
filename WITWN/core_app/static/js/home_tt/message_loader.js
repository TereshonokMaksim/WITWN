
function processMessageTime(text){
    let date = new Date(text)
    console.log(date, date.toLocaleString())
    let hours = String(date.getHours())
    let minutes = String(date.getMinutes())
    if (hours.length == 1){
        hours = `0${hours}`
    }
    if (minutes.length == 1){
        minutes = `0${minutes}`
    }
    let dateText = `${hours}:${minutes}`
    return dateText
}

document.querySelectorAll(".profile-friend-time").forEach(obj => {
    obj.innerHTML = processMessageTime(obj.innerHTML)
})