const menuButton = document.querySelector(".menu-button");
const navigation = document.querySelector(".primary-nav");
const regionSelector = document.querySelector("#region-selector");
// 방문 세션당 한 번만 지역 선택 창을 띄움 (사이트 안에서 둘러볼 때는 다시 뜨지 않음)
let regionSelectorSeen = false;
try {
  regionSelectorSeen = sessionStorage.getItem("regionSelectorSeen") === "1";
  sessionStorage.setItem("regionSelectorSeen", "1");
} catch {}
const cameFromSite = document.referrer && new URL(document.referrer).origin === window.location.origin;
if (!regionSelectorSeen && !cameFromSite) {
  regionSelector.showModal();
}

menuButton.addEventListener("click", () => {
  const isOpen = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!isOpen));
  menuButton.setAttribute("aria-label", isOpen ? "메뉴 열기" : "메뉴 닫기");
  navigation.classList.toggle("open", !isOpen);
  document.body.classList.toggle("menu-open", !isOpen);
});

navigation.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "메뉴 열기");
    navigation.classList.remove("open");
    document.body.classList.remove("menu-open");
  });
});

const gradeTabs = document.querySelectorAll("[data-grade]");
gradeTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    gradeTabs.forEach((item) => {
      const isSelected = item === tab;
      item.setAttribute("aria-selected", String(isSelected));
      document.querySelector(`#grade-panel-${item.dataset.grade}`).hidden = !isSelected;
    });
  });
});

document.querySelector("#year").textContent = new Date().getFullYear();