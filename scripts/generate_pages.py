"""지역·학년별 수학과외 페이지와 sitemap.xml을 생성합니다.

생성 대상
- regions/{구군}/{동}.html          : 동·읍·면별 안내 페이지
- regions/{구군}/{학년}-math.html   : 구군 + 초등/중등/고등 수학과외 페이지
- math/{학년}.html                  : 울산 전체 초등/중등/고등 수학과외 페이지
- sitemap.xml

사용법: python scripts/generate_pages.py
"""
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://classfit.kr/"
PHONE = "010-2928-3614"
TEL = "tel:01029283614"
OG_IMAGE = "https://classfit.kr/assets/social-preview.png?v=20261008-1"
TODAY = date.today().isoformat()

REGIONS = [
    {"name": "중구", "slug": "jung-gu", "type": "동", "areas": [
        ("학성동", "hakseong-dong"), ("반구1동", "bangu-1-dong"), ("반구2동", "bangu-2-dong"), ("복산동", "boksan-dong"),
        ("성안동", "seongan-dong"), ("중앙동", "jungang-dong"), ("우정동", "ujeong-dong"), ("태화동", "taehwa-dong"),
        ("다운동", "daun-dong"), ("병영1동", "byeongyeong-1-dong"), ("병영2동", "byeongyeong-2-dong"), ("약사동", "yaksa-dong"),
    ]},
    {"name": "남구", "slug": "nam-gu", "type": "동", "areas": [
        ("신정1동", "sinjeong-1-dong"), ("신정2동", "sinjeong-2-dong"), ("신정3동", "sinjeong-3-dong"), ("신정4동", "sinjeong-4-dong"),
        ("신정5동", "sinjeong-5-dong"), ("달동", "dal-dong"), ("삼산동", "samsan-dong"), ("삼호동", "samho-dong"),
        ("무거동", "mugeo-dong"), ("옥동", "ok-dong"), ("야음장생포동", "yaeum-jangsaengpo-dong"), ("대현동", "daehyeon-dong"),
        ("수암동", "suam-dong"), ("선암동", "seonam-dong"),
    ]},
    {"name": "동구", "slug": "dong-gu", "type": "동", "areas": [
        ("방어동", "bangeo-dong"), ("일산동", "ilsan-dong"), ("화정동", "hwajeong-dong"), ("대송동", "daesong-dong"),
        ("전하1동", "jeonha-1-dong"), ("전하2동", "jeonha-2-dong"), ("남목1동", "nammok-1-dong"), ("남목2동", "nammok-2-dong"),
        ("남목3동", "nammok-3-dong"),
    ]},
    {"name": "북구", "slug": "buk-gu", "type": "동", "areas": [
        ("농소1동", "nongso-1-dong"), ("농소2동", "nongso-2-dong"), ("농소3동", "nongso-3-dong"), ("강동동", "gangdong-dong"),
        ("효문동", "hyomun-dong"), ("송정동", "songjeong-dong"), ("양정동", "yangjeong-dong"), ("염포동", "yeompo-dong"),
    ]},
    {"name": "울주군", "slug": "ulju-gun", "type": "읍·면", "areas": [
        ("온산읍", "onsan-eup"), ("언양읍", "eonyang-eup"), ("온양읍", "onyang-eup"), ("범서읍", "beomseo-eup"),
        ("청량읍", "cheongnyang-eup"), ("삼남읍", "samnam-eup"), ("서생면", "seosaeng-myeon"), ("웅촌면", "ungchon-myeon"),
        ("두동면", "dudong-myeon"), ("두서면", "duseo-myeon"), ("상북면", "sangbuk-myeon"), ("삼동면", "samdong-myeon"),
    ]},
]


def region_label(region):
    # 울주군은 "울산 울주군"보다 "울주군"으로 더 많이 검색되지만, 지역명 일관성을 위해 울산을 붙입니다.
    return f"울산 {region['name']}"


