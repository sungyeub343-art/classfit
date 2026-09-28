$ErrorActionPreference = "Stop"
$scriptDirectory = if ($PSScriptRoot) { $PSScriptRoot } else { Join-Path (Get-Location) "scripts" }
$root = Split-Path -Parent $scriptDirectory
$regionsRoot = Join-Path $root "regions"
$utf8 = New-Object System.Text.UTF8Encoding($false)

$regions = @(
    @{ Name = "중구"; Slug = "jung-gu"; Type = "동"; Parent = "jung-gu.html"; Areas = @(
        @("학성동", "hakseong-dong"), @("반구1동", "bangu-1-dong"), @("반구2동", "bangu-2-dong"), @("복산동", "boksan-dong"),
        @("성안동", "seongan-dong"), @("중앙동", "jungang-dong"), @("우정동", "ujeong-dong"), @("태화동", "taehwa-dong"),
        @("다운동", "daun-dong"), @("병영1동", "byeongyeong-1-dong"), @("병영2동", "byeongyeong-2-dong"), @("약사동", "yaksa-dong")
    )},
    @{ Name = "남구"; Slug = "nam-gu"; Type = "동"; Parent = "nam-gu.html"; Areas = @(
        @("신정1동", "sinjeong-1-dong"), @("신정2동", "sinjeong-2-dong"), @("신정3동", "sinjeong-3-dong"), @("신정4동", "sinjeong-4-dong"),
        @("신정5동", "sinjeong-5-dong"), @("달동", "dal-dong"), @("삼산동", "samsan-dong"), @("삼호동", "samho-dong"),
        @("무거동", "mugeo-dong"), @("옥동", "ok-dong"), @("야음장생포동", "yaeum-jangsaengpo-dong"), @("대현동", "daehyeon-dong"),
        @("수암동", "suam-dong"), @("선암동", "seonam-dong")
    )},
    @{ Name = "동구"; Slug = "dong-gu"; Type = "동"; Parent = "dong-gu.html"; Areas = @(
        @("방어동", "bangeo-dong"), @("일산동", "ilsan-dong"), @("화정동", "hwajeong-dong"), @("대송동", "daesong-dong"),
        @("전하1동", "jeonha-1-dong"), @("전하2동", "jeonha-2-dong"), @("남목1동", "nammok-1-dong"), @("남목2동", "nammok-2-dong"), @("남목3동", "nammok-3-dong")
    )},
    @{ Name = "북구"; Slug = "buk-gu"; Type = "동"; Parent = "buk-gu.html"; Areas = @(
        @("농소1동", "nongso-1-dong"), @("농소2동", "nongso-2-dong"), @("농소3동", "nongso-3-dong"), @("강동동", "gangdong-dong"),
        @("효문동", "hyomun-dong"), @("송정동", "songjeong-dong"), @("양정동", "yangjeong-dong"), @("염포동", "yeompo-dong")
    )},
    @{ Name = "울주군"; Slug = "ulju-gun"; Type = "읍·면"; Parent = "ulju-gun.html"; Areas = @(
        @("온산읍", "onsan-eup"), @("언양읍", "eonyang-eup"), @("온양읍", "onyang-eup"), @("범서읍", "beomseo-eup"),
        @("청량읍", "cheongnyang-eup"), @("삼남읍", "samnam-eup"), @("서생면", "seosaeng-myeon"), @("웅촌면", "ungchon-myeon"),
        @("두동면", "dudong-myeon"), @("두서면", "duseo-myeon"), @("상북면", "sangbuk-myeon"), @("삼동면", "samdong-myeon")
    )}
)

