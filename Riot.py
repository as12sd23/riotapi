import requests

ApiKey = "RGAPI-6bb0eed6-7bae-48c2-8d80-c8eefe7d8bfb"
header = {"X-Riot-Token": ApiKey}
DeathPosition = {}
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

#플레이어 검색
Account = SummonerSearch("KR1", "마루하늘")

#puuid 추출
if Account.status_code == 200:
    data = Account.json()

    DataCode = data['puuid']
    DataName = data['gameName']

#인게임 검색
GameSearch = MatchSearch(DataCode, 'normal', 20)

if GameSearch.status_code == 200:
    GameData = GameSearch.json()

#인게임 데이터 분류
for i in GameData:
    print('-----------------------------------')
    print(i)
    InGame = MatchData(i)

    if InGame.status_code == 200:
        InGameData = InGame.json()

        InData = InGameData['info']
        InData = InData['participants']
        
        for i in InData:
            if i['teamId'] == 100:
                TeamColor = 'Blue'
            elif i['teamId'] == 200:
                TeamColor = 'Red'
            TeamPosition = i['teamPosition']
            print(TeamColor + "팀")
            print("라인 :", TeamPosition)
            print("이름 :", i['summonerName'])

'''
killerId가 킬 딴 사람 ID
victimId가 죽은 사람 ID

matadata에서 participants 안에 순서로 번호가 결정됨
내가 0번째면 1번 아이디를 가져감

레드팀일 경우 6 ~ 10 숫자를 가져감
블루팀일 경우 1 ~ 5 숫자를 가져감

victimId칸 안에어 position에 x, y 좌표있음
'''

        
        


    