# 학년별 콘텐츠. {R}은 "울산", "울산 중구" 같은 지역명으로 바뀝니다.
GRADES = [
    {
        "key": "elementary", "label": "초등", "eyebrow": "ELEMENTARY MATH",
        "title": "{R} 초등 수학과외 | 초등 수학수업·기초수학 1:1 무료체험",
        "description": "{R} 초등 수학과외. 연산·개념·문장제까지 초등 기초수학을 1:1로 잡는 맞춤 수학수업과 초등 수학공부 습관 관리, 무료체험수업을 안내합니다.",
        "h1": "<em>{R} 초등 수학과외</em><br>기초수학부터 단단하게",
        "hero": "{R} 초등학생의 연산 습관과 개념 이해도를 먼저 살펴보고, 학생 속도에 맞춘 1:1 초등 수학수업으로 수학 자신감을 키웁니다.",
        "intro_h2": "초등 수학공부,<br>습관이 실력이 됩니다.",
        "intro": "<strong>{R} 초등 수학</strong>은 지금 배우는 단원만이 아니라 중학교 수학의 바탕이 됩니다. 연산 정확도, 개념을 말로 설명하는 힘, 문장제를 읽고 식으로 바꾸는 과정을 차근차근 점검하며 초등 기초수학을 탄탄하게 다집니다.",
        "stages": [
            ("초1~2", "수 감각과 연산 기초", "수의 크기와 자릿값, 덧셈·뺄셈, 곱셈구구의 원리를 그림과 구체물로 이해하며 계산 습관을 바르게 만듭니다."),
            ("초3~4", "곱셈·나눗셈·분수", "두 자리 이상의 곱셈과 나눗셈, 분수와 소수의 개념, 도형과 측정을 연결해 기초수학의 폭을 넓힙니다."),
            ("초5~6", "중등 수학 준비", "약수와 배수, 분수의 계산, 비와 비율, 도형의 넓이와 부피를 익히며 중학교 수학의 기반을 만듭니다."),
        ],
        "concerns": [
            "계산 실수가 잦고 연산 속도가 느린 학생",
            "문장제 문제를 읽고 식을 세우기 어려워하는 학생",
            "수학을 어려워하거나 자신감이 떨어진 학생",
            "중학교 진학 전 초등 수학 개념을 정리하고 싶은 학생",
        ],
        "faqs": [
            ("초등학생도 1:1 수학과외가 필요할까요?",
             "초등 수학은 연산 습관과 개념 이해가 자리 잡는 시기입니다. 1:1 수업에서는 학생이 어디에서 막히는지 바로 확인하고, 잘못된 풀이 습관을 일찍 바로잡을 수 있습니다."),
            ("기초수학이 많이 부족한데 따라갈 수 있을까요?",
             "현재 학년보다 앞선 내용이 아니라, 막히기 시작한 단원부터 다시 짚습니다. 이전 학년 개념까지 연결해 빈틈을 채운 뒤 현재 진도로 돌아옵니다."),
            ("선행 학습도 가능한가요?",
             "현재 학년 개념이 충분히 이해된 경우 학생 속도에 맞춰 다음 학기 내용을 준비합니다. 무리한 선행보다 이해 중심의 진도를 권합니다."),
        ],
        "card": "수학수업 · 수학공부 · 기초수학",
    },
    {
        "key": "middle", "label": "중등", "eyebrow": "MIDDLE SCHOOL MATH",
        "title": "{R} 중등 수학과외 | 중학생 수학내신·기초수학 1:1 무료체험",
        "description": "{R} 중등 수학과외. 학교별 진도에 맞춘 중등 수학내신 대비, 기초수학 보완, 서술형 풀이까지 1:1 중학생 수학수업과 무료체험수업을 안내합니다.",
        "h1": "<em>{R} 중등 수학과외</em><br>수학내신과 개념을 함께",
        "hero": "{R} 중학생의 학교 진도와 시험 범위를 확인하고, 개념의 빈틈부터 내신 서술형까지 1:1 중등 수학수업으로 준비합니다.",
        "intro_h2": "중등 수학공부,<br>개념이 내신을 결정합니다.",
        "intro": "<strong>{R} 중등 수학</strong>은 학교마다 진도와 출제 경향이 다릅니다. 학교 진도에 맞춰 핵심 개념을 연결하고, 유형별 풀이와 오답 분석, 서술형 연습으로 중등 수학내신 대비와 기초수학 보완을 함께 진행합니다.",
        "stages": [
            ("중1", "수와 식의 기초", "정수와 유리수, 문자와 식, 일차방정식, 좌표평면과 그래프, 기본 도형으로 중등 수학의 기초를 세웁니다."),
            ("중2", "연립방정식과 함수", "유리수와 순환소수, 식의 계산, 연립방정식, 일차함수, 도형의 성질과 확률을 내신 유형과 함께 익힙니다."),
            ("중3", "고등 수학 연결", "제곱근과 실수, 인수분해, 이차방정식, 이차함수, 삼각비, 원의 성질로 고등 수학과의 연결을 준비합니다."),
        ],
        "concerns": [
            "중학교에 올라와 수학 점수가 갑자기 떨어진 학생",
            "개념은 아는데 시험에서 실수가 많은 학생",
            "서술형 풀이 과정을 정리하기 어려워하는 학생",
            "고등학교 진학 전 중등 수학을 다시 정리하고 싶은 학생",
        ],
        "faqs": [
            ("학교별 수학내신 대비가 가능한가요?",
             "학생이 다니는 학교의 진도와 시험 범위를 확인해 수업 계획을 세웁니다. 교과서와 학교 프린트, 학생의 오답을 바탕으로 시험 전 핵심 유형과 서술형을 점검합니다."),
            ("중학생인데 초등 기초수학부터 다시 해야 할까요?",
             "진단 결과 막힌 지점이 이전 학년 개념이라면 필요한 부분만 짧게 짚고 현재 진도와 연결합니다. 처음부터 다시 하기보다 빈틈을 골라 채우는 방식입니다."),
            ("중3인데 고등 수학 준비는 언제 시작하면 좋을까요?",
             "중3 내용 중 인수분해, 이차방정식, 이차함수가 고등 수학의 바탕이 됩니다. 이 단원의 이해도를 먼저 확인한 뒤 학생 상황에 맞춰 고등 수학 준비 시점을 정합니다."),
        ],
        "card": "수학내신 · 수학공부 · 기초수학",
    },
    {
        "key": "high", "label": "고등", "eyebrow": "HIGH SCHOOL MATH",
        "title": "{R} 고등 수학과외 | 고등 수학내신·수능수학 대비 1:1 무료체험",
        "description": "{R} 고등 수학과외. 고등 수학내신, 수능대비 수능수학, 부족한 기초수학 보완까지 목표 등급에 맞춘 1:1 고등 수학수업과 무료체험수업을 안내합니다.",
        "h1": "<em>{R} 고등 수학과외</em><br>내신부터 수능수학까지",
        "hero": "{R} 고등학생의 현재 등급과 목표를 바탕으로 내신, 모의고사, 수능대비의 비중을 설계하는 1:1 고등 수학수업입니다.",
        "intro_h2": "고등 수학공부,<br>목표에서 거꾸로 설계합니다.",
        "intro": "<strong>{R} 고등 수학</strong>은 내신과 수능을 함께 준비해야 합니다. 학교 시험 범위에 맞춘 고등 수학내신 대비, 기출 분석 중심의 수능수학 훈련, 막히는 단원을 위한 기초수학 보완을 학생 상황에 맞게 배분합니다.",
        "stages": [
            ("고1", "공통수학 내신", "다항식, 방정식과 부등식, 경우의 수, 행렬, 도형의 방정식, 집합과 명제, 함수를 학교 진도에 맞춰 다집니다."),
            ("고2", "선택과목과 모의고사", "대수, 미적분, 확률과 통계 등 학교별 편성 과목의 내신을 준비하며 모의고사 유형에 익숙해집니다."),
            ("고3", "수능대비 실전", "수능수학 기출 분석과 실전 모의고사, 시간 배분 훈련으로 목표 등급에 맞춘 수능대비를 진행합니다."),
        ],
        "concerns": [
            "고등학교에 올라와 수학 내신 등급이 떨어진 학생",
            "모의고사에서 시간이 부족하거나 킬러 문항 앞에서 막히는 학생",
            "중학교 개념이 부족해 고등 수학을 따라가기 어려운 학생",
            "수능 수학 목표 등급에 맞춘 학습 계획이 필요한 학생",
        ],
        "faqs": [
            ("고등 수학내신과 수능대비를 함께 할 수 있나요?",
             "시험 기간에는 학교 내신 범위에 집중하고, 그 외 기간에는 기출 분석과 수능수학 유형 훈련의 비중을 높입니다. 학년과 목표에 따라 두 과정의 비율을 조정합니다."),
            ("기초가 부족한 고등학생도 가능한가요?",
             "진단으로 막힌 단원을 찾은 뒤, 고등 수학에 필요한 중등 개념만 골라 빠르게 보완합니다. 기초수학 보완과 현재 진도를 병행해 내신 공백이 생기지 않도록 합니다."),
            ("수능 수학은 언제부터 준비하면 좋을까요?",
             "고1·고2 내신 개념이 곧 수능 수학의 바탕입니다. 학년별 내신을 충실히 하면서 모의고사와 기출 문제로 수능 유형에 일찍 익숙해지는 것을 권합니다."),
        ],
        "card": "수학내신 · 수능대비 · 수능수학",
    },
]

