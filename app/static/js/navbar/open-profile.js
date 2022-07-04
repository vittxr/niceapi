var navbar__profileItem = document.querySelector(".navbar__profile-item");
var profile__box = document.querySelector(".profile__box");

navbar__profileItem.addEventListener("mouseover", OpenProfile)
navbar__profileItem.addEventListener("mouseout", closeProfile)
profile__box.addEventListener("mouseover", OpenProfile)
profile__box.addEventListener("mouseout", closeProfile)

function OpenProfile() {
    profile__box.classList.add("profile__box-display-flex")
      //esse estilo faz com que a profile-box tenha um display: flex.
}

function closeProfile() {
    profile__box.classList.remove("profile__box-display-flex")
}
