<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg"/>
  <img src="assets/banner-light.svg" alt="Kyubum Jang - QA Engineer" width="100%%"/>
</picture>

<br/>

<a href="https://www.notion.so/lawrencejang/KYUBUM-JANG-681280b273b04d4ca9f6bcd6d81e335d"><img src="https://img.shields.io/badge/Resume-10B981?style=for-the-badge" alt="Resume"/></a>&nbsp;<a href="https://www.linkedin.com/in/kyubumjang"><img src="https://img.shields.io/badge/LinkedIn-0F172A?style=for-the-badge" alt="LinkedIn"/></a>&nbsp;<a href="https://kyubumjang.github.io/"><img src="https://img.shields.io/badge/Blog-0F172A?style=for-the-badge" alt="Blog"/></a>&nbsp;<a href="https://www.notion.so/lawrencejang/2bc378e1e50f43349f0c968e9ba65768"><img src="https://img.shields.io/badge/About-0F172A?style=for-the-badge" alt="About"/></a>

<sub>장규범 · Seoul, Korea</sub>

</div>

---

품질은 배포 직전에 검사해서 만들어지지 않는다고 생각합니다. 기획서를 읽는 순간부터 무엇이 위험한지를 정하고, 그 기준을 팀이 함께 쓰게 만드는 일까지가 QC의 몫이라고 봅니다.

커머스·B2B 서비스 네 곳의 정기 배포를 맡고 있습니다. 릴리스마다 위험도 순으로 검수 범위를 정하고, 결과를 리포트로 남겨 다음 릴리스의 기준으로 씁니다. 같은 결함이 두 번 나오면 테스트 케이스가 아니라 프로세스를 고칩니다. 어느 단계에서 걸러졌어야 했는지 되짚어 체크리스트와 가이드에 반영합니다.

프론트엔드 개발 경험이 있어 컴포넌트 상태와 API 응답을 직접 확인합니다. 덕분에 결함 리포트를 "버튼이 안 눌려요"가 아니라 "이 조건에서 이 요청이 이 응답을 받고 이 상태로 남습니다"로 적을 수 있고, 고치는 쪽과 확인하는 쪽이 한 번에 끝납니다.

반복되는 확인은 사람이 하지 않아야 한다고 보고, 자동점검과 AI로 옮기는 작업을 계속하고 있습니다. 사람은 판단이 필요한 자리에 남겨두는 것이 좋은 QC라고 생각합니다.

> 나무처럼 꾸준히 가지를 뻗어, 결국 열매를 맺는 사람이 되고 싶습니다.

<details>
<summary><b>English</b></summary>

<br/>

Quality isn't created by inspecting a build the day before release. From the moment the spec is written, someone has to decide what is risky and get the whole team using that same standard. That is what I think QC is for.

I own the release cycle for four commerce and B2B services. Each release, I scope verification by risk, then publish a report that becomes the baseline for the next one. When the same defect shows up twice, I fix the process rather than the test case, and trace back which stage should have caught it.

Having written production frontend code, I read component state and API responses myself. So a defect report says "under this condition this request returns this response and leaves this state," not "the button doesn't work" - which means the person fixing it and the person verifying it are both done in one pass.

Repetitive checks shouldn't be done by people, so I keep moving them into automated checks and AI. People stay where judgment is actually needed.

</details>

## What I Test

| 영역 | 대상 | 범위 |
| :-- | :-- | :-- |
| **Release&nbsp;QC** | 애드콘 · 애드콘비즈 · 비즈애드콘 · 애드웰 | 정기 배포 검수, 운영 환경 핵심 시나리오 점검, HTML QC 리포트 발행 |
| **External&nbsp;QA** | 외부 고객사 WEB / MOBILE | 테스트 계획서, 결함 관리, 품질 통계 대시보드 |
| **Automation** | 서비스 자동점검 · 회귀 스위트 | Playwright · Python 검증 스크립트 |
| **AI&nbsp;×&nbsp;QC** | AI TC 생성기 | 품질 분석, 중복 제거, 커버리지 갭 분석 |

## How I Work

**위험한 것부터 봅니다.**
기능 목록 순서로 테스트하면 시간이 모자랄 때 하필 마지막 항목이 잘립니다. RBT(Risk-Based Testing) 분류 체계를 만들어, 틀리면 되돌리기 어려운 구간을 먼저 확인하고 그 다음을 잘라냅니다.

**반복되는 확인은 자동으로 넘깁니다.**
회귀 검증 사이클을 `16시간 → 6시간` 으로 줄였습니다. 스위트를 병렬로 쪼개고, 매번 같은 순서로 클릭하던 구간을 Playwright 자동점검으로 옮긴 결과입니다.

**판단 기준을 문서로 남깁니다.**
7단계 QC 프로세스 가이드와 온보딩 문서를 써서, 신규 입사자가 첫 배포 검수에 바로 들어갈 수 있게 했습니다. 혼자 잘하는 것보다 팀이 같은 기준으로 판단하는 편이 오래 갑니다.

## Experience

| 기간 | 소속 | 역할 |
| :-- | :-- | :-- |
| 2025.04 ~ | **다우기술** 품질관리팀 | QC - 커머스·B2B 서비스 배포 검수, 자동점검, AI TC |
| 2022.12 ~ 2023.06 | **aaant** 개발팀 | Frontend - React · TypeScript |
| 2021.06 ~ 2021.08 | **시너지** 개발팀 | Frontend |

## Toolbox

| 분류 | 스택과 쓰임 |
| :-- | :-- |
| **테스트 자동화** | Playwright, Python - 회귀 스위트와 서비스 자동점검 스크립트 |
| **AI** | Claude - TC 생성·정제, 중복/커버리지 갭 분석, 품질 게이트 설계 |
| **협업 · 관리** | Redmine, Notion, Slack, Excel |
| **프론트엔드** | TypeScript, React, Next.js, React Query, Recoil, Emotion, vanilla-extract |

## Work with me

이력서는 [Notion](https://www.notion.so/lawrencejang/KYUBUM-JANG-681280b273b04d4ca9f6bcd6d81e335d)에 정리해두었고, 커피챗과 문의는 [LinkedIn](https://www.linkedin.com/in/kyubumjang)으로 받습니다. 공부한 것은 [트리규의 개발 블로그](https://kyubumjang.github.io/)에 쓰고 있습니다.