function New-SubareaPage($region, $areaName, $areaSlug) {
    $areaLinks = ($region.Areas | ForEach-Object {
        $current = if ($_[1] -eq $areaSlug) { ' aria-current="page"' } else { "" }
        "<a$current href=`"$($_[1]).html`">$($_[0])</a>"
    }) -join ""
    $title = "울산 $($region.Name) $areaName 수학과외 무료체험수업 안내 | 울산 수학과외"
    return @"
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="울산 $($region.Name) $areaName 초등·중등·고등 학생을 위한 맞춤 수학과외 무료체험수업 안내입니다.">
  <link rel="canonical" href="https://classfit.kr/regions/$($region.Slug)/$areaSlug.html">
  <link rel="icon" href="../../assets/logo-mark.svg" type="image/svg+xml">
  <title>$title</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../region-styles.css">
</head>
<body>
  <header class="region-header">
    <a class="brand" href="../../"><img class="brand-mark" src="../../assets/logo-mark.svg" alt=""><span>울산 수학과외<small>1:1 맞춤 수업</small></span></a>
    <nav class="region-nav" aria-label="지역 페이지 메뉴"><a href="../">지역별 안내</a><a href="../$($region.Parent)">$($region.Name) 안내</a><a class="call-link" href="tel:01029283614">☎ 010-2928-3614</a></nav>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="현재 위치"><a href="../../">홈</a><span>›</span><a href="../">지역별 수학과외</a><span>›</span><a href="../$($region.Parent)">$($region.Name)</a><span>›</span>$areaName</nav>
    <section class="area-hero">
      <p class="eyebrow">ULSAN LOCAL MATH TUTORING</p>
      <h1><em>울산 $($region.Name) $areaName</em><br>수학과외 무료체험수업 안내</h1>
      <p>$areaName 초등·중등·고등 학생의 현재 수준과 목표를 살펴보고, 학교 진도와 학습 속도에 맞는 1:1 수학 공부 방향을 설계합니다.</p>
      <div class="hero-actions"><a class="button button-primary" href="../../#consult">무료체험 상담 신청</a><a class="button button-outline" href="tel:01029283614">전화 상담하기</a></div>
    </section>
    <section class="content-section">
      <div class="section-intro"><div><p class="eyebrow">PERSONALIZED LESSON</p><h2>$areaName 학생에게 맞는<br>공부 흐름을 만듭니다.</h2></div><div><p><strong>울산 $($region.Name) $areaName 수학과외</strong>는 정답만 알려주지 않습니다. 개념의 빈틈과 풀이 습관을 진단하고, 이해·적용·복습의 과정을 학생의 속도에 맞춰 이어갑니다.</p></div></div>
      <div class="feature-grid"><article class="feature"><span>01 DIAGNOSIS</span><h3>현재 수준 진단</h3><p>개념 이해도와 문제 풀이 과정을 확인해 먼저 보완할 부분을 찾습니다.</p></article><article class="feature"><span>02 LESSON</span><h3>학년별 맞춤 수업</h3><p>초등 기초, 중등 내신, 고등 학습 목표에 맞게 수업의 순서와 속도를 정합니다.</p></article><article class="feature"><span>03 MANAGEMENT</span><h3>복습과 오답 관리</h3><p>수업 후 복습과 오답 점검으로 혼자 공부할 수 있는 학습 습관을 기릅니다.</p></article></div>
    </section>
    <section class="trial-band"><div><h2>$areaName 수학과외,<br>무료체험수업으로 시작하세요.</h2><p>상담 후 학생에게 맞는 체험수업 방향을 안내해 드립니다.</p></div><div class="trial-actions"><a class="button button-primary" href="../../#consult">무료체험 신청</a><a class="button button-outline" href="tel:01029283614">010-2928-3614</a></div></section>
    <section class="other-areas"><h2>$($region.Name) 다른 $($region.Type) 안내</h2><div class="area-links">$areaLinks</div></section>
  </main>
  <footer class="region-footer"><a class="brand" href="../../"><img class="brand-mark" src="../../assets/logo-mark.svg" alt=""><span>울산 수학과외<small>1:1 맞춤 수업</small></span></a><p>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p><p>© 2026 ULSAN MATH TUTORING.</p></footer>
</body>
</html>
"@
}

$areaUrls = @()
foreach ($region in $regions) {
    $targetDirectory = Join-Path $regionsRoot $region.Slug
    if (Test-Path $targetDirectory) { Remove-Item $targetDirectory -Recurse -Force }
    New-Item -ItemType Directory -Path $targetDirectory | Out-Null
    foreach ($area in $region.Areas) {
        $areaName, $areaSlug = $area
      [System.IO.File]::WriteAllText((Join-Path $targetDirectory "$areaSlug.html"), (New-SubareaPage $region $areaName $areaSlug), $utf8)
        $areaUrls += "regions/$($region.Slug)/$areaSlug.html"
    }
}

$baseUrls = @("", "regions/") + ($regions | ForEach-Object { "regions/$($_.Parent)" })
$allUrls = $baseUrls + $areaUrls
$sitemapEntries = for ($index = 0; $index -lt $allUrls.Count; $index++) {
    $frequency = if ($index -eq 0) { "weekly" } else { "monthly" }
    $priority = if ($index -eq 0) { "1.0" } elseif ($index -eq 1) { "0.9" } elseif ($index -lt $baseUrls.Count) { "0.8" } else { "0.7" }
    "  <url>`n    <loc>https://classfit.kr/$($allUrls[$index])</loc>`n    <changefreq>$frequency</changefreq>`n    <priority>$priority</priority>`n  </url>"
}
$sitemap = "<?xml version=`"1.0`" encoding=`"UTF-8`"?>`n<urlset xmlns=`"http://www.sitemaps.org/schemas/sitemap/0.9`">`n$($sitemapEntries -join "`n")`n</urlset>`n"
[System.IO.File]::WriteAllText((Join-Path $root "sitemap.xml"), $sitemap, $utf8)

Write-Output "Generated $($areaUrls.Count) subarea pages and $($allUrls.Count) sitemap URLs."