hamburger = document.querySelector(".__hamburger");
hamburgerMenu = document.querySelector(".__navbar-menu ul");
hamburgerMenuItems = document.querySelectorAll("ul li");
mobileNav = false;
hamburger.addEventListener("click", this.mobileNavOpen);

function mobileNavOpen() {
  if (mobileNav === false) {
    mobileNav = true;
    hamburgerMenu.classList.add("__navbar-menu-open");
    hamburgerMenu.classList.remove("__navbar-menu-close");
  } else {
    mobileNav = false;
    hamburgerMenu.classList.remove("__navbar-menu-open");
    hamburgerMenu.classList.add("__navbar-menu-close");
  }
}

hamburgerMenuItems.forEach((link) => {
  link.addEventListener("click", () => {
    mobileNav = false;
    hamburgerMenu.classList.remove("__navbar-menu-open");
    hamburgerMenu.classList.add("__navbar-menu-close");
  });
});