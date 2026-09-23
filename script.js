const gradeContent = {
  elementary: {
    kicker: "수학 자신감의 시작",
    title: "개념을 말로 설명하는 힘을 키웁니다.",
    description: "연산 정확도와 기초 개념을 단단히 잡고, 풀이 과정을 자신의 말로 표현하는 습관을 만듭니다.",
    points: ["교과 개념 이해와 연산 습관", "서술형 풀이 과정 연습", "중등 수학을 위한 기초 사고력"],
  },
  middle: {
    kicker: "내신과 개념을 동시에",
    title: "빈틈 없는 개념이 성적의 기준이 됩니다.",
    description: "학교별 진도에 맞춰 핵심 개념을 연결하고, 유형별 풀이와 오답 분석으로 시험 대응력을 높입니다.",
    points: ["학교 진도와 내신 시험 대비", "취약 단원 집중 보완", "풀이 근거를 찾는 사고 훈련"],
  },
  high: {
    kicker: "목표에서 역산하는 학습",
    title: "문제를 해석하고 전략을 세우는 힘을 기릅니다.",
    description: "현재 등급과 목표를 바탕으로 개념, 기출, 실전 훈련의 비중을 설계하고 안정적인 풀이 루틴을 만듭니다.",
    points: ["내신과 모의고사 학습 설계", "기출 문제 분석과 유형 연결", "시간 관리와 실전 풀이 점검"],
  },
};

const menuButton = document.querySelector(".menu-button");
const navigation = document.querySelector(".primary-nav");

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

const gradePanel = document.querySelector(".grade-panel");
document.querySelectorAll("[data-grade]").forEach((tab) => {
  tab.addEventListener("click", () => {
    const content = gradeContent[tab.dataset.grade];
    document.querySelectorAll("[data-grade]").forEach((item) => item.setAttribute("aria-selected", "false"));
    tab.setAttribute("aria-selected", "true");
    gradePanel.innerHTML = `
      <p class="grade-kicker">${content.kicker}</p>
      <h3>${content.title}</h3>
      <p class="grade-description">${content.description}</p>
      <ul class="grade-points">${content.points.map((point) => `<li>${point}</li>`).join("")}</ul>
    `;
  });
});

const consultationForm = document.querySelector("#consult-form");
const formStatus = consultationForm.querySelector(".form-status");

consultationForm.addEventListener("submit", (event) => {
  if (!consultationForm.checkValidity()) {
    event.preventDefault();
    consultationForm.reportValidity();
    return;
  }
  formStatus.textContent = "상담 내용을 전송하고 있습니다.";
});

if (new URLSearchParams(window.location.search).get("submitted") === "true") {
  formStatus.textContent = "상담 신청이 완료되었습니다. 확인 후 연락드리겠습니다.";
}

document.querySelector("#year").textContent = new Date().getFullYear();