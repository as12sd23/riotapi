import requests
import cv2
import keyboard

ApiKey = "RGAPI-401401b1-d294-404c-9f83-d57f7e82aa3b"
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
image = cv2.imread('C:/Users/c404/Desktop/sangjin/riotapi-main/minimap.png')
index = 0
TotalScore = []
for i in GameData:
    
    KillMap = cv2.resize(image, dsize = (17000,17000), interpolation = cv2.INTER_AREA)
    (h,w) = KillMap.shape[:2]
    (cX, cY) = (w/2, h/2)
    M = cv2.getRotationMatrix2D((cX, cY),180,1.0)
    KillMap = cv2.warpAffine(KillMap,M,(h,w))
    
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
                        if dict == type(i):
                            if "x" in i:
                                x = i["x"]
                            if "y" in i:
                                y = i["y"]
                            cv2.line(KillMap, (int(x), int(y)), (int(x), int(y)), (0,0,255), 300)
                            

                    if k['killerId'] == location:
                        if dict == type(i):
                            if "x" in i:
                                x = i["x"]
                            if "y" in i:
                                y = i["y"]
                            cv2.line(KillMap, (int(x), int(y)), (int(x), int(y)), (255,255,255), 300)
                            
     M = cv2.getRotationMatrix2D((cX, cY),-180,1.0)
     KillMap = cv2.warpAffine(KillMap,M,(h,w))                   
     cv2.imwrite("C:/Users/c404/Desktop/sangjin/riotapi-main/Minimap/minimap{}.jpg".format(index), KillMap)
     index = index + 1

idx = 0
cnt = int(GameCount) * 2
print(cnt)
while True:
    img = cv2.imread("C:/Users/c404/Desktop/sangjin/riotapi-main/Minimap/minimap{}.jpg".format(idx))
    if img is None:
        print("load failed!")
        break
    img = cv2.resize(img, dsize = (500,500), interpolation = cv2.INTER_AREA)
    cv2.imshow('{}번째게임'.format(idx + 1), img)
    cv2.waitKey()
    if keyboard.is_pressed("Right"):
        idx += 1
        if idx >= cnt:
            idx = 0
    elif keyboard.is_pressed("Left"):
        idx -= 1
        if idx < 0:
            idx = cnt - 1
    else:
        break        
cv2.destroyAllWindows()

    
