window.addEventListener("DOMContentLoaded", (_) => {
    for (const button of document.getElementsByClassName("like-button")) {
        console.log("ADDING", button)
        button.addEventListener("change", async function () {
            console.log("TRIGGERED", this)
            await fetch("http://35.217.17.201/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ state: this.checked, video: this.dataset.uuid })
            })
        })
    }
})
