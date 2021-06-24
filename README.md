# MuYaHome
본 문서는 무야홈(얼굴 인식 출입 스마트홈)을 위한 시스템 구현을 위하여 시스템 및 상세 설계서를 기술하고자 한다.
## 프로젝트 소개
* 프로젝트명 : 얼굴 인식으로 출입하고 앱으로 모든 기능을 제어함으로써 삶을 편리하게 만들어주는 스마트홈 시스템이다.
* 개발기간 : 2021-02-13 ~ 2021-06-24
* 개발인원 : 박희웅, 권택근, 윤원준, 강태훈
### 작품기능
1. 인체 감지 : 카메라 활성화
2. 눈 깜빡임 인식 : 사진으로 출입하는 것을 방지
3. 얼굴 인식 : 거주자 얼굴 인식을 하여 출입
4. 녹화 : 얼굴 인식 안될 시 저장
5. 현관문 실시간 확인 : 현관 앞 신원 미상자 감지 및 알림
6. 엘리베이터 : 출입 시 호출/해당 층 자동 선택 및 외출 시 호출/1층 자동 선택
7. 아두이노 : 엘리베이터 층수 제어 및 인체 감지
### 적용기술
1. PYTHON – dlib, face recognition, OPENCV 라이브러리를 이용해서 눈깜빡임, 얼굴인식, 녹화저장 기능 제어
2. 안드로이드 APP – 엘리베이터 호출, 현관문 실시간 확인
3. Node.js – 서버를 구축하여 프로젝트의 전반적인 데이터들을 공유
4. MySQL – 공유한 데이터들을 저장
5. 아두이노 – 엘리베이터 층수 제어
6. 라즈베리 파이 – PIR 센서를 이용한 인체 감지
### 시스템 구조도 및 순서도
![noname01](https://user-images.githubusercontent.com/86356725/123232506-2f9fdc00-d514-11eb-9dff-3387925dd68a.png)

![noname02](https://user-images.githubusercontent.com/86356725/123232527-33cbf980-d514-11eb-9219-262bb5b66c0b.png)
### 하드웨어
1. Arduino
	- Arduino Uno
  2. Arduino Ethernet Shield
	- 아두이노를 웹서버와 연동하기 위한 모듈
	- 5V I/O 신호 허용 오차로 3.3V 작동
	- 크기 : 71.0mm x 53.0mm x 23.0mm / 2.8" x 2.1" x 0.9"
	- 무게 : 25.0g/0.9oz
3. Raspberry Pi
4. 카메라 모듈
	- 얼굴인식을 하기 위한 카메라 모듈
	- 3280 x 2464 정적 이미지 지원
	- 1/4"의 광학 크기
	- 크기 : 25mm x 23mm x 9mm / 0.98" x 0.90" x 0.35“
	- 무게 : (카메라 보드 + 부착된 케이블) : 3.4g
5 PIR 센서
	- 인체 감지를 위한 PIR 센서
	- 작동 전압 범위 : DC 4.5 ~ 20V
	- 대기 전류 : 50uA
	- 감지 각도 : 트리거(트리거 L 트리거를 반복할 수 없음
	- 감지거리 : 최대 110
6. Android Smartphone
	- SAMSUNG Galaxy Note 20
###  소프트웨어
1. Arduino IDE
2. Android OS
3. Node.js 서버
4. MySQL 데이터베이스
5. PYTHON 모듈을 이용한 얼굴 인식


### 개발환경
1. Arduino IDE
2. Android Studio
3. Visual Studio Code
4. Naver Cloud Platform
### 개발언어
1. PYTHON
2. XML
3. JAVA
4. JAVA Script

### APP UI 모듈 및 시나리오
![4](https://user-images.githubusercontent.com/86356725/123236207-91157a00-d517-11eb-94bb-e9b7fb62e9a3.png)
![noname03](https://user-images.githubusercontent.com/86356725/123236126-7ba05000-d517-11eb-9fef-403ca265d122.png)
![1](https://user-images.githubusercontent.com/86356725/123236284-a38fb380-d517-11eb-8f5c-b1dafa8bb90d.png)
![2](https://user-images.githubusercontent.com/86356725/123236302-a68aa400-d517-11eb-8a3b-9d617be385b4.png)

### 출입 시나리오
![1](https://user-images.githubusercontent.com/86356725/123236400-ba360a80-d517-11eb-8e21-23b3c8487bf0.png)
![2](https://user-images.githubusercontent.com/86356725/123236413-bbffce00-d517-11eb-9133-3ec876158616.png)
![3](https://user-images.githubusercontent.com/86356725/123236447-c4580900-d517-11eb-8201-c8c044162345.png)

### API
![1](https://user-images.githubusercontent.com/86356725/123236601-e6518b80-d517-11eb-8e33-52e1665f4bfb.PNG)

### DB 모듈
![2](https://user-images.githubusercontent.com/86356725/123236651-f2d5e400-d517-11eb-880d-502a05e3778e.png)

### Arduino 회로도
◎ 7-Segment(엘리베이터 층수) 회로도
![1](https://user-images.githubusercontent.com/86356725/123236831-1731c080-d518-11eb-8beb-350f946e9a8d.png)

◎ PIR 센서 회로도
![2](https://user-images.githubusercontent.com/86356725/123236865-1f89fb80-d518-11eb-967f-296b2412bae9.png)
