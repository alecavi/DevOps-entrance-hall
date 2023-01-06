window.addEventListener("DOMContentLoaded", (_) => {
    for (const button of document.getElementsByClassName("like-button")) {
        button.addEventListener("change", async function () {
            await fetch("http://35.217.17.201/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video: this.dataset.uuid })
            })
        })
    }
})
