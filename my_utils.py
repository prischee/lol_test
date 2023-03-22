import requests
import pandas as pd
from tqdm import tqdm
import time
import random
import cx_Oracle as co
import pymysql.cursors

dsn = co.makedsn('localhost', 1521, 'xe')
riot_api_key = 'RGAPI-be1ffcef-3c5c-41a3-93ad-ab6339fcd048'
# api_key=RGAPI-6d6d0479-e484-4970-aacc-2e0f9a628fbd
seoul_api_key = '5478465a5763686a313037546a74786f'
division_list = ['I', 'II', 'III', 'IV']

def db_open() :
    global db
    global cursor
    db = co.connect(user = 'icia', password = '1111', dsn = dsn)
    cursor = db.cursor()
    print('Oracle Open!')

def oracle_execute(q):
    global db
    global cursor
    try:
        if 'select' in q or 'SELECT' in q:
            df = pd.read_sql(sql=q, con=db)
            return df
        cursor.execute(q)
        return 'oracle 쿼리 성공!'
    except Exception as e:
        print(e)

def oracle_close() :
    global db
    global cursor
    try :
        db.commit()
        cursor.close()
        db.close()
        return 'Oracle Close...'
    except Exception as e :
        print(e)

'''
mysql
'''

def connect_mysql(db) :
    conn = pymysql.connect(host='localhost', user = 'root', password = '1111', db = 'icia', charset='utf8')
    return conn

def mysql_execute(query, conn) :
    cursor_mysql = conn.cursor()
    cursor_mysql.execute(query)
    result = cursor_mysql.fetchall()
    print(result)
    return result

def mysql_execute_dict(query, conn) :
    cursor_mysql = conn.cursor(cursor = pymysql.cursors.DictCursor)
    cursor_mysql.execute(query)
    result = cursor_mysql.fetchall()
    return result

def df_creater(url) :
    global seoul_api_key
    url = url.replace('(인증키)', seoul_api_key).replace('xml', 'json').replace('/5/', '/1000/')
    res = requests.get(url).json()
    key = list(res.keys())[0]
    data = res[key]['row']
    df = pd.DataFrame(data)
    return df

def get_puuid(user_name):
    url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user_name}?api_key={riot_api_key}'
    res = requests.get(url).json()
    puuid = res['puuid']
    return puuid

def get_match_id(puuid, num):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={num}&api_key={riot_api_key}'
    res = requests.get(url).json()
    return res

def get_matches_timelines(match_id):
    url1 = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={riot_api_key}'
    res1 = requests.get(url1).json()
    url2 = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={riot_api_key}'
    res2 = requests.get(url2).json()
    return res1,res2

def get_master_puuid(user_name) :
    url = f'https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key={riot_api_key}'
    res = requests.get(url).json()
    master_list = []

def rand() :
    page = random.randrange(1, 10)
    return page

def get_rawdata(tier) :
    lst = []
    page = rand()
    for i in range(len(division_list)) :
        url = f'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division_list[i]}?page=1&api_key={riot_api_key}'
        res = requests.get(url).json()
        lst += random.sample(res, 3)
    summoner_lst = list(map(lambda x : x['summonerName'], lst))
    df_lst = []
    for s in tqdm(summoner_lst) :
        puuid = get_puuid(s)
        match_ids = get_match_id(puuid, 3)
        for match_id in match_ids :
            matches, timelines = get_matches_timelines(match_id)
            match_timelines_lst = [match_id, matches, timelines]
            df_lst.append(match_timelines_lst)
        time.sleep(3)
    df = pd.DataFrame(df_lst, columns=['match_id', 'matches', 'timelines'])
    return df

def get_match_timeline_df(df) :
    df_creator = []
    print('소환사 스텟 생성 중...')
    for i in range(len(df)) :
        if 'status' in df.iloc[i]['matches'].keys() or 'status' in  df.iloc[i]['timelines'].keys():
            print('status : 426')
        else :
            for j in range(len(df.iloc[i]['matches']['info']['participants'])) :
                lst_match = []
                participantId = df.iloc[i]['matches']['info']['participants'][j]['participantId']
                lst_match.append(df.iloc[i]['matches']['info']['gameId'])
                lst_match.append(df.iloc[i]['matches']['info']['gameDuration'])
                lst_match.append(df.iloc[i]['matches']['info']['gameVersion'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['summonerName'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['summonerLevel'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['participantId'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['championName'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['champExperience'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['teamPosition'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['teamId'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['win'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['kills'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['deaths'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['assists'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['totalDamageDealtToChampions'])
                lst_match.append(df.iloc[i]['matches']['info']['participants'][j]['totalDamageTaken'])
                if len(df.iloc[i]['timelines']['info']['frames']) < 25 :
                    for k in range(4, 25) :
                        if k < len(df.iloc[i]['timelines']['info']['frames']) :
                            lst_match.append(df.iloc[i]['timelines']['info']['frames'][k]['participantFrames'][str(participantId)]['totalGold'])
                        else :
                            lst_match.append(0)
                else :
                    for k in range(4, 25) :
                        lst_match.append(df.iloc[i]['timelines']['info']['frames'][k]['participantFrames'][str(participantId)]['totalGold'])
                df_creator.append(lst_match)
    my_df = pd.DataFrame(df_creator, columns=['gameId', 'gameDuration', 'gameVersion', 'summonerName', 'summonerLevel', 'participantId', 'championName', 'champExperience', 'teamPosition', 'teamId', 'win', 'kills', 'deaths', 'assists', 'totalDamageDealtToChampions', 'totalDamageTaken', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15', 'g16', 'g17', 'g18', 'g19', 'g20', 'g21', 'g22', 'g23', 'g24', 'g25'])
    return my_df

def insert(df) :
    query = (
        f'MERGE INTO lol_proj USING DUAL ON(gameId=\'{df.gameId}\' and participantId={df.participantId}) '
        f'WHEN NOT MATCHED THEN '
        f'insert (gameId, gameDuration, gameVersion, summonerName, summonerLevel, participantId, championName, champExperience, teamPosition, teamId, win, kills, deaths, assists, totalDamageDealtToChampions, totalDamageTaken, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17, g18, g19, g20, g21, g22, g23, g24, g25)'
        f' values ({repr(df.gameId)}, {repr(df.gameDuration)}, {repr(df.gameVersion)}, {repr(df.summonerName)}, {df.summonerLevel}, {df.participantId}, {repr(df.championName)}, {df.champExperience}, {repr(df.teamPosition)}, {df.teamId}, {repr(str(df.win))}, {df.kills}, {df.deaths}, {df.assists}, {df.totalDamageDealtToChampions}, {df.totalDamageTaken}, {df.g5}, {df.g6}, {df.g7}, {df.g8}, {df.g9}, {df.g10}, {df.g11}, {df.g12}, {df.g13}, {df.g14}, {df.g15}, {df.g16}, {df.g17}, {df.g18}, {df.g19}, {df.g20}, {df.g21}, {df.g22}, {df.g23}, {df.g24}, {df.g25})'
    )
    oracle_execute(query)
    return