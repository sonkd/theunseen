const shareOptions = document.querySelector(".share-popup");
const shareBtn = document.querySelector(".share-btn");
const closeShareBtn = document.querySelector(".close_share-btn");

function sharePopup() {
    shareOptions.classList.toggle('active');
    shareBtn.setAttribute("hidden", "");
    closeShareBtn.removeAttribute("hidden");
}

function closePopup() {
    shareOptions.classList.remove('active');
    shareBtn.removeAttribute("hidden");
    closeShareBtn.setAttribute("hidden", "");
}