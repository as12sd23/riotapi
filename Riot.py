import requests
import cv2
import keyboard

ApiKey = "RGAPI-59131c3a-7bf5-48ec-a67e-cf454b4fc5dd"
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

image = cv2.imread('C:/Users/c404/Desktop/sangjin/riotapi-main/minimap.png')
ImageCount = 0
MapType = "kill"
while True:
    State = "change"
    KillMap = cv2.resize(image, dsize = (15000,15000), interpolation = cv2.INTER_AREA)
    DeathMap = cv2.resize(image, dsize = (15000,15000), interpolation = cv2.INTER_AREA)
    
    (h,w) = KillMap.shape[:2]
    (cX, cY) = (w/2, h/2)
    
    (h,w) = DeathMap.shape[:2]
    (cX, cY) = (w/2, h/2)
    
    M = cv2.getRotationMatrix2D((cX, cY),180,1.0)
    KillMap = cv2.warpAffine(KillMap,M,(h,w))
    DeathMap = cv2.warpAffine(DeathMap,M,(h,w))
    
    i = 0
    for Data in TotalScore:
        if ImageCount == i:
            for Info in Data["kill"]:
                for i in Info:
                    if dict == type(i):
                        if "x" in i:
                            x = i["x"]
                        if "y" in i:
                            y = i["y"]
                        cv2.line(KillMap, (int(x), int(y)), (int(x), int(y)), (0,255,0), 100)
            for Info in Data["death"]:
                for i in Info:
                    if dict == type(i):
                        if "x" in i:
                            x = i["x"]
                        if "y" in i:
                            y = i["y"]
                        cv2.line(DeathMap, (int(x), int(y)), (int(x), int(y)), (255,0,0), 100)
            break
        i += 1
    
    M = cv2.getRotationMatrix2D((cX, cY),-180,1.0)
    KillMap = cv2.warpAffine(KillMap,M,(h,w))
    DeathMap = cv2.warpAffine(DeathMap,M,(h,w))
    KillMap = cv2.resize(KillMap, dsize = (500,500), interpolation = cv2.INTER_AREA)
    DeathMap = cv2.resize(DeathMap, dsize = (500,500), interpolation = cv2.INTER_AREA)
    cv2.imshow(MapType, KillMap)

    cv2.waitKey()
    while True:
        if State == "change":
            if keyboard.is_pressed("right"):
                if ImageCount >= int(GameCount):
                    ImageCount = 0
                else:
                    ImageCount += 1
                break
            elif keyboard.is_pressed("left"):
                if ImageCount <= 0:
                    ImageCount = int(GameCount)
                else:
                    ImageCount -= 1
                break
            elif keyboard.is_pressed("up"):
                if (MapType == "kill"):
                    MapType = "death"
                else:
                    MapType = "kill"
                break
            elif keyboard.is_pressed("down"):
                if (MapType == "kill"):
                    MapType = "death"
                else:
                    MapType = "kill"
                break
            elif keyboard.is_pressed("enter"): 
                State = "close"
                cv2.destroyAllWindows()
                break
    
    
    if State == "close":
        break

