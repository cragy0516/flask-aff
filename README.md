# ARGOS Freshman Festival Grade Server

## 소개

ARGOS Freshman Festival (AFF)란 ARGOS에서 주최하는, 신입생들을 위한 내부 C언어 대회입니다. C언어에 한정한 코딩 문제들을 소수의 인원들이 해결하면서 점수를 획득하고, 이를 이용해서 경쟁하며 순위를 평가하는 방식입니다.

본 `repository`는 해당 대회를 위한 채점 서버에 필요한 기술적인 사항을 정리한 것 입니다. 기본적으로 안전한 컴파일 환경을 보장하기 위해 가상화 도구인 `Docker`를 사용하고, 사용자와 상호작용 하는 부분은 `flask`를 사용하였습니다. 자세한 내용은 [블로그 문서](https://cragy0516.github.io/Development-Grade-Server-with-Docker-and-Flask/)를 참조하시기 바랍니다.

## 주의 사항

해당 `repository`는 자동화된 설치 도구를 제공하지 않습니다. 모든 환경이 세팅된 상황에서는 완벽하게 동작하지만, 그렇지 않은 환경이라면 `Docker`와 `image file`등 동작 전에 필요한 사항을 세팅해 줄 필요가 있을것입니다. 또한 Linux Ubuntu 16.04.1 운영체제에서 테스트 해 보았으며, 아직 최소/권장사양을 점검하지 않은 상태입니다.