/** Accessible, dependency-free mobile navigation enhancement. */
document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.getElementById("menu-toggle");
  const navigation = document.getElementById("primary-nav");

  if (!menuButton || !navigation) return;

  document.documentElement.classList.add("has-js");
  const buttonLabel = menuButton.querySelector(".sr-only");

  const closeNavigation = ({ restoreFocus = false } = {}) => {
    menuButton.setAttribute("aria-expanded", "false");
    navigation.classList.remove("is-open");
    if (buttonLabel) buttonLabel.textContent = "Open navigation";
    if (restoreFocus) menuButton.focus();
  };

  menuButton.addEventListener("click", () => {
    const isExpanded = menuButton.getAttribute("aria-expanded") === "true";
    if (isExpanded) {
      closeNavigation();
      return;
    }

    menuButton.setAttribute("aria-expanded", "true");
    navigation.classList.add("is-open");
    if (buttonLabel) buttonLabel.textContent = "Close navigation";
  });

  navigation.querySelectorAll("a").forEach((navigationLink) => {
    navigationLink.addEventListener("click", () => closeNavigation());
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
      closeNavigation({ restoreFocus: true });
    }
  });
});
