import numpy as np
import pandas as pd
import my_utils as mu
import requests
import matplotlib.pyplot as plt

'''
    데이터 시각화
'''

# 서울시 시간 평균 대기오염도 정보
url = 'http://openAPI.seoul.go.kr:8088/(인증키)/xml/TimeAverageAirQuality/1/5/20130615/종로구'
df = mu.df_creater(url) # DataFrame 만들기
df.drop(columns='MSRSTE_NM', inplace=True)



print(df)
