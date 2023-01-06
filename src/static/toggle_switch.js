let buttons = new Map()

function store_button(key, value) {
    let list = buttons.get(key);
    if (list === undefined) {
        buttons.set(key, [value]);
    } else {
        list.push(value)
    }
}

window.addEventListener("DOMContentLoaded", (_) => {
    for (const button of document.getElementsByClassName("like-button")) {
        store_button(button.dataset.uuid, button);

        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/api/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
            console.log("checked: ", this.checked);
            console.log("uuid: ", this.dataset.uuid);
            console.log("buttons", buttons);
            for (const button of buttons[this.dataset.uuid]) {
                button.checked = this.checked;
            }
        })
    }

    for (const button of document.getElementsByClassName("watch-later-button")) {
        button.addEventListener("change", async function () {
            store_button(button.dataset.uuid, this);

            await fetch("http://35.217.17.201/api/watch-later", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
            for (const button of buttons[this.dataset.uuid]) {
                button.checked = this.checked;
            }
        })
    }

})
