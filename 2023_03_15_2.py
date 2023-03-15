import requests
import pandas as pd
from tqdm import tqdm
import my_utils as mu
import time
import random
'''
    티어 + 디비전
'''
url = 'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/GOLD/IV?page=1&api_key=RGAPI-ba02ad31-18e8-4da7-9005-8d209ab0420e'

res = requests.get(url).json()
print('res : ', res)

summoner_lst = list(map(lambda x : x['summonerName'], res))

lst = []
# for s in tqdm(summoner_lst[:10]) :
#     puuid = mu.get_puuid(s)
#     print('puuid : ', puuid)
#     match_ids = mu.get_match_id(puuid, 5)
#     for match_id in match_ids :
#         match_timelines_lst = mu.get_matches_timelines(match_id)
#         lst.append(match_timelines_lst)
#     time.sleep(20)
#
# print('lst : ', lst)

'''
    matchid, matches, timeline으로 구성된 원시데이터 df 만드는 함수
    (인자값으로 티어만 넣으면 해당 티어의 디비전 1, 2, 3, 4 사람들 중 랜덤으로 가져오는 함수
'''
division_list = ['I', 'II', 'III', 'IV']

def rand() :
    page = random.randrange(1, 10)
    division = random.randrange(0, 3)
    return page, division

def get_rawdata(tier) :
    lst = []
    page, division = rand()
    riot_api_key = mu.riot_api_key
    url = f'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division_list[division]}?page=1&api_key={riot_api_key}'
    print(url)
    res = requests.get(url).json()
    lst += random.sample(res, 5)
    summoner_lst = list(map(lambda x: x['summonerName'], lst))
    print('summoner_lst : ', summoner_lst)
    lst = []
    for s in tqdm(summoner_lst) :
        puuid = mu.get_puuid(s)
        match_ids = mu.get_match_id(puuid, 5)
        for match_id in match_ids :
            matches, timelines = mu.get_matches_timelines(match_id)
            match_timelines_lst = [match_id, matches, timelines]
            lst.append(match_timelines_lst)
        time.sleep(3)
    df = pd.DataFrame(lst, columns=['match_id', 'matches', 'timelines'])
    return df
    #summoner_lst = list(map(lambda x: x['summonerName'], res))
    # division 리스트와 page를 랜덤으로 뽑아올 함수를 사용하기, lst 리스트도 만들어 두기
    # riot api를 통해서 summonerName을 가져오기
    # match_ids 가져오기
    # match, timeline rawdata - match_id, matches, timelines df 만들기

# def get_rawdata(tier) :
#
#     match_timelines = 'Bronze'
#     return match_timelines

row_data = get_rawdata('SILVER')
print(row_data)

print(row_data['matches'].keys())

# 원시 데이터인 df 넣어서 ouput, match, timeline 데이터가 있는 df를 만들기
#['gameId','gameDuration','gameVersion','summonerName','summonerLevel','participantId','championName', 'champExperience','teamPosition','teamId','win','kills','deaths','assists', 'totalDamageDealtToChampions','totalDamageTaken']
#timeline_df [,'g5','g6' ~ 'g25'] => 25분까지 안 가는 게임 0으로 넣기
# pk 값 - (match_id, participantId)
# def get_match_timeline_df(df) :
#     df_creator = []
#     print('소환사 스텟 생성 중....')
#     for i in range(len(df)) :
#         #match를 만드는
#         #timeline을 만드는
#     return df

# 함수 결과값(df)를 넣을 수 있는 테이블 생성과 insert 까지
# pk 값(match_id, participantId)
# kda = []
# # match_id, championName, kills, deaths, assists
# for i in range(len(df)) :
#     print(df.iloc[i].gameid)
#     for j in range(len(df.iloc[i].matches['info']['participants'])) :
#         kda_list = []
#         kda_list.append(df.iloc[i].gameid)
#         kda_list.append(df.iloc[i].matches['info']['participants'][j]['championName'])
#         kda_list.append(df.iloc[i].matches['info']['participants'][j]['kills'])
#         kda_list.append(df.iloc[i].matches['info']['participants'][j]['deaths'])
#         kda_list.append(df.iloc[i].matches['info']['participants'][j]['assists'])
#         kda.append(kda_list)

'''
    팀끼리 상의해서 흥미롭고 재미있을 것 같은 롤 데이터를 통해 만들 수 있는 주제 3가지를 선정해서 발표
    시각화 모듈 사용해서 최소 2가지
'''