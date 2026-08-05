# 슬라이드 디자인 시스템 — Slide Design.md (초안)

> 이 문서는 [kms_uxui_portfolio_draft.html](kms_uxui_portfolio_draft.html) 아티팩트에서 실제 쓰인 스타일을 일반화한 문서.
> **컬러·폰트만 이 프로젝트(페이퍼토리) 값**이고, 나머지 레이아웃·컴포넌트·모션 규칙은 다른 프로젝트에도 그대로 재사용 가능하도록 구조화함.
> 상태: 초안 — "슬라이드 끝!" 신호 받으면 최종 HTML 기준으로 전체 재동기화 예정.

## 0. 컨셉

세로로 쭉 이어지는 **한 장짜리 스크롤형 슬라이드 덱**. 각 섹션(`section.slide`)이 뷰포트 하나를 채우는 "슬라이드"처럼 동작하되, 브라우저 스크롤로 자연스럽게 넘어감(`scroll-snap-type: y proximity` — 강제 아님, 부드럽게 걸리는 정도).

## 1. 컬러 시스템 (이 프로젝트 값 — 다른 프로젝트는 여기만 교체)

Primitive를 따로 두지 않고 바로 Semantic 토큰(CSS 커스텀 프로퍼티)으로 선언. **컴포넌트는 항상 var(--토큰)만 참조**, hex 직접 사용 금지.

| 토큰 | 역할 | 라이트 | 다크 |
|---|---|---|---|
| `--bg` | 페이지 배경 | `#F7F8FC` | `#12141B` |
| `--surface` | 카드·패널 배경 | `#FFFFFF` | `#1A1D26` |
| `--card` | 보조 배경(코드블록 라벨, 매트릭스 중립 등) | `#EFF1F5` | `#20232E` |
| `--text` | 본문 기본 | `#1C222A` | `#EEF1FC` |
| `--text-secondary` | 리드 문단·설명 | `#5F656E` | `#A6ACC2` |
| `--text-tertiary` | 캡션·각주 | `#7A8089` | `#7E86A0` |
| `--border` | 구분선·아웃라인 | `#E3E6EC` | `#2B2F3C` |
| `--brand` | 주 강조색(링크, 아이콘, 통계 숫자) | `#6083F5` | `#8FA8FF` |
| `--brand-strong` | 브랜드 강조 텍스트 | `#4664CB` | `#B8C8FF` |
| `--brand-tint` | 브랜드 옅은 배경(뱃지 등) | `#EDF0FD` | `#1D2440` |
| `--lime` | 보조 강조색 — **하이라이트/형광펜 모티프 전용** | `#E6F997` | `#D8EE7A` |
| `--lime-ink` | 라임 배경 위 텍스트 | `#545E1C` | `#20240A` |
| `--negative` | 부정/거부 시맨틱 컬러 | `#BF5055` | `#E08387` |
| `--negative-tint` | 부정 배경 | `#F6E8EA` | `#3A2226` |

**컬러 사용 원칙**
- `--brand`는 "신뢰·정보" 톤(링크, 통계, 데이터 시각화 기본색)
- `--lime`은 "기록·강조" 톤 — 본문 중 핵심 문구를 `<mark>`로 감쌀 때, 반응 매트릭스의 "승인" 배지, 장식용 그라디언트 블롭에만 사용. 일반 UI 색으로 남용하지 않음(제품 자체의 "형광펜" 컨셉과 일치시키기 위함)
- `--negative`는 게이지/매트릭스 등 데이터 시각화에서만 사용, UI 크롬에는 쓰지 않음
- **다크모드는 `@media (prefers-color-scheme: dark)` + `:root[data-theme="dark/light"]` 이중 정의** — 뷰어 시스템 설정과 수동 토글 둘 다 대응

## 2. 타이포그래피

| 역할 | 클래스 | 크기 | 굵기 |
|---|---|---|---|
| 슬라이드 제목 | `h2` | `clamp(1.6rem, 3.4vw, 2.35rem)` | 800 |
| 커버 타이틀 | `.cover h1` | `clamp(2.8rem, 8vw, 4.6rem)` | 800 |
| 섹션 라벨(eyebrow) | `.eyebrow` | `0.78rem` | 700, uppercase, letter-spacing 0.08em |
| 리드 문단 | `.lede` | `1.08rem` | 400, `--text-secondary`, `max-width: 56ch` |
| 본문 리스트 | `.points li` | 기본 | 400, `max-width: 68ch` |
| 통계 숫자 | `.stat .num` | `clamp(2.6rem, 7vw, 4rem)` | 800, `font-variant-numeric: tabular-nums` |
| 캡션/각주 | `.note` | `0.78rem` | `--text-tertiary` |

**폰트 패밀리**: 이 프로젝트는 Paperlogy(제목·UI, 400/500/600/700/800 5웨이트) 단일 패밀리 + 웨이트로 위계 구분. 다른 프로젝트로 옮길 때는 이 자리에 해당 프로젝트의 제목용/본문용 웹폰트를 `@font-face` + base64 data URI로 통째로 교체 (외부 CDN 링크 금지 — 퍼블리시 환경 CSP 때문에 반드시 인라인).

## 3. 레이아웃 / 스페이싱

- **슬라이드 컨테이너**: `section.slide { min-height: 100svh; padding: 5rem 1.5rem; }`, 콘텐츠는 `.wrap { max-width: 860px; margin: 0 auto; }`로 중앙 정렬
- **섹션 간 리듬**: 슬라이드 내부 블록 간 간격은 `margin-top: 1.5~2rem` 통일
- **2단 레이아웃**: `.split2`(1fr 1fr, gap 2.5rem, 모바일에서 1열), `.grid2`(카드 2x2), `.split`(비교 카드 2개) — 용도별로 분리하되 전부 `@media (max-width:760px)`에서 1열로 붕괴
- **여백 원칙**: 카드 내부 패딩 `1.4rem 1.5rem`, 카드 라운드 `16px`(코드블록은 `14px`, 칩·뱃지는 `999px`)

