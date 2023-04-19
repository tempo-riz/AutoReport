from lcu_driver import Connector
from time import sleep
import os

connector = Connector()
@connector.ready


async def connect(connection):
    VERSION="1.0.1"
    print(f"[VERSION {VERSION}] waiting for endgame ...\n")

    print("not working as expected ? want to propose a new feature ?")
    print("-> https://github.com/tempo-riz/AutoReport/issues")

    sleep(3)
    gameIDs = []

    while True:
        users = {}
        friends = []
        try:
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

                    print(len(to_report),"nerds reported 🫡\n")

                    print("not working as expected ? want to propose a new feature ?")
                    print("-> https://github.com/tempo-riz/AutoReport/issues")

                    while len(to_report) > 0:
                        _report = {
                            "comment": "trash talk, toxic, racist, inting, trolling, feeding, afk, etc.",
                            "gameId": gameID,
                            "offenses": "Negative Attitude, Verbal Abuse, Intentional Feeding",
                            # "reportedSummonerId": to_report.pop(),
                            "offenderSummonerId":to_report.pop()
                        }
                        response = await connection.request('post', "/lol-end-of-game/v2/player-reports", data=_report)
                        response = await response.json()
                        # print(response)

                    pass
                except KeyError:
                    pass
            except KeyError:
                print("error in get conversation")
        except Exception as e:
            print(e)
            sleep(20)

        sleep(3)

        

connector.start()