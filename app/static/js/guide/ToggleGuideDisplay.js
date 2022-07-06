var guide = document.querySelector(".guide__section")
var openerGuideBtn = document.querySelector(".itd__btn-guide")
var closerGuideBtn = document.querySelector(".guide__close-btn")

openerGuideBtn.addEventListener("click", openGuide)
closerGuideBtn.addEventListener("click", closeGuide)

function openGuide() {
    guide.style.display = "flex"
}

function closeGuide() {
    guide.style.display = "none"
}
