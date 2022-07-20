# GITOMP

![기톰프뮤직](https://user-images.githubusercontent.com/70262871/103122910-9fe4b680-46c5-11eb-8319-5f09f694ea7e.jpg)

- **Team_name** : GITOMP
- **Team_member** : 김규빈(Team Leader), 김승재 , 문병곤 , 박소윤 , 최선우
- **Project_development \_period** : 2020년 12월 15일 ~ 2020년 12월 24일
- **Backend_github** : **[GITOMP-Backend](https://github.com/wecode-bootcamp-korea/15-1st-GITOMP-backend)**

## Project_info

연주음악 전문 레이블로 출발한 **[STOMPMUSIC](http://stompmusic.com/)** 사이트는 정통클래식, 재즈, 뉴에이지, 영화음악, 월드뮤직 그리고 대중음악까지 장르가 다양한 사이트를 공부의 목적으로 참조하여 구현하였습니다.

## Main_skills

- Swiper 라이브러리를 이용한 슬라이더 기능
- 동적 라우팅을 이용한 페이지 이동 기능
- 로그인/회원가입 기능
- 게시판 기능

## Tech_stack / Tool

> **Front-end**

- React
- React-router-dom
- Javascript
- HTML, SASS
- CRA, npm
- Git & Github
- ESLint , Prettier
- trello

![image](https://user-images.githubusercontent.com/70262871/103123428-ab38e180-46c7-11eb-99a9-04d136db789e.png)

---

> **Back-end**

- Python
- Django
- MySQL
- AWS
- JWT
- Bcrypt
- Faker & Google Trans
- Gunicorn
- Nginx
- Git & Github
- trello
- Aquerytool

![image](https://user-images.githubusercontent.com/70262871/103123637-5ba6e580-46c8-11eb-95d7-321c2ca66548.png)

# Video

_-_ **MainPage onClick**

[![image](https://user-images.githubusercontent.com/70262871/103147016-0932fb00-4794-11eb-9150-98523ed01591.png)](https://youtu.be/dGxxuie2M10)

## Member Info

1. 김규빈 :

- Role : Team Leader
- Position : Front-end
- Stack : React / Sass / Router
- Works : 회원가입 / 앨범 카테고리 / 커뮤니티 카테고리

[로그인 & 회원가입]

- 회원가입 / 로그인 폼 구현 및 기능구현 (Vaildation 및 로그인 인증/인가 통신)
- 로그인 성공시 TOKEN가져와 로컬스토리지에 저장
- 모달창 형식으로 팝업, 로그인 후 View 수정(로그아웃 버튼, 닉네임 출력)

[앨범 게시판]

- 앨범 카테고리(fetch를 통해 앨범 데이터 가져오기)
- 앨범 리스트 페이지 네이션(componentDidUpdate를 통해 match.params를 비교하여 업데이트 후 출력)
- 앨범리스트 필터링 기능(년도, 장르, 내용, 검색키워드를 쿼리스트링으로 요청 후 매칭되는 데이터 출력)
- 앨범 리스트 디테일 페이지(componentDidUpdate를 통해 해당되는 id 데이터를 조회 후 출력)
- 앨범 디테일 페이지 다음 글,이전 글(match.params를 통해 id+1 ,id -1 데이터를 가져오는 방식)

[커뮤니티 게시판]

- 커뮤니티 게시판 정보 통신 후 가져오기
- 커뮤니티 게시판 글쓰기 기능(TOKEN 정보를 가져와 인가를 통해 게시물 판별)
- 커뮤니티 게시판 글쓰기(제목, 내용, 닉네임, 조회수, 날짜)
- 게시물 디테일 화면 구현
- 게시물 다음글 이전글 탭 구현

---

2. 문병곤

- Role : Team Member
- Position : Front-end
- Stack : React / Sass / Router
- Works : ( 작업한 페이지 구현 )

[메인페이지]

- 메인 페이지 애니메이션 및 기능 구현
- swiper 라이브러리를 통해 슬라이드 애니메이션 구현
- 백엔드 Api를 가져와 앨범 섹션의 슬라이드에 구현

후기글
https://velog.io/@soral215/GITOMP-MUSIC-1%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9B%84%EA%B8%B0


---

3. 박소윤

- Role : Team Member
- Position : Front-end
- Stack : React / Sass / Router
- Works : Navigation

[ Navigation ]

1. 100% Nav Layout 및 scss 구현
2. component 구현
3. Navigation의 animation 구현

[ Concert ]

1. Concert 페이지 바탕으로 Component 설계 Layout 및 scss를 이용한 디자인 구현
2. Component 구현과 관련 API 연결
3. Concert_List 페이지 및 Concert-Detail 페이지 에따른 관련 API 연결

---

---

4. 김승재

- Role : Team Member
- Position : Back-end
- Stack : Django, Python
- Works : 모델링 (공통) 로그인&회원가입 (공퉁) & 자유게시판 & 앨범

[로그인 & 회원가입]

- JWT Token & bcrypt를 이용한 인증 & 인가
- 회원정보 (이메일/ 비밀번호/ 닉네임)을 정규표현식을 이용하여 데이터 유효성 검사
- 유저 회원 가입시 기타 오류 (jsondecodingerror 및 유효성 실패)에 대한 예외처리

[자유게시판]

- Http 통신시 토큰을 이용한 인가로 유저데이터 입력
- 게시물 CRUD (등록 / 조회 / 삭제 / 수정) API 구현
- 댓글 CRUD (등록 / 조회 / 삭제 / 수정) API 구현
- 페이지네이션과 검색옵션+검색어에 따른 필터링 구현

[앨범]

- 앨범 Fake Data 준비 (faker library와 google trans를 이용한 100개이상의 랜덤 앨범 데이터 생성 로직 구현)
- Main Page에 나오는 카테고리별 앨범데이터 API 구현
- 앨범 리스트의 페이지네이션과 검색옵션을 이용한 필터링 구현
- 앨범 상세 정보에 대한 데이터와 이전/이후 앨범에 대한 데이터 API 준비

---

5. 최선우

- Role : Team Member
- Position : Back-end
- Stack : Django, Python
- Works : 모델링 (공통) 로그인 & 회원가입 (공퉁) & 콘서트

[로그인 & 회원가입]

- JWT Token & bcrypt를 이용한 인증 & 인가
- 회원정보 (이메일/ 비밀번호/ 닉네임)을 정규표현식을 이용하여 데이터 유효성 검사
- 유저 회원 가입시 기타 오류 (jsondecodingerror 및 유효성 실패)에 대한 예외처리

[콘서트]

- Main Page에 나오는 콘서트 데이터 API 구현
- 콘서트 리스트의 페이지네이션과 검색 옵션을 이용한 필터링 구현
- 콘서트 상세 정보에 대한 데이터와 이전/이후 앨범에 대한 데이터 API 준비
- 콘서트 Fake Data 준비

---

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![image](https://user-images.githubusercontent.com/70262871/103124814-4af86e80-46cc-11eb-9e50-8671c6a712f4.png)

---

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;👍 GITOMP 팀 너무너무 최고였습니다 !!! 👍

---
