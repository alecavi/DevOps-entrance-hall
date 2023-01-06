let like_buttons = new Map();
like_buttons.set("test", "tset");
let counter = 0;

function store_like_button(key, value) {
    let list = like_buttons.get(key);
    if (list === undefined) {
        like_buttons.set(key, [value]);
    } else {
        list.push(value)
    }
    console.log("store_button ", JSON.stringify(like_buttons), counter++);
}

window.addEventListener("DOMContentLoaded", function () {
    for (const button of document.getElementsByClassName("like-button")) {
        store_like_button(button.dataset.uuid, button);

        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/api/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
            console.log("checked: ", this.checked);
            console.log("uuid: ", this.dataset.uuid);
            console.log("buttons", JSON.stringify(like_buttons));
            for (const button of like_buttons[this.dataset.uuid]) {
                button.checked = this.checked;
            }
        })
    }

    for (const button of document.getElementsByClassName("watch-later-button")) {
        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/api/watch-later", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
            for (const button of like_buttons[this.dataset.uuid]) {
                button.checked = this.checked;
            }
        })
    }
    console.log("layer one", JSON.stringify(like_buttons));
})
console.log("layer zero", JSON.stringify(like_buttons));