# liveqr

## About
liveqr은 구매자 중심의 UX를 갖춘 Payment 서비스 프로토 타입입니다.

판매점에서 직접 가격을 입력하면, 사용자는 생성된 QR코드를 이용하여, 결제할 수 있습니다.

해당 Repository에서는 가격 입력 / QR 코드 생성 / 디스플레이 표출 부분을 다룹니다.

## Important about Modified Script
- PLL Control Set `0x19` == `143Hz`
- VCM_DC_SETTING `0x28`
- getbuffer method Changed `(Change Algorithm)`
- display method Changed `(Change Algorithm)`
- clear method Changed `(Short Loop)`

## System_Info
### Dev_System
- OS : `Raspbian strech lite`
- Python Version : `3.5.3`
- Python Package : `requirements.txt 참조`

### Run_System
- OS : `Raspbian strech lite`
- Python Version : `3.5.3`
- Python Package : `requirements.txt 참조`

## Source_Tree
 - main.py
    - 전반적인 Flow에 따라서 Method 호출
- epd5in83.py
    - E-Paper Control 위한 Command 및 Data T/R
- epdconfig.py
    - E-paper Control 위한 초기 세팅 설정
- keypad.py
    - 시리얼 통신을 통해서 4x4 keypad Data Read 및 맵핑하여 키 return
- web.py
    - KaKaoPay API를 이용하여 결제 링크 return

## Dev-Log
- 2019-02-06 카카오페이 API 연결 및 V0.1 배포
- 2019-02-05 Keypad 입력 솔루션 완성 및 기존 E-Paper 디스플레이 부분과 연결
- 2019-02-04 E-Paper 초기 Loading시에 걸리는 시간 단축 `60초 -> 35초`
- 2019-02-03 E-Paper Demo Script와 qrcode Script Combine
- 2019-02-02 개발 시작

## Refer
- [qrcode Library](https://pypi.org/project/qrcode/)
- [5.83inch e-Paper HAT](https://www.waveshare.com/wiki/5.83inch_e-Paper_HAT)
- [AD Keypad](https://www.waveshare.com/wiki/AD_Keypad)
- [Pillow Library](https://pillow.readthedocs.io/en/3.0.x/index.html)
- [KakaoPay API](https://developers.kakao.com/docs/restapi/kakaopay-api)