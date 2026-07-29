const shareOptions = document.querySelector(".share-popup");
const shareBtn = document.querySelector(".share-btn");
const closeShareBtn = document.querySelector(".close_share-btn");

function sharePopup() {
    if (!shareOptions || !shareBtn || !closeShareBtn) return;
    shareOptions.classList.toggle('active');
    shareBtn.setAttribute("hidden", "");
    closeShareBtn.removeAttribute("hidden");
}

function closePopup() {
    if (!shareOptions || !shareBtn || !closeShareBtn) return;
    shareOptions.classList.remove('active');
    shareBtn.removeAttribute("hidden");
    closeShareBtn.setAttribute("hidden", "");
}

const copyUrl = document.getElementById("copy-btn");
if (copyUrl) {
    copyUrl.addEventListener("click", function(){
        copyUrl.innerHTML = "Copied";
        navigator.clipboard.writeText(document.getElementById("copy-url").value);
        setTimeout(function() {
            copyUrl.innerHTML ="Copy";
        }, 3000);
    });
}