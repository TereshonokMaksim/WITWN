function getContrastYIQ(hexcolor) {
    // hexcolor = hexcolor.replace("#", "");
    const r = parseInt(hexcolor.substr(0, 2), 16);
    const g = parseInt(hexcolor.substr(2, 2), 16);
    const b = parseInt(hexcolor.substr(4, 2), 16);
    const yiq = (r * 299 + g * 587 + b * 114) / 1000;
    return yiq >= 128 ? 'black' : 'white';
}

function autoTagTextColoring(){
    let allTags = document.querySelectorAll(".tag")
    allTags.forEach((tag) => {
        console.log(tag.style)
        tag.style.backgroundColor = `#${tag.dataset.color}`
        tag.style.color = getContrastYIQ(tag.dataset.color)
    })
}

autoTagTextColoring()