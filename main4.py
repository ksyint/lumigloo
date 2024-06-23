
import glob 
import os
import openai
import time 
from threading import Thread
import easyocr
import random
import csv
import re
openai.api_key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI
from datetime import datetime
import pytz

korea_tz = pytz.timezone('Asia/Seoul')
korea_time = datetime.now(korea_tz)

client = OpenAI()

reader = easyocr.Reader(['ko','en'],gpu = True) 

def chat_gpt(prompt,contents):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        
        messages=[{"role": "system", "content": f"{contents}"},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def main(index,paths):

    prompts=" "

    for path in paths:
        
        ocr_result=reader.readtext(path,detail=0)
        prompts+=str(ocr_result)
        prompts+="  "
#https://github.com/favorcat/GPT-RAG/blob/master/cli_gpt.py
    contents=f""" product_name, brand_name, expires_at, serial_number로 분류하세요,product_name과 brand_name은 같아선 안됩니다. 
                expires_at, product_name은 숫자 0 으로 시작하지 않습니다. 이때  ['신세계백화점', '0000원권 2024.04.29 까지', '900759761791'] 
                와 같은 형태의 리스트가 {len(paths)}개가 들어올것이고 총 {len(paths)}개 줄의 product_name,brand_name,serial_number,expires_at을  
                추출하세요, 한줄 예시 -> product_name : 아메리카노 hot, brand_name : 메가커피, expires_at : 20240604, serial_number : 608997198786 
                & product_name : 카페 아메리카노 T, brand_name : 스타박스, serial_number : 900556865990, expires_at : 20230305 
                그리고 마지막으로 ['신세계백화점', '0000원권 2024.04.29 까지', '900759761791']  는 ocr 의 결과이고 부정확한 텍스트가 있을수 있다. 
                해당 데이터베이스 내용을 참고하여서 리스트안의 내용이 잘못되었다고 판단이 들면 텍스트를 고쳐서 출력을 하십시오, 데이터 베이스 내용은 다음과
                같습니다-> [brand_name 종류 : 스타벅스, 투썸플레이스] [product_name 종류 : 스타벅스 카페라떼] -> 
                데이터베이스 활용예시: ['스타넉스'] 즉 스타벅스 와 유사한 단어가 리스트안에 있을때 스타벅스 로 고친다. 
                이때 스타벅스와 유사한 단어는 스타넉스 에만 국한하지 않는다. 고치는 예시는 스타넉스-> 스타벅스, 스타박스 -> 스타벅스
                product_name의 경우 브랜드명이 있어선 안된다. 이와관련해서 맞는 예시하나는 떠먹는 베리 쿠키 아이스박스 이고 잘못된 예시하나는 
                투썸플레이스 떠먹는 베리 쿠키 아이스박스 이다 """

    A=chat_gpt(prompts,contents)
    print("Recording")
    os.makedirs(f"records",exist_ok=True)

    with open(f"records/record_{korea_time}.txt","a") as record:
        record.writelines(f"Start {len(paths)} 개 문장 나와야한다")
        record.writelines("\n")
        record.writelines(str(A))
        record.writelines("\n")
        record.writelines("\n")
        record.writelines("출처")
        record.writelines("\n")
        record.writelines(str(paths))
        record.writelines("\n")
        record.writelines("End")
        record.writelines("\n")
        record.writelines("\n")
        record.close()
    
    
if __name__ == "__main__":
    
    print("Start")
    #rag 로 성능 개선 필요 label csv 를 db로 활용
    start=time.time()
    inputs=glob.glob(f"colorful/*.png")
    random.shuffle(inputs)
    inputs=inputs[0:200] 

    number_per_folder=len(inputs)//14 
    number_per_folder_last=len(inputs)%14 

    

    th1 = Thread(target=main,args=(1,inputs[0:number_per_folder]))
    th2 = Thread(target=main,args=(2,inputs[number_per_folder:number_per_folder*2]))
    th3 = Thread(target=main,args=(3,inputs[number_per_folder*2:number_per_folder*3]))
    th4 = Thread(target=main,args=(4,inputs[number_per_folder*3:number_per_folder*4]))
    th5 = Thread(target=main,args=(5,inputs[number_per_folder*4:number_per_folder*5]))
    th6 = Thread(target=main,args=(6,inputs[number_per_folder*5:number_per_folder*6]))
    th7 = Thread(target=main,args=(7,inputs[number_per_folder*6:number_per_folder*7]))
    th8 = Thread(target=main,args=(8,inputs[number_per_folder*7:number_per_folder*8]))
    th9 = Thread(target=main,args=(9,inputs[number_per_folder*8:number_per_folder*9]))
    th10 = Thread(target=main,args=(10,inputs[number_per_folder*9:number_per_folder*10]))
    th11 = Thread(target=main,args=(11,inputs[number_per_folder*10:number_per_folder*11]))
    th12 = Thread(target=main,args=(12,inputs[number_per_folder*11:number_per_folder*12]))
    th13 = Thread(target=main,args=(13,inputs[number_per_folder*12:number_per_folder*13]))
    th14 = Thread(target=main,args=(14,inputs[number_per_folder*13:number_per_folder*14]))
    th15 = Thread(target=main,args=(15,inputs[number_per_folder*14:number_per_folder*14+number_per_folder_last]))
    
    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th6.start()
    th7.start()
    th8.start()
    th9.start()
    th10.start()
    th11.start()
    th12.start()
    th13.start()
    th14.start()
    th15.start()
    
    th1.join()
    th2.join()
    th3.join()
    th4.join()
    th5.join()
    th6.join()
    th7.join()
    th8.join()
    th9.join()
    th10.join()
    th11.join()
    th12.join()
    th13.join()
    th14.join()
    th15.join()

    end=time.time()
    print(f"{len(inputs)} 개의 쿠폰")
    print("Wasted Time")
    print(end-start)
    print("End")

    # 1장당 0.24초 
    # 16초 50장 
    # 25초 100장




