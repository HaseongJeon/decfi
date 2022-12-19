import math

def raw_to_json(text):
  split_text = text.split(',')
  if len(split_text) == 13:
    split_text.remove(split_text[1]) #1998~2018년 월드컵의 split_text에 있는 빈 문자열 제거

  #승부차기까지 간 경우
  if len(split_text[5]) != 3: 
    home_away_score = int(split_text[5][4])
    json_text = {"home": split_text[4][:-3], "away": split_text[6][3:], "home_point": home_away_score, "away_point": home_away_score, "dif": 0, "home_rank": 0, "away_rank": 0, "round": 16}
  #승부차기까지 가지 않은 경우
  else:
    home_point = int(split_text[5].split('–')[0])
    away_point = int(split_text[5].split('–')[1])
    json_text = {"home": split_text[4][:-3], "away": split_text[6][3:], "home_point": home_point, "away_point": away_point, "dif": home_point - away_point, "home_rank": 0, "away_rank": 0, "round": 16}

  #몇 강까지 갔는지 기록
  if split_text[0] == 'Round of 16':
    json_text['round'] = 16
  elif split_text[0] == 'Quarter-finals':
    json_text['round'] = 8
  elif split_text[0] == 'Semi-finals':
    json_text['round'] = 4
  elif split_text[0] == 'Final':
    json_text['round'] = 2
  
  return json_text


#월드컵 연도 나누는 함수
def worldcup_year(string):
  split_string = string.split('!/n')
  return split_string

worldcup_year(game_string)


def get_teams_of_league(worldcup):
  #쪼개기
  worldcup_str = worldcup.split('\n')
  split_list = [] 
  country_list = []
  dictionary_list = []
  return_dict = [{16: []}, {8:[]}, {4:[]}, {2:[]}, {1:[]}]
  
  #쓸모없는 문자열 없애기
  wc_str = [p for p in worldcup_str if p != '' and p != '!' and p != '! ' and p != '\n']
      

#엔터(\n)를 기준으로 쪼개진 값을 딕셔너리 형태로 변환 - split_list로 들어감
  split_list = [raw_to_json(i) for i in wc_str]

#참가한 나라들 모두 나열(중복 X) - country_list로 들어감
  country_list = set([j['home'] for j in split_list] + [j['away'] for j in split_list])
      
      
  for k in country_list:
    #한 나라가 참가한 모든 경기를 team_gamecollection에 넣음
    #우승팀인 경우 team_gamecollection에 1을 넣음
    team_gamecollection = []
    for l in split_list:
      if k == l['home'] or k == l['away']:
        if l['round'] == 2:
          if k == l['home']:
            if l['home_point'] > l['away_point']:
              team_gamecollection.append(1)
            else:
              team_gamecollection.append(l)
          elif k == l['away']:
            if l['away_point'] > l['home_point']:
              team_gamecollection.append(1)
            else:
              team_gamecollection.append(l)
        else:
          team_gamecollection.append(l)

    #team_gamecollection에 1이 들어간 경우를 확인함
    if 1 in team_gamecollection:
      #max_level: 몇 강까지 올라갔는지 (우승팀은 1)
      max_level = 1
    else:
      max_level = min([m['round'] for m in team_gamecollection])
    dictionary_list.append({max_level: k}) #{최고 강 수: 나라} 형태로 dictionary_list에 들어감

  #딕셔너리 형태로 들어있는 자료를 return_dict(반환값)에다 집어넣음
  for n in dictionary_list:
    key = list(n.keys())[0]
    value = n[key]
    return_dict[4 - int(math.log2(key))][key].append(value)

  return return_dict

#tracking_team에서 대상 팀이 어느 경기에서 away 팀으로 배정되는 경우 home과 away의 위치를 바꾸는 프로그램
def changehomeaway(for_variable):
  cng_home = for_variable['away']
  cng_away = for_variable['home']
  cng_home_p = for_variable['away_point']
  cng_away_p = for_variable['home_point']
  cng_dif = cng_home_p - cng_away_p

  for_variable['home'] = cng_home
  for_variable['away'] = cng_away
  for_variable['home_point'] = cng_home_p
  for_variable['away_point'] = cng_home_p
  for_variable['dif'] = cng_dif
  
  return for_variable

def tracking_team(match1, team):
  worldcup_str = match1.split('\n')
  split_list = [] 

#엔터(\n)를 기준으로 쪼개진 값을 딕셔너리 형태로 변환 - split_list로 들어감
  for i in worldcup_str:
    split_list.append(raw_to_json(i))

#참가한 게임임 모두 team_gamecollection에 넣음
  team_gamecollection = []
  for j in split_list:
    if j['home'] == team:
      team_gamecollection.append(j)
    elif j['away'] == team:
      team_gamecollection.append(changehomeaway(j))
  
  return {team: team_gamecollection}

def analysis_to_train(match):
    train_set=[[match["home_point"], match["away_point"], match["dif"], match["home_rank"], match["away_rank"], match["home_rank"]-match["away_rank"]]]
    round_cnt=[0,0,0,0,0]
    if match["round"]==16: round_cnt[0]+=1
    elif match["round"]==8: round_cnt[1]+=1
    elif match["round"]==4: round_cnt[2]+=1
    elif match["round"]==2: round_cnt[3]+=1
    else: round_cnt[4] +=1
    train_set.append(round_cnt)
    return train_set
  
  
