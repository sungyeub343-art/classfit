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


# 학년별 세부 페이지 (math/{key}.html). parent는 상위 학교급 GRADES의 key입니다.
# 2026년 기준: 중1·중2·고1·고2는 2022 개정 교육과정, 중3·고3은 2015 개정 교육과정이 적용됩니다.
YEARS = [
    {
        "key": "pre-middle-1", "parent": "middle", "label": "예비중1", "eyebrow": "PRE MIDDLE SCHOOL",
        "title": "{R} 예비중1 수학과외 | 초6 중학수학 준비·초등 수학 총정리 1:1",
        "description": "{R} 예비중1 수학과외. 초등 수학 빈틈 점검부터 중1 수학 예습까지, 중학교 첫 시험을 대비하는 초6·예비중1 1:1 수학수업과 무료체험수업을 안내합니다.",
        "h1": "<em>{R} 예비중1 수학과외</em><br>중학교 수학의 첫 단추",
        "hero": "{R} 초6·예비중1 학생의 초등 수학 이해도를 점검하고, 중1 수학으로 자연스럽게 넘어가는 1:1 수학수업을 설계합니다.",
        "intro_h2": "예비중1 수학공부,<br>복습과 예습의 균형",
        "intro": "<strong>{R} 예비중1 수학</strong>은 무리한 선행보다 초등 수학의 빈틈을 먼저 채우는 것이 중요합니다. 분수와 소수의 계산, 비와 비율처럼 중학교 수학으로 이어지는 단원을 점검한 뒤, 소인수분해와 정수와 유리수 같은 중1 1학기 내용을 차근차근 예습합니다.",
        "stages": [
            ("STEP 1", "초등 수학 총정리", "분수·소수의 계산, 비와 비율, 도형의 넓이와 부피 등 중학교 수학의 바탕이 되는 초등 단원을 점검합니다."),
            ("STEP 2", "중1 1학기 예습", "소인수분해, 정수와 유리수, 문자의 사용과 식, 일차방정식을 학생 속도에 맞춰 미리 익힙니다."),
            ("STEP 3", "중학교 공부 습관", "개념 노트 정리, 오답 관리, 서술형 풀이 쓰기처럼 중학교 시험에 필요한 공부 습관을 만듭니다."),
        ],
        "concerns": [
            "초등 수학 개념에 빈틈이 있는지 확인하고 싶은 초6 학생",
            "중학교 수학이 어려워질까 걱정되는 예비중1 학생",
            "선행을 어디까지 해야 할지 고민인 학부모님",
            "스스로 공부하는 습관을 중학교 전에 만들고 싶은 학생",
        ],
        "faqs": [
            ("예비중1 수학은 언제 시작하면 좋을까요?",
             "초6 2학기 내용을 마무리하는 시기부터 겨울방학까지가 일반적입니다. 먼저 초등 수학의 빈틈을 확인하고, 결과에 따라 복습과 중1 예습의 비중을 정합니다."),
            ("중1 수학은 얼마나 선행해야 하나요?",
             "학생의 이해 속도에 따라 다릅니다. 중1 1학기 내용을 충분히 이해하고 들어가는 것을 우선 목표로 하고, 여유가 있으면 2학기 내용까지 넓혀 갑니다."),
            ("중학교 수학 시험은 초등과 무엇이 다른가요?",
             "학교별 지필평가와 수행평가가 있고, 풀이 과정을 쓰는 서술형 문항의 비중이 커집니다. 예비중1 시기부터 풀이 과정을 정리해 쓰는 연습을 함께 합니다."),
        ],
        "card": "초등 수학 총정리 · 중1 예습",
    },
    {
        "key": "middle-1", "parent": "middle", "label": "중1", "eyebrow": "MIDDLE SCHOOL 1",
        "title": "{R} 중1 수학과외 | 중학교 1학년 수학 개념·첫 내신 대비 1:1",
        "description": "{R} 중1 수학과외. 소인수분해, 정수와 유리수, 일차방정식부터 도형과 통계까지 중학교 1학년 수학 개념과 첫 내신 시험을 1:1 맞춤 수학수업으로 준비합니다.",
        "h1": "<em>{R} 중1 수학과외</em><br>중학 수학의 기초를 세우는 시기",
        "hero": "{R} 중학교 1학년 학생이 초등과 다른 중학교 수학에 적응하도록, 개념 이해부터 첫 내신 시험 준비까지 1:1로 함께합니다.",
        "intro_h2": "중1 수학공부,<br>기초가 3년을 좌우합니다.",
        "intro": "<strong>{R} 중1 수학</strong>에서 배우는 정수와 유리수, 문자와 식, 일차방정식은 중학교 3년과 고등 수학까지 이어지는 기초입니다. 개념을 정확히 이해하고 계산 실수를 줄이는 습관을 만들며, 학교별 일정에 맞춰 첫 내신 시험을 준비합니다.",
        "stages": [
            ("수와 연산", "소인수분해·정수와 유리수", "소인수분해와 최대공약수·최소공배수, 정수와 유리수의 사칙계산을 정확하게 익힙니다."),
            ("변화와 관계", "문자와 식·일차방정식", "문자를 사용한 식, 일차방정식의 풀이와 활용, 좌표평면과 그래프를 연결해 이해합니다."),
            ("도형과 자료", "기본 도형·통계", "기본 도형, 작도와 합동, 평면도형과 입체도형, 자료의 정리와 해석을 다룹니다."),
        ],
        "concerns": [
            "초등 때와 달리 중학교 수학이 어렵게 느껴지는 학생",
            "정수와 유리수 계산에서 부호 실수가 잦은 학생",
            "일차방정식 활용 문제에서 식을 세우기 어려워하는 학생",
            "중학교 첫 내신 시험을 처음부터 제대로 준비하고 싶은 학생",
        ],
        "faqs": [
            ("중1은 시험이 없나요?",
             "학교마다 자유학기 운영 방식과 지필평가 일정이 다릅니다. 시험이 없는 학기에도 수행평가와 단원평가가 있고, 다음 학기 내신의 바탕이 되므로 개념을 꾸준히 다져야 합니다. 다니는 학교의 일정을 확인해 수업 계획을 세웁니다."),
            ("중1 수학에서 가장 중요한 단원은 무엇인가요?",
             "정수와 유리수의 계산, 문자와 식, 일차방정식은 이후 모든 학년 수학의 기초가 됩니다. 이 단원에서 생긴 빈틈은 중2·중3에서 크게 드러나므로 정확하게 이해하고 넘어가도록 합니다."),
            ("중1인데 중2 선행을 해도 될까요?",
             "현재 학기 내용을 충분히 이해했다면 학생 속도에 맞춰 다음 학기와 중2 내용을 준비합니다. 진도보다 이해가 우선이므로 진단 결과를 보고 선행 범위를 정합니다."),
        ],
        "card": "정수와 유리수 · 일차방정식",
    },
    {
        "key": "middle-2", "parent": "middle", "label": "중2", "eyebrow": "MIDDLE SCHOOL 2",
        "title": "{R} 중2 수학과외 | 중학교 2학년 연립방정식·일차함수 내신 1:1",
        "description": "{R} 중2 수학과외. 식의 계산, 연립방정식, 일차함수, 도형의 성질과 닮음, 확률까지 중학교 2학년 수학내신을 1:1 맞춤 수학수업으로 대비합니다.",
        "h1": "<em>{R} 중2 수학과외</em><br>수학 성적이 갈리는 학년",
        "hero": "{R} 중학교 2학년 학생의 함수와 도형 이해도를 점검하고, 학교별 시험 범위에 맞춘 1:1 수학내신 대비 수업을 진행합니다.",
        "intro_h2": "중2 수학공부,<br>함수와 도형을 잡아야 합니다.",
        "intro": "<strong>{R} 중2 수학</strong>은 연립방정식과 일차함수, 도형의 성질과 닮음처럼 개념과 응용이 함께 어려워지는 학년입니다. 중1 기초에서 막힌 부분이 있다면 함께 보완하고, 내신 서술형과 고난도 유형까지 단계적으로 준비합니다.",
        "stages": [
            ("수와 식", "순환소수·식의 계산", "유리수와 순환소수, 지수법칙과 다항식의 계산, 일차부등식을 정확하게 익힙니다."),
            ("방정식과 함수", "연립방정식·일차함수", "연립일차방정식의 풀이와 활용, 일차함수의 그래프와 식, 일차함수와 일차방정식의 관계를 연결합니다."),
            ("도형과 확률", "도형의 성질·닮음·확률", "삼각형과 사각형의 성질, 도형의 닮음, 피타고라스 정리, 경우의 수와 확률을 다룹니다."),
        ],
        "concerns": [
            "중2가 되면서 수학 점수가 떨어지기 시작한 학생",
            "일차함수 그래프와 식이 연결되지 않는 학생",
            "도형 증명과 서술형 문제를 어려워하는 학생",
            "중1 내용에 빈틈이 있어 중2 진도를 따라가기 힘든 학생",
        ],
        "faqs": [
            ("중2 수학이 특히 어려운 이유는 무엇인가요?",
             "함수와 도형 증명처럼 추상적인 개념이 본격적으로 등장하고, 중1 내용을 바탕으로 응용 문제가 많아지기 때문입니다. 어디에서 막히는지 진단한 뒤 필요한 기초부터 연결합니다."),
            ("중2인데 중1 내용이 부족하면 어떻게 하나요?",
             "처음부터 다시 하기보다, 중2 단원에 필요한 중1 개념만 골라 짧게 보완하고 현재 진도로 돌아옵니다. 내신 일정에 지장이 없도록 비중을 조절합니다."),
            ("중2 내신 서술형은 어떻게 준비하나요?",
             "풀이 과정을 단계별로 쓰는 연습을 수업마다 하고, 학교 기출과 학생의 오답을 바탕으로 감점되기 쉬운 부분을 점검합니다."),
        ],
        "card": "연립방정식 · 일차함수 · 도형",
    },
    {
        "key": "middle-3", "parent": "middle", "label": "중3", "eyebrow": "MIDDLE SCHOOL 3",
        "title": "{R} 중3 수학과외 | 중학교 3학년 이차함수 내신·고등수학 준비 1:1",
        "description": "{R} 중3 수학과외. 제곱근과 실수, 인수분해, 이차방정식, 이차함수, 삼각비까지 중학교 3학년 수학내신과 고등 수학 준비를 1:1 맞춤 수학수업으로 진행합니다.",
        "h1": "<em>{R} 중3 수학과외</em><br>중등 수학을 마무리하고 고등으로",
        "hero": "{R} 중학교 3학년 학생의 내신을 챙기면서, 고등 수학의 바탕이 되는 인수분해·이차방정식·이차함수를 확실히 다지는 1:1 수학수업입니다.",
        "intro_h2": "중3 수학공부,<br>고등 수학의 출발점입니다.",
        "intro": "<strong>{R} 중3 수학</strong>에서 배우는 인수분해, 이차방정식, 이차함수는 고1 공통수학의 핵심 바탕입니다. 학교 내신을 안정적으로 준비하면서, 고등 수학에서 다시 쓰이는 개념을 정확히 이해하고 넘어가도록 수업을 설계합니다.",
        "stages": [
            ("수와 식", "제곱근과 실수·인수분해", "제곱근과 실수의 계산, 다항식의 곱셈과 인수분해를 고등 수학에서 막히지 않을 만큼 정확하게 익힙니다."),
            ("방정식과 함수", "이차방정식·이차함수", "이차방정식의 풀이와 활용, 이차함수의 그래프와 성질을 고1 공통수학과 연결해 이해합니다."),
            ("도형과 통계", "삼각비·원의 성질·통계", "삼각비, 원의 성질, 대푯값과 산포도, 상관관계를 내신 유형과 함께 정리합니다."),
        ],
        "concerns": [
            "인수분해와 이차방정식 계산이 아직 불안한 학생",
            "이차함수 그래프 문제에서 자주 막히는 학생",
            "중3 내신과 고등 수학 준비를 함께 하고 싶은 학생",
            "고등학교 진학 전 중등 수학 빈틈을 정리하고 싶은 학생",
        ],
        "faqs": [
            ("중3 내신과 고등 선행 중 무엇이 먼저인가요?",
             "중3 내용 자체가 고등 수학의 바탕이므로 현재 학기 내신을 충실히 하는 것이 먼저입니다. 내신이 안정되면 시험이 끝난 시기를 활용해 고1 공통수학 준비 비중을 높입니다."),
            ("중3 2학기에는 무엇을 준비해야 하나요?",
             "2학기 내신을 마무리한 뒤 겨울방학까지 중등 수학의 빈틈을 정리하고 고1 공통수학을 예습합니다. 자세한 내용은 예비고1 수학 안내를 참고해 주세요."),
            ("중3인데 중1·중2 내용이 많이 부족해요.",
             "중3 단원을 공부하면서 필요한 이전 학년 개념을 함께 보완합니다. 특히 식의 계산과 일차함수는 중3과 고등 수학에 직접 연결되므로 우선적으로 점검합니다."),
        ],
        "card": "인수분해 · 이차함수 · 고등 준비",
    },
    {
        "key": "pre-high-1", "parent": "high", "label": "예비고1", "eyebrow": "PRE HIGH SCHOOL",
        "title": "{R} 예비고1 수학과외 | 중3 겨울방학 공통수학 준비 1:1",
        "description": "{R} 예비고1 수학과외. 중등 수학 빈틈 정리부터 고1 공통수학1·2 예습까지, 고등학교 첫 내신을 준비하는 중3·예비고1 1:1 수학수업과 무료체험수업을 안내합니다.",
        "h1": "<em>{R} 예비고1 수학과외</em><br>고등학교 첫 내신을 준비합니다",
        "hero": "{R} 중3·예비고1 학생의 중등 수학 빈틈을 점검하고, 고1 공통수학을 학생 속도에 맞춰 준비하는 1:1 수학수업입니다.",
        "intro_h2": "예비고1 수학공부,<br>겨울방학이 중요합니다.",
        "intro": "<strong>{R} 예비고1 수학</strong>은 고등학교 첫 시험 전에 중등 수학의 빈틈을 정리하고 고1 공통수학을 미리 익히는 과정입니다. 특히 인수분해, 이차방정식, 이차함수처럼 고등 수학에서 바로 쓰이는 개념을 먼저 다진 뒤, 다항식과 방정식·부등식부터 차례로 예습합니다.",
        "stages": [
            ("STEP 1", "중등 핵심 단원 정리", "식의 계산, 인수분해, 이차방정식, 일차·이차함수처럼 고등 수학에 직접 연결되는 중등 단원을 점검합니다."),
            ("STEP 2", "공통수학1 예습", "다항식의 연산, 항등식과 나머지정리, 복소수와 이차방정식, 이차방정식과 이차함수, 여러 가지 방정식과 부등식을 익힙니다."),
            ("STEP 3", "고등 공부 방식 적응", "늘어난 학습량에 맞춰 개념 복습, 유형 연습, 오답 정리의 루틴을 만들어 고1 첫 내신에 대비합니다."),
        ],
        "concerns": [
            "중3 겨울방학에 무엇부터 공부해야 할지 막막한 학생",
            "중등 수학에 빈틈이 있어 고등 수학이 걱정되는 학생",
            "고1 첫 중간고사를 제대로 준비하고 싶은 학생",
            "선행 범위와 속도를 상담받고 싶은 학부모님",
        ],
        "faqs": [
            ("예비고1 수학은 어디까지 선행해야 하나요?",
             "학생의 중등 수학 이해도에 따라 다릅니다. 고1 1학기 내신 범위인 공통수학1을 충분히 이해하는 것을 우선 목표로 하고, 여유가 있으면 공통수학2까지 넓혀 갑니다."),
            ("중등 수학이 부족한데 바로 고등 수학을 해도 될까요?",
             "고등 수학에서 바로 쓰이는 중등 단원을 먼저 짧게 정리하는 것을 권합니다. 인수분해와 이차함수가 흔들리면 공통수학1 진도가 나가도 내신에서 실수가 반복되기 쉽습니다."),
            ("고등학교 내신은 중학교와 무엇이 다른가요?",
             "시험 범위와 학습량이 크게 늘고, 같은 학년 학생들 사이의 상대평가로 등급이 정해집니다. 예비고1 시기에 고등학교 공부 루틴을 미리 만들어 두는 것이 도움이 됩니다."),
        ],
        "card": "중등 정리 · 공통수학 예습",
    },
    {
        "key": "high-1", "parent": "high", "label": "고1", "eyebrow": "HIGH SCHOOL 1",
        "title": "{R} 고1 수학과외 | 고등학교 1학년 공통수학 내신 1:1",
        "description": "{R} 고1 수학과외. 공통수학1·2의 다항식, 방정식과 부등식, 경우의 수, 행렬, 도형의 방정식, 집합과 명제, 함수까지 고등학교 1학년 수학내신을 1:1로 대비합니다.",
        "h1": "<em>{R} 고1 수학과외</em><br>공통수학 내신을 탄탄하게",
        "hero": "{R} 고등학교 1학년 학생의 공통수학 이해도를 점검하고, 학교별 시험 범위와 출제 경향에 맞춘 1:1 수학내신 대비 수업을 진행합니다.",
        "intro_h2": "고1 수학공부,<br>첫 내신이 방향을 정합니다.",
        "intro": "<strong>{R} 고1 수학</strong>은 공통수학1·2를 배우며 고등 수학 전체의 기초를 세우는 학년입니다. 첫 내신 등급이 이후 학습 계획에 큰 영향을 주므로, 개념 이해와 유형 연습, 학교 기출 분석을 함께 진행하고 부족한 중등 개념은 필요한 만큼 보완합니다.",
        "stages": [
            ("공통수학1", "다항식·방정식과 부등식", "다항식의 연산과 나머지정리, 인수분해, 복소수와 이차방정식, 이차함수, 여러 가지 방정식과 부등식을 다룹니다."),
            ("공통수학1", "경우의 수·행렬", "합의 법칙과 곱의 법칙, 순열과 조합, 행렬과 그 연산을 정확하게 익힙니다."),
            ("공통수학2", "도형의 방정식·집합·함수", "점과 직선, 원의 방정식, 도형의 이동, 집합과 명제, 함수와 그래프를 학교 진도에 맞춰 준비합니다."),
        ],
        "concerns": [
            "고등학교 첫 시험에서 생각보다 낮은 등급을 받은 학생",
            "중학교 때와 달리 시험 범위와 난도에 적응하기 어려운 학생",
            "개념은 아는데 응용 문제와 시간 배분에서 막히는 학생",
            "공통수학 내신과 모의고사를 함께 준비하고 싶은 학생",
        ],
        "faqs": [
            ("고1 첫 내신은 어떻게 준비해야 하나요?",
             "다니는 학교의 시험 범위와 교과서, 부교재, 기출 경향을 먼저 확인합니다. 시험 4~5주 전부터는 범위 내 개념 정리와 유형 연습, 실전 시간 훈련 순서로 준비합니다."),
            ("고1 수학 성적이 낮으면 이후에도 어려울까요?",
             "공통수학은 이후 대수, 미적분, 확률과 통계의 바탕이 되므로, 지금 빈틈을 채우면 다음 학년 수학이 훨씬 수월해집니다. 진단으로 원인을 찾아 우선순위를 정합니다."),
            ("고1부터 모의고사도 준비해야 하나요?",
             "고1 모의고사는 공통수학 범위 중심이라 내신 공부와 많이 겹칩니다. 시험 기간에는 내신에 집중하고, 그 외 기간에 모의고사 유형을 함께 연습합니다."),
        ],
        "card": "공통수학1 · 공통수학2 내신",
    },
    {
        "key": "high-2", "parent": "high", "label": "고2", "eyebrow": "HIGH SCHOOL 2",
        "title": "{R} 고2 수학과외 | 고등학교 2학년 대수·미적분·확률과 통계 내신 1:1",
        "description": "{R} 고2 수학과외. 대수, 미적분Ⅰ, 확률과 통계 등 학교별 편성 과목의 고등학교 2학년 수학내신과 모의고사, 수능대비를 1:1 맞춤 수학수업으로 준비합니다.",
        "h1": "<em>{R} 고2 수학과외</em><br>내신과 수능의 연결 고리",
        "hero": "{R} 고등학교 2학년 학생의 학교별 편성 과목을 확인하고, 내신과 모의고사를 함께 준비하는 1:1 수학수업을 진행합니다.",
        "intro_h2": "고2 수학공부,<br>수능의 범위가 시작됩니다.",
        "intro": "<strong>{R} 고2 수학</strong>에서 배우는 대수와 미적분Ⅰ, 확률과 통계는 수능 수학의 직접적인 범위입니다. 학교마다 과목 편성과 진도가 다르므로 다니는 학교 기준으로 내신을 준비하고, 기출과 모의고사 유형으로 수능대비의 기반을 함께 만듭니다.",
        "stages": [
            ("대수", "지수·로그·삼각함수·수열", "지수와 로그, 지수함수와 로그함수, 삼각함수, 수열을 개념부터 내신 고난도 유형까지 다룹니다."),
            ("미적분Ⅰ", "극한·미분·적분", "함수의 극한과 연속, 미분과 도함수의 활용, 적분을 그래프 해석과 함께 이해합니다."),
            ("확률과 통계", "경우의 수·확률·통계", "순열과 조합, 확률, 통계를 학교 편성에 맞춰 준비하고 모의고사 유형에 익숙해집니다."),
        ],
        "concerns": [
            "고2가 되면서 수학 과목이 늘어 부담이 커진 학생",
            "지수·로그와 삼각함수에서 막히는 학생",
            "내신과 모의고사 성적 차이가 큰 학생",
            "고3 전에 수능 수학의 기반을 만들고 싶은 학생",
        ],
        "faqs": [
            ("고2 수학 과목은 학교마다 다른가요?",
             "고교학점제에 따라 학교마다 학기별로 편성하는 과목과 진도가 다릅니다. 상담에서 다니는 학교의 편성표와 시험 범위를 확인하고 수업 계획을 세웁니다."),
            ("고2 때 수능 준비를 시작해야 하나요?",
             "고2에서 배우는 과목이 곧 수능 범위이므로 내신 공부가 수능 준비의 바탕이 됩니다. 시험이 없는 기간에 기출과 모의고사 문제로 수능 유형을 익히는 것을 권합니다."),
            ("고1 공통수학이 부족한데 고2 과목을 따라갈 수 있을까요?",
             "고2 단원에 필요한 공통수학 개념을 골라 함께 보완합니다. 특히 함수와 방정식·부등식은 대수와 미적분에서 계속 쓰이므로 우선 점검합니다."),
        ],
        "card": "대수 · 미적분Ⅰ · 확률과 통계",
    },
    {
        "key": "high-3", "parent": "high", "label": "고3", "eyebrow": "HIGH SCHOOL 3",
        "title": "{R} 고3 수학과외 | 수능수학 실전 대비·고3 내신 1:1",
        "description": "{R} 고3 수학과외. 수학Ⅰ·수학Ⅱ와 선택과목 기출 분석, 실전 모의고사, 시간 배분 훈련까지 목표 등급에 맞춘 고3 수능수학 대비와 내신을 1:1로 진행합니다.",
        "h1": "<em>{R} 고3 수학과외</em><br>수능수학 실전에 집중합니다",
        "hero": "{R} 고등학교 3학년 학생의 현재 모의고사 성적과 목표 등급을 바탕으로, 남은 기간에 맞춘 1:1 수능수학 대비 계획을 세웁니다.",
        "intro_h2": "고3 수학공부,<br>남은 시간을 설계합니다.",
        "intro": "<strong>{R} 고3 수학</strong>은 정해진 기간 안에 점수를 올려야 하는 시기입니다. 모의고사 결과로 취약 단원과 실수 유형을 분석하고, 기출 문제와 실전 모의고사, 시간 배분 훈련의 비중을 목표 등급에 맞춰 조정합니다. 수시를 준비하는 학생은 3학년 내신도 함께 챙깁니다.",
        "stages": [
            ("진단", "취약 단원 분석", "최근 모의고사와 오답을 분석해 점수를 가장 많이 잃는 단원과 실수 유형을 찾습니다."),
            ("기출", "수능 기출 유형 정리", "수학Ⅰ·수학Ⅱ와 선택과목의 기출 문제를 유형별로 정리하고 풀이 근거를 세웁니다."),
            ("실전", "모의고사·시간 배분", "실전 모의고사로 문항 배치에 따른 시간 배분과 검토 루틴을 훈련합니다."),
        ],
        "concerns": [
            "모의고사에서 시간이 부족해 끝까지 풀지 못하는 학생",
            "특정 단원에서 반복해서 점수를 잃는 학생",
            "목표 등급까지 한두 등급을 올려야 하는 학생",
            "수시 내신과 수능 최저 기준을 함께 준비하는 학생",
        ],
        "faqs": [
            ("고3인데 지금 시작해도 늦지 않을까요?",
             "남은 기간에 따라 목표와 범위를 현실적으로 정합니다. 점수를 가장 많이 잃는 단원과 실수 유형부터 줄이면 짧은 기간에도 개선할 여지가 있습니다."),
            ("수능 최저 기준만 맞추면 되는데 어떻게 공부하나요?",
             "목표 등급에 필요한 점수를 기준으로, 꼭 맞혀야 할 문항 유형을 먼저 안정시키는 방식으로 계획을 세웁니다. 고난도 문항보다 정확도를 우선합니다."),
            ("고3 내신과 수능을 함께 준비할 수 있나요?",
             "수시 지원 계획에 따라 비중을 정합니다. 내신 시험 기간에는 학교 범위에 집중하고, 그 외 기간에는 수능 기출과 실전 훈련에 집중합니다."),
        ],
        "card": "수능 기출 · 실전 모의고사",
    },
]


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
    urls += [(f"math/{y['key']}.html", "monthly", "0.8") for y in YEARS]
    urls += [(f"regions/{r['slug']}.html", "monthly", "0.8") for r in REGIONS]
    grade_urls, area_urls = [], []
    years_of = lambda key: [y for y in YEARS if y["parent"] == key]

    # 울산 전체 학년별 페이지
    for grade in GRADES:
        path = f"math/{grade['key']}.html"
        name = f"울산 {grade['label']} 수학과외"
        # 초등 페이지에는 다음 단계인 예비중1 안내를 연결합니다.
        years = years_of(grade["key"]) or [y for y in YEARS if y["key"] == "pre-middle-1"]
        write(path, grade_page(
            grade, place="울산", path=path, root="../", css="../regions/region-styles.css",
            crumbs=[("홈", "../"), ("지역별 수학과외", "../regions/"), (name, None)],
            crumb_ld=[("홈", ""), ("지역별 수학과외", "regions/"), (name, path)],
            sibling_links=[(f"울산 {g['label']} 수학과외", f"{g['key']}.html", g is grade) for g in GRADES],
            local_title=f"울산 {grade['label']} 학년별 세부 안내" if years_of(grade["key"]) else "다음 단계 안내",
            local_links=[(f"울산 {y['label']} 수학과외", f"{y['key']}.html", False) for y in years],
            cross_title=f"구·군별 {grade['label']} 수학과외",
            cross_links=[(f"{region_label(r)} {grade['label']} 수학", f"../regions/{r['slug']}/{grade['key']}-math.html", False) for r in REGIONS],
        ))

    # 울산 전체 학년(중1, 고2 등) 세부 페이지
    for year in YEARS:
        path = f"math/{year['key']}.html"
        parent = next(g for g in GRADES if g["key"] == year["parent"])
        parent_name = f"울산 {parent['label']} 수학과외"
        name = f"울산 {year['label']} 수학과외"
        write(path, grade_page(
            year, place="울산", path=path, root="../", css="../regions/region-styles.css",
            crumbs=[("홈", "../"), ("지역별 수학과외", "../regions/"), (parent_name, f"{parent['key']}.html"), (name, None)],
            crumb_ld=[("홈", ""), ("지역별 수학과외", "regions/"), (parent_name, f"math/{parent['key']}.html"), (name, path)],
            sibling_links=[(f"울산 {y['label']} 수학과외", f"{y['key']}.html", y is year) for y in years_of(year["parent"])],
            local_title="", local_links=None,
            cross_title=f"지역별 {parent['label']} 수학과외",
            cross_links=[(f"울산 전체 {parent['label']} 수학", f"{parent['key']}.html", False)]
            + [(f"{region_label(r)} {parent['label']} 수학", f"../regions/{r['slug']}/{parent['key']}-math.html", False) for r in REGIONS],
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
                + [(f"{region_label(r)} {grade['label']} 수학", f"../{r['slug']}/{grade['key']}-math.html", False) for r in REGIONS if r is not region]
                + [(f"울산 {y['label']} 수학과외", f"../../math/{y['key']}.html", False)
                   for y in (years_of(grade["key"]) or [y for y in YEARS if y["key"] == "pre-middle-1"])],
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
    print(f"Generated {len(GRADES)} Ulsan grade pages, {len(YEARS)} Ulsan year pages, {len(grade_urls)} region grade pages, {len(area_urls)} area pages, {len(urls)} sitemap URLs.")


if __name__ == "__main__":
    main()
