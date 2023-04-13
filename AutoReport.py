from lcu_driver import Connector
from time import sleep
import os

connector = Connector()
@connector.ready

async def connect(connection):
    print("waiting for the end of the game\n")
    gameIDs = []

    while True:
        users = {}
        friends = []
        tmp = await connection.request('get', '/lol-chat/v1/friends')
        tmp = await tmp.json()
        for friend in tmp:
            friends.append(friend['summonerId'])
            users[friend['summonerId']] = friend['name']
        me = await connection.request('get', '/lol-chat/v1/me')
        me = await me.json()
        friends.append(me['summonerId'])
        try:
            got = await connection.request('get', "/lol-end-of-game/v1/eog-stats-block")
            got = await got.json()

            try:
                gameID = got['gameId']
                if gameID in gameIDs:
                    continue
                gameIDs.append(gameID)
                os.system('cls' if os.name == 'nt' else 'clear') # clear console

                teams = got['teams']

                to_report = []
                for team in teams:
                    is_ally_team = False
                    
                    for player in team['players']:
                        if player['summonerId'] in friends:
                            is_ally_team = True
                            print(player['summonerName'], ": keep it L9 😎")
                        else:
                            print(player['summonerName'], ": reported.")
                            to_report.append(player['summonerId'])
                            
                            
                    if is_ally_team:
                        print("----- Ally team -----\n")
                    else:
                        print("----- Enemy team -----\n")

                print("my done here is job 🫡\n")
                    

                while len(to_report) > 0:
                    _report = {
                        "comment": "trash talk, toxic, racist, inting, trolling, feeding, afk, etc.",
                        "gameId": gameID,
                        "offenses": "Negative Attitude, Verbal Abuse, Intentional Feeding",
                        "reportedSummonerId": to_report.pop()
                    }
                    response = await connection.request('post', "/lol-end-of-game/v2/player-complaints", data=_report)
                    response = await response.json()

                    # print(response)
                    
                
                pass
            except KeyError:
                pass
        except KeyError:
            print("error in get conversation")
        sleep(3)

connector.start()