## 4. 장식 모티프 — 앰비언트 그라디언트 블롭

**핵심 규칙: 블롭은 섹션이 아니라 `body`에 고정(`position: fixed`)** — 섹션마다 새로 그리면 스크롤할 때 슬라이드 경계에서 끊겨 보임. `body::before`(라임, 우상단) / `body::after`(브랜드 블루, 좌하단) 두 개의 큰 radial-gradient 원을 뷰포트에 고정해, 스크롤해도 하나로 이어지는 배경처럼 보이게 함.

```css
body::before, body::after{ content:""; position:fixed; border-radius:50%; pointer-events:none; z-index:0; }
body::before{ width:50rem; height:50rem; top:-16rem; right:-14rem;
  background:radial-gradient(circle at 32% 32%, var(--lime) 0%, transparent 68%);
  opacity:0.30; filter:blur(30px); }
body::after{ width:42rem; height:42rem; bottom:-16rem; left:-14rem;
  background:radial-gradient(circle at 68% 68%, var(--brand) 0%, transparent 70%);
  opacity:0.20; filter:blur(35px); }
```

커버·클로징처럼 자체 배경(그라디언트/틴트)이 있는 섹션은 이 블롭 위에 불투명하게 덮이므로 자동으로 자연스럽게 처리됨. 콘텐츠(`.wrap`)는 `position:relative; z-index:1`로 블롭 위에 뜸.

## 5. 컴포넌트 목록

| 컴포넌트 | 클래스 | 용도 |
|---|---|---|
| 상단 배너 | `.draft-banner` | 초안임을 알리는 고정 상단 바 |
| 진행률 바 | `.progress` | 스크롤 위치에 따라 채워지는 최상단 얇은 바 |
| 닷 내비게이션 | `.dotnav` | 우측 고정, 섹션별 점 + hover 툴팁, `IntersectionObserver`로 활성 표시. 900px 이하에서 숨김 |
| 카드 | `.card` | 일반 정보 카드 |
| 인용구 | `.quote` + `<cite>` | 큰 pull-quote, 핵심 어구는 `<mark>`로 라임 하이라이트 |
| 통계 콜아웃 | `.stat` | 큰 숫자 + 짧은 설명 |
| 퍼널 차트 | `.funnel` | 막대형 퍼널(TAM→SAM→SOM류 단계 축소 시각화) |
| 포지셔닝 차트 | `.quadrant` | **실제 자료(스크린샷)를 그대로 넣는 자리** — 좌표를 직접 손으로 재현하지 않고 원본 슬라이드 이미지를 크롭해 사용 (아래 §7 참고) |
| 반응 매트릭스 | `.rmatrix` | 항목×참여자 반응을 점 색상(brand/neutral/negative)으로, 우측에 판정 뱃지(`go`=라임, `no`=negative) |
| 좌우 비교 | `.split` + `.tag` | 두 가지 접근을 나란히 대비 |
| 실제 자료 이미지 | `.realshot` | 발표 슬라이드·현장 사진 등 원본을 그대로 삽입할 때 |
| 코드블록 | `.codeblock` | 다크 패널 + monospace, 쿼리·커밋 메시지 등 인용 |
| 기기 프레임 라이브 임베드 | `.pocbox` / `.pocframe` | 실제 동작하는 프로토타입을 iframe으로 축소 삽입 (아래 §7) |
| 스크린샷 자리 | `.shot` | 아직 없는 이미지의 점선 플레이스홀더 |

## 6. 반응형

- 브레이크포인트 하나만 사용: `max-width: 760px` (2단→1단), `max-width: 900px`(닷 내비 숨김)
- 이미지·프레임은 항상 `max-width` + `width:100%` 조합으로 축소, 고정 px 금비

## 7. 실제 자산을 그대로 쓰는 두 가지 기법

1. **정적 이미지**: 실제 발표 슬라이드나 사진을 스크린샷/크롭해서 `<img src="data:image/jpeg;base64,...">`로 통째로 인라인. 차트나 복잡한 시각 자료는 직접 CSS로 재현하지 말고 원본을 그대로 잘라 쓰는 쪽이 항상 더 정확함.
2. **라이브 프로토타입 임베드**: 독립 실행형 HTML(POC 등)을 base64로 인코딩해 페이지 하단 `<script>`에 심어두고, `iframe.srcdoc`에 디코드해 주입. 기기 프레임(`.pocframe`, `aspect-ratio: 393/852`)에 실제 사이즈(393×852)로 iframe을 그리고 `transform: scale(컨테이너너비/393)`으로 축소 — 리사이즈 시 재계산.
   - 주의: 원본 HTML이 외부 CDN(웹폰트 등)을 참조하면 퍼블리시 환경 CSP에 막혀 폰트만 시스템 폰트로 대체됨(기능은 정상 동작).

## 8. 다른 프로젝트에 적용할 때 체크리스트

- [ ] §1 컬러 토큰 값을 새 프로젝트 브랜드 컬러로 교체 (라이트/다크 둘 다)
- [ ] §2 폰트를 새 프로젝트 웹폰트로 교체 (base64 `@font-face`)
- [ ] §4 블롭 컬러가 새 브랜드 컬러를 참조하는지 확인 (토큰만 쓰면 자동 반영됨)
- [ ] 나머지(레이아웃/컴포넌트/모션/반응형)는 그대로 재사용