COMMON_FAQ = ("무료체험수업은 어떻게 신청하나요?",
              f"{PHONE}로 전화 주시면 학생의 학년과 현재 학습 상황을 듣고, 무료체험수업 일정과 수업 방향을 안내해 드립니다.")


def json_ld(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'


def breadcrumb_ld(items):
    return json_ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + path}
            for i, (name, path) in enumerate(items)
        ],
    })


def faq_ld(faqs):
    return json_ld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    })


def head(*, title, description, path, root, css, extra=""):
    url = SITE + path
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="울산 수학과외">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="{root}assets/logo-mark.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css}">
  {extra}
</head>"""


def header(root, links):
    nav = "".join(f'<a href="{href}">{text}</a>' for text, href in links)
    return f"""<body>
  <header class="region-header">
    <a class="brand" href="{root}"><img class="brand-mark" src="{root}assets/logo-mark.svg" alt=""><span>울산 수학과외<small>1:1 맞춤 수업</small></span></a>
    <nav class="region-nav" aria-label="지역 페이지 메뉴">{nav}<a class="call-link" href="{TEL}">☎ {PHONE}</a></nav>
  </header>"""


def footer(root):
    return f"""  <footer class="region-footer"><a class="brand" href="{root}"><img class="brand-mark" src="{root}assets/logo-mark.svg" alt=""><span>울산 수학과외<small>1:1 맞춤 수업</small></span></a><p>상담 문의 <a href="{TEL}">{PHONE}</a></p><p>© 2026 ULSAN MATH TUTORING.</p></footer>
