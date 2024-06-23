## Overview
### 쿠폰이미지로 부터 상품명, 브랜드명, 유효기간, 시리얼 넘버를 추출.

1. images 폴더내 쿠폰이미지들을 15개의 "Thread" 프로세스에 분배를한다. 이 때 서버에 전송된 쿠폰이미지들은
   최소한 15개 이상 이어야하며 images 폴더내에 저장이된다.

2. 프로세스 하나에 3개의 이미지가 있다고 가정을 하면 각 이미지로부터 글자를
   ""['신세계백화점', '0000원권', 2024.04.29 까지', '900759761791']"" 리스트 형태로 3개 추출한다.

3. API로 작동하는 GPT-3.5 Turbo 모델이 3개의 리스트를 ""product_name : 카페 아메리카노 T,
   brand_name : 스타박스, serial_number : 900556865990, expires_at : 20230305"" 형태로
   3개의 문장을 추출한다.

4. 위 추출된문장들을 records/record.txt 에 기록을 한다. records 폴더는 코드에서 자동으로 만들어진다.
 
## 실행

1. images 폴더내에 png 형태의 쿠폰이미지를 15개 이상 저장을한다.
   
2. python easyocr_gpt3.py 를 바로 실행한다.
   
3. (Option) 49번째줄에 records/record.txt 부분이 있는데 txt 파일 (정형 데이터) 이름을 변경 할수 있다.
   record2.txt 로 변경하고 싶으면 records/record2.txt 로 변경 하면 된다.

## Appendix

1. 11-15번 째 줄 : GPT-3.5 Turbo 와 EasyOCR 모델을 Load 한다.
 
2. 18-24번 째 줄 : GPT-3.5 Turbo 가 content 와 prompt를 받고 output 을 내는 함수, contents는 조건사항
   prompt 는 ocr 로 추출된 문자열들 즉 input 이다.
   
3. 30-34 : GPT-3.5 Turbo 에 전달할 쿠폰 이미지들내 문자들이 추출된다.
 
4. 37-41 : GPT-3.5 Turbo 에 대한 Prompt Engineering 부분이며 조건 사항들을 지시한다.
