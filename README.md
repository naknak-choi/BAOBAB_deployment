# BAOBAB_deployment

## 멋쟁이 사자차럼 11기 중앙 해커톤 전북대 BAOBAB팀 배포 레포지터리 입니다

프론트엔드 레포 : https://github.com/asIwishAsIdream/LikeLion_BAOBOB
프론트 레포에서 다음 명령어 실행

```bash
$npm run build
```

후 생성된 build 폴더를 복사, 이 레포에 frontend_build 라는 이름으로 붙여넣기

python 3.8 add Path 체크 해 설치 후 다음 명령어 실행해 필요한 파일 설치
```bash
$pip install virtualenv
$virtualenv -p python3.8 myenv
$.\myenv\Scripts\activate
$pip install -r requirements.txt
$pip install whitenoise
pip install django-cors-headers
```
BAOBAB 폴더 하단에 secrets.json 파일 생성
파일 내부에
```{
  "SECRET_KEY": "여기에 장고 시크릿 키 입력",
  "EMAIL_HOST_USER": "xxx@gmail.com",
  "EMAIL_HOST_PASSWORD": "xxx"
}
```
설정 후 저장하고 다음 명령어로 서버 실행
```bash
$python manage.py runserver
```
