window.addEventListener("DOMContentLoaded", (_) => {
    for (const button of document.getElementsByClassName("like-button")) {
        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/api/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
        })
    }

    for (const button of document.getElementsByClassName("watch-later-button")) {
        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/api/watch-later", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video_id: this.dataset.uuid })
            })
        })
    }

})
