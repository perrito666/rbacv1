#!/usr/bin/env python3
import csv
import requests
from config import SHIFTLEFT_ORG_ID, SHIFTLEFT_ACCESS_TOKEN

def main():
    with requests.Session() as s:
        url = 'https://www.shiftleft.io/api/v4/orgs/{}/rbac/teams'.format(SHIFTLEFT_ORG_ID)
        headers = {'Authorization':'Bearer {}'.format(SHIFTLEFT_ACCESS_TOKEN)}
        r = requests.get(url, headers=headers)
        teams = r.json()['response']
        #print(teams)
        url = 'https://www.shiftleft.io/api/v4/orgs/{}/rbac/users'.format(SHIFTLEFT_ORG_ID)
        r = requests.get(url, headers=headers)
        users = r.json()['response']
        #print(users)
        url = 'https://www.shiftleft.io/api/v4/orgs/{}/rbac/roles'.format(SHIFTLEFT_ORG_ID)
        r = requests.get(url, headers=headers)
        roles = r.json()['response']
        #print(roles)
        #for role in roles:
        #    if 'TEAM_DEFINED' in role.values():
        #        user_team_role = role.get('id')
        #        print(user_team_role)
        with open("rbac.csv", "r") as csv_file:
            csvreader = csv.DictReader(csv_file)
            #for row in csvreader:
            #    print(row["email"], row["team"])
            csvlist = []
            for x in csvreader:
                csvlist.append(x)
            for row in csvlist:
                user_email = row.get('email')
                #print(user_email)
                user_team = row.get('team')
                #print(user_team)
                user_role = row.get('role')
                #print(user_role)
                for team in teams:
                    #print(team)
                    if user_team in team.values():
                        user_team_id = team.get('team_id')
                        version = team.get('team_version')
                        print(user_team_id)
                        for user in users:
                            if user_email in user.values():
                                user_id = user.get('id_v2')
                                print(user_id)
                                payload = {
                                            "version": int(version),
                                                "add_team_membership": [
                                                    {
                                                        "user_id_v2": str(user_id),
                                                        "team_role": "6d5fbe08-0512-46e0-b5d2-45902ee6c0ba"
                                                    }
                                                ]
                                            }
                                url = 'https://www.shiftleft.io/api/v4/orgs/{orgid}/rbac/teams/{userteam}'.format (orgid=SHIFTLEFT_ORG_ID, userteam=user_team_id)
                                r = requests.put(url, headers=headers, json=payload)
                                print(r.status_code)
                                #print(roles)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()