</body>
</html>
"""


def breadcrumb_nav(items):
    parts = []
    for i, (name, href) in enumerate(items):
        if i:
            parts.append("<span>›</span>")
        parts.append(f'<a href="{href}">{name}</a>' if href else name)
    return f'<nav class="breadcrumb" aria-label="현재 위치">{"".join(parts)}</nav>'


def links_block(title, links):
    items = "".join(
        f'<a{" aria-current=\"page\"" if current else ""} href="{href}">{text}</a>'
        for text, href, current in links
    )
    return f'<section class="other-areas"><h2>{title}</h2><div class="area-links">{items}</div></section>'


def trial_band(heading):
    return f"""<section class="trial-band"><div><h2>{heading}</h2><p>전화 상담 후 학생에게 맞는 체험수업 방향을 안내해 드립니다.</p></div><div class="trial-actions"><a class="button button-primary" href="{TEL}">무료체험 전화 상담</a><a class="button button-outline" href="{TEL}">{PHONE}</a></div></section>"""


def grade_page(grade, *, place, path, root, css, crumbs, crumb_ld, sibling_links, local_links, local_title, cross_links, cross_title):
    fmt = lambda s: s.replace("{R}", place)
    faqs = [(fmt(q), fmt(a)) for q, a in grade["faqs"]] + [COMMON_FAQ]
    stages = "".join(
        f'<article class="feature"><span>{s[0]}</span><h3>{s[1]}</h3><p>{s[2]}</p></article>' for s in grade["stages"]
    )
    concerns = "".join(f"<li>{c}</li>" for c in grade["concerns"])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    title = fmt(grade["title"])
    return f"""{head(title=title, description=fmt(grade["description"]), path=path, root=root, css=css,
                 extra=breadcrumb_ld(crumb_ld) + faq_ld(faqs))}
{header(root, [("지역별 안내", crumbs[1][1]), ("학년별 수업", "#stages")])}
  <main>
    {breadcrumb_nav(crumbs)}
    <section class="area-hero"><p class="eyebrow">{grade["eyebrow"]}</p><h1>{fmt(grade["h1"])}</h1><p>{fmt(grade["hero"])}</p><div class="hero-actions"><a class="button button-primary" href="{TEL}">무료체험 전화 상담</a><a class="button button-outline" href="#faq">자주 묻는 질문</a></div></section>
    <section class="content-section" id="stages"><div class="section-intro"><div><p class="eyebrow">CURRICULUM</p><h2>{grade["intro_h2"]}</h2></div><div><p>{fmt(grade["intro"])}</p></div></div><div class="feature-grid">{stages}</div></section>
    <section class="check-section"><h2>이런 학생에게 맞습니다</h2><ul class="check-list">{concerns}</ul></section>
    <section class="faq-section" id="faq"><h2>{place} {grade["label"]} 수학과외 자주 묻는 질문</h2><div class="faq-list">{faq_html}</div></section>
    {trial_band(f"{place} {grade['label']} 수학과외,<br>무료체험수업으로 시작하세요.")}
    {links_block(f"{place} 학년별 수학과외", sibling_links)}
    {links_block(local_title, local_links) if local_links else ""}
    {links_block(cross_title, cross_links)}
  </main>
{footer(root)}"""


def area_page(region, area_name, area_slug):
    root, gu = "../../", region_label(region)
    place = f"{gu} {area_name}"
    path = f"regions/{region['slug']}/{area_slug}.html"
    title = f"{place} 수학과외 | 초등·중등·고등 수학수업 1:1 무료체험"
    description = f"{place} 수학과외. 초등 기초수학, 중등 수학내신, 고등 수능수학까지 학생 수준에 맞춘 1:1 수학수업과 무료체험수업을 안내합니다. 상담 {PHONE}"
    crumbs = [("홈", root), ("지역별 수학과외", "../"), (region["name"], f"../{region['slug']}.html"), (area_name, None)]
    crumb_ld = [("홈", ""), ("지역별 수학과외", "regions/"), (gu, f"regions/{region['slug']}.html"), (place, path)]
    grade_cards = "".join(
        f'<a class="grade-card" href="{g["key"]}-math.html"><span>{g["eyebrow"]}</span><strong>{area_name} {g["label"]} 수학</strong><small>{g["card"]} →</small></a>'
        for g in GRADES
    )
    area_links = [(name, f"{slug}.html", slug == area_slug) for name, slug in region["areas"]]
    return f"""{head(title=title, description=description, path=path, root=root, css="../region-styles.css", extra=breadcrumb_ld(crumb_ld))}
{header(root, [("지역별 안내", "../"), (f"{region['name']} 안내", f"../{region['slug']}.html")])}
  <main>
    {breadcrumb_nav(crumbs)}
    <section class="area-hero">
      <p class="eyebrow">ULSAN LOCAL MATH TUTORING</p>
      <h1><em>{place}</em><br>수학과외 무료체험수업 안내</h1>
      <p>{area_name} 초등·중등·고등 학생의 현재 수준과 목표를 살펴보고, 학교 진도와 학습 속도에 맞는 1:1 수학 공부 방향을 설계합니다.</p>
      <div class="hero-actions"><a class="button button-primary" href="{TEL}">무료체험 전화 상담</a><a class="button button-outline" href="#grades">학년별 수업 보기</a></div>
    </section>
    <section class="content-section">
      <div class="section-intro"><div><p class="eyebrow">PERSONALIZED LESSON</p><h2>{area_name} 학생에게 맞는<br>공부 흐름을 만듭니다.</h2></div><div><p><strong>{place} 수학과외</strong>는 정답만 알려주지 않습니다. 개념의 빈틈과 풀이 습관을 진단하고, 이해·적용·복습의 과정을 학생의 속도에 맞춰 이어갑니다.</p></div></div>
      <div class="feature-grid"><article class="feature"><span>01 DIAGNOSIS</span><h3>현재 수준 진단</h3><p>개념 이해도와 문제 풀이 과정을 확인해 먼저 보완할 부분을 찾습니다.</p></article><article class="feature"><span>02 LESSON</span><h3>학년별 맞춤 수업</h3><p>초등 기초수학, 중등 수학내신, 고등 수능수학까지 목표에 맞게 수업의 순서와 속도를 정합니다.</p></article><article class="feature"><span>03 MANAGEMENT</span><h3>복습과 오답 관리</h3><p>수업 후 복습과 오답 점검으로 혼자 공부할 수 있는 학습 습관을 기릅니다.</p></article></div>
    </section>
    <section class="grade-section" id="grades"><h2>{area_name} 학년별 수학 수업</h2><p>{place} 초등·중등·고등 수학수업 안내를 확인하세요.</p><div class="grade-cards">{grade_cards}</div></section>
    {trial_band(f"{area_name} 수학과외,<br>무료체험수업으로 시작하세요.")}
    {links_block(f"{region['name']} 다른 {region['type']} 수학과외", area_links)}
  </main>
{footer(root)}"""


def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def main():
    urls = [("", "weekly", "1.0"), ("regions/", "monthly", "0.9")]
    urls += [(f"math/{g['key']}.html", "monthly", "0.9") for g in GRADES]
    urls += [(f"regions/{r['slug']}.html", "monthly", "0.8") for r in REGIONS]
    grade_urls, area_urls = [], []

    # 울산 전체 학년별 페이지
    for grade in GRADES:
        path = f"math/{grade['key']}.html"
        name = f"울산 {grade['label']} 수학과외"
        write(path, grade_page(
            grade, place="울산", path=path, root="../", css="../regions/region-styles.css",
            crumbs=[("홈", "../"), ("지역별 수학과외", "../regions/"), (name, None)],
            crumb_ld=[("홈", ""), ("지역별 수학과외", "regions/"), (name, path)],
            sibling_links=[(f"울산 {g['label']} 수학과외", f"{g['key']}.html", g is grade) for g in GRADES],
            local_links=None, local_title="",
            cross_title=f"구·군별 {grade['label']} 수학과외",
            cross_links=[(f"{region_label(r)} {grade['label']} 수학", f"../regions/{r['slug']}/{grade['key']}-math.html", False) for r in REGIONS],
        ))

    for region in REGIONS:
        folder = ROOT / "regions" / region["slug"]
        if folder.exists():
            shutil.rmtree(folder)
        gu = region_label(region)

        # 구·군 학년별 페이지
        for grade in GRADES:
            path = f"regions/{region['slug']}/{grade['key']}-math.html"
            name = f"{gu} {grade['label']} 수학과외"
            write(path, grade_page(
                grade, place=gu, path=path, root="../../", css="../region-styles.css",
                crumbs=[("홈", "../../"), ("지역별 수학과외", "../"), (region["name"], f"../{region['slug']}.html"), (f"{grade['label']} 수학과외", None)],
                crumb_ld=[("홈", ""), ("지역별 수학과외", "regions/"), (gu, f"regions/{region['slug']}.html"), (name, path)],
                sibling_links=[(f"{gu} {g['label']} 수학과외", f"{g['key']}-math.html", g is grade) for g in GRADES],
                local_title=f"{region['name']} {region['type']}별 수학과외",
                local_links=[(n, f"{s}.html", False) for n, s in region["areas"]],
                cross_title=f"다른 지역 {grade['label']} 수학과외",
                cross_links=[(f"울산 전체 {grade['label']} 수학", f"../../math/{grade['key']}.html", False)]
                + [(f"{region_label(r)} {grade['label']} 수학", f"../{r['slug']}/{grade['key']}-math.html", False) for r in REGIONS if r is not region],
            ))
            grade_urls.append(path)

        # 동·읍·면 페이지
        for area_name, area_slug in region["areas"]:
            path = f"regions/{region['slug']}/{area_slug}.html"
            write(path, area_page(region, area_name, area_slug))
            area_urls.append(path)

    urls += [(u, "monthly", "0.8") for u in grade_urls]
    urls += [(u, "monthly", "0.7") for u in area_urls]
    entries = "\n".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{f}</changefreq>\n    <priority>{p}</priority>\n  </url>"
        for u, f, p in urls
    )
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n')
    print(f"Generated {len(GRADES)} Ulsan grade pages, {len(grade_urls)} region grade pages, {len(area_urls)} area pages, {len(urls)} sitemap URLs.")


if __name__ == "__main__":
    main()
