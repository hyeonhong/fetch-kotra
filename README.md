# fetch_kotra

## 구동 환경 설치

[Brew](https://brew.sh/index_ko.html) 또는 [Linuxbrew](http://linuxbrew.sh/) 이용

```sh
brew install python3
pip3 install pipenv
pipenv install
```

- python 2 는 지원하지 않음


## 실행

관련 티켓: [KOTRA 스크래핑](http://git.kross.works/Kross/biz/issues/4)

브라질 진출국가 정보를 CSV 형식으로 저장 (파일은 `{진출국가}.csv` 로 생성됨)
```sh
cd bin
./fetch_kotra --region brazil --output csv
```

확인
```sh
cat brazil.csv
```
