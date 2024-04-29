import requests
import cv2
import keyboard

ApiKey = "RGAPI-c16df5a5-7eb4-408d-9b59-bee6b1c520de"
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
    else:
        return 400

def GameMatch(DataCode, GameType, Count):
    #인게임 검색
    GameSearch = MatchSearch(DataCode, GameType, Count)
    if GameSearch.status_code == 200:
        GameData = GameSearch.json()
        return GameData
    else:
        return 400
    
while True:
    PlayerName = input("닉네임 검색\n > ")
    if '#' in PlayerName:
        Name = PlayerName.split('#')
        _Number = PlayerSearch(Name[0], Name[1])
        if _Number != 400:
            break
        else:
            ("닉네임이 잘못되었습니다.")
    else:
        print("닉네임과 태그가 잘못 입력되었습니다.")
        
while True:
    GameType = input("1. 랭크\n2. 일반\n > ")
    GameCount = input("최대 100까지\n > ")
    if GameType == '1' or GameType == '랭크':
        A = 'ranked'
    elif GameType == '2' or GameType == '일반':
        A = 'normal'
    GameData = GameMatch(_Number, 'ranked', GameCount)
    if GameData != 400:
        break
    else:
        print("다시 입력해주세요.")


#타임라인
TotalScore = []
for i in GameData:
    Total = {}
    kill = []
    death = []
    killtime = []
    deathtime = []
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
            if j == _Number:
                break
        
        _InGameData = InGameData['info']
        _InGameDataEvent = _InGameData['frames']

        for j in _InGameDataEvent:
            DataEvent = j['events']
            for k in DataEvent:
                if 'victimId' in k:
                    if k['victimId'] == location:
                        # 리스트에 넣기
                        death.append(k['position'])
                        death.append(k['timestamp'])
                        deathtime.append(list(death))
                        death.clear()
                    if k['killerId'] == location:
                        kill.append(k['position'])
                        kill.append(k['timestamp'])
                        killtime.append(list(kill))
                        kill.clear()
    Total['kill'] = killtime
    Total['death'] = deathtime
    Total['gamecode'] = i
    TotalScore.append(dict(Total))

for Data in TotalScore:
    print("kill")
    for i in Data["kill"]:
        for A in i:
            if dict == type(A):
                if "x" in A:
                    print(A["x"])
                if "y" in A:
                    print(A["y"])
            else:
                print(A)
    print()
    
    print("death")
    for i in Data["death"]:
        for A in i:
            if dict == type(A):
                if "x" in A:
                    print(A["x"])
                if "y" in A:
                    print(A["y"])
            else:
                print(A)
    print()
    if "gamecode" in Data:
        print(Data["gamecode"])

image = cv2.imread('C:/Users/home/Desktop/riotapi-main/riotapi-main/minimap.png')
while True:
    State = "change"
    KillMap = cv2.copy(image)
    DeathMap = cv2.copy(image)

    
    Map = cv2.resize(image, dsize = (15000,15000), interpolation = cv2.INTER_AREA)

    for Data in TotalScore:
        for Info in Data["kill"]:
            for i in Info:
                if dict == type(i):
                    if "x" in i:
                        x = i["x"]
                    if "y" in i:
                        y = i["y"]
                    cv2.line(KillMap, (int(x), int(y)), (int(x), int(y)), (0,255,0), 100)
        for Info in Data["kill"]:
            for i in Info:
                if dict == type(i):
                    if "x" in i:
                        x = i["x"]
                    if "y" in i:
                        y = i["y"]
                    cv2.line(DeathMap, (int(x), int(y)), (int(x), int(y)), (0,255,0), 100)
                        
    cv2.imshow("kill", Map)
'''
for i in killmap:
    x = i['x'] / 24.39 + 34
    y = i['y'] / 24.39 + 42
    cv2.line(killImage, (int(x), int(y)), (int(x), int(y)), (0,255,0), 3)

for i in deathmap:
    x = i['x'] / 24.39 + 34
    y = i['y'] / 24.39 + 42
    cv2.line(deathImage, (int(x), int(y)), (int(x), int(y)), (0,0,255), 3)
'''

    cv2.waitKey()
    while True:
        if keyboard.is_pressed("right"):
            State = "right"
        elif keyboard.is_pressed("left"):
            State = "left"
        elif keyboard.is_pressed("enter"): 
            cv2.destroyAllWindows()
            State = "close"
            break
    if State == "close":
        break
    elif State == "right":
        
    elif State == "left":
        

