import requests
import cv2
import numpy as np

ApiKey = "RGAPI-75946a3e-2f2b-42aa-bc8f-4772ab2dda7d"
header = {"X-Riot-Token": ApiKey}
DeathPosition = []
GameColor = []
Game = []


#플레이어 검색
def SummonerSearch(Tag, Name):
    url = f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{Name}/{Tag}?api_key={ApiKey}'

    return requests.get(url, headers = header)
#인게임 찾기
def MatchSearch(puuid, GameType, GameCount):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={GameType}&start=0&count={GameCount}&api_key={ApiKey}'

    return requests.get(url, headers = header)
#인게임 데이터
def MatchData(matchId):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={ApiKey}'

    return requests.get(url, headers = header)
#인게임 타임라인
def MatchTimeLineData(matchId):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline?api_key={ApiKey}'

    return requests.get(url, headers = header)

def PlayerSearch(name, tag):
    
    #플레이어 검색
    Account = SummonerSearch(tag, name)

    #puuid 추출
    if Account.status_code == 200:
        data = Account.json()

        DataCode = data['puuid']

        return DataCode
    else
        return 400

def GameMatch(GameType,Count)
    #인게임 검색
    GameSearch = MatchSearch(DataCode, GameType, Count)
    if GameSearch.status_code == 200:
        GameData = GameSearch.json()
        return GameData
    else:
        return 400
    
while True:
    PlayerName = input("닉네임 검색")
    if '#' in PlayerName:
        Name = PlayerName.split('#')
        _Number = PlayerSearch(Name[0], Name[1])
        if _Number != 400:
            GameType = input("1. 랭크\n2. 일반\n3. 자유랭\n > ")
            GameCount = input("최대 100까지\n > ")
            
        else:
            ("닉네임이 잘못되었습니다.")
    else:
        print("닉네임과 태그가 잘못 입력되었습니다.")
    
#타임라인
deathmap = []
killmap = []
for i in GameData:
    location = 0
    print('-----------------------------------')
    print(i)
    InGame = MatchTimeLineData(i)
    if InGame.status_code == 200:
        InGameData = InGame.json()
        _InGameMetadata = InGameData['metadata']
        _InGameParti = _InGameMetadata['participants']
        for j in _InGameParti:
            location += 1
            if j == DataCode:
                break
        
        _InGameData = InGameData['info']
        _InGameDataEvent = _InGameData['frames']

        for j in _InGameDataEvent:
            DataEvent = j['events']
            for k in DataEvent:
                if 'victimId' in k:
                    if k['victimId'] == location:
                        deathmap.append(k['position'])
                    if k['killerId'] == location:
                        killmap.append(k['position'])

                        

image = cv2.imread('C:/Users/c404/Desktop/sangjin/python/minimap.png')
killImage = image.copy()
deathImage = image.copy()
#670 669 3
#나누기 22 하면 될듯
for i in killmap:
    x = i['x'] / 24.39 + 34
    y = i['y'] / 24.39 + 42
    cv2.line(killImage, (int(x), int(y)), (int(x), int(y)), (0,255,0), 3)

for i in deathmap:
    x = i['x'] / 24.39 + 34
    y = i['y'] / 24.39 + 42
    cv2.line(deathImage, (int(x), int(y)), (int(x), int(y)), (0,0,255), 3)

cv2.imshow("kill", killImage)
cv2.imshow("death", deathImage)
cv2.waitKey()
cv2.destroyAllWindows()
                        

