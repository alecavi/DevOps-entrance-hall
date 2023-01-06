let like_buttons = new Map();
let watch_later_buttons = new Map();
let counter = 0;

function store_button(map, key, value) {
    let list = map.get(key);
    if (list === undefined) {
        map.set(key, [value]);
    } else {
        list.push(value)
    }
}

window.addEventListener("DOMContentLoaded", function () {
    for (const button of document.getElementsByClassName("like-button")) {
        store_button(like_buttons, button.dataset.uuid, button);

        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/api/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
            for (const button of like_buttons.get(this.dataset.uuid)) {
                button.checked = this.checked;
            }
        })
    }

    for (const button of document.getElementsByClassName("watch-later-button")) {
        store_button(watch_later_buttons, button.dataset.uuid, button);

        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/api/watch-later", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
            for (const button of watch_later_buttons.get(this.dataset.uuid)) {
                button.checked = this.checked;
            }
        })
    }
})