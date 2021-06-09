import csv

import settings


def preprocessing(data):
    for k in data:
        if not data[k]:
            data[k] = 'None'
    return data


def output_game_info(data):
    """
    parameter:
        league_name: 'Asia - World Cup Qualifying'
        home_team: 'South Korea'
        away_team: 'Sri Lanka'
        how_to_bet: 'Under 9.5'
        odds: 1.04
        stake: '15573.35'
        to_return: '16195.28'
        cash_out: '16035.93'
        play_time: 63
        attacks: [78, 69]
        d_attacks: [44, 38]
        possession: [48, 52]
        yellow_card: [2, 5]
        red_card: [0, 0]
        corner_kick: [5, 3]
        on_target: [2, 4]
        off_target: [8, 6]
        shifts: [4, 1]
        pk: [1, 0]
        goal: [2, 1]
        goal_time: [[23, 44], [69]]
    csv header:
        play time,attacks,dangerous attacks,possession,yellow card,red card,
        corner kick,on target,off target,shifts,pk,goal,goal time
    """
    if not data:
        return False
    data = preprocessing(data)
    with open(settings.csv_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([
            data['league_name'],
            data['home_team'],
            data['away_team'],
            data['how_to_bet'],
            data['odds'],
            data['stake'],
            data['to_return'],
            data['cash_out'],
            data['play_time'],
            str(data['attacks'][0]) + '-' + str(data['attacks'][1]),
            str(data['d_attacks'][0]) + '-' + str(data['d_attacks'][1]),
            str(data['possession'][0]) + '-' + str(data['possession'][1]),
            str(data['yellow_card'][0]) + '-' + str(data['yellow_card'][1]),
            str(data['red_card'][0]) + '-' + str(data['red_card'][1]),
            str(data['corner_kick'][0]) + '-' + str(data['corner_kick'][1]),
            str(data['on_target'][0]) + '-' + str(data['on_target'][1]),
            str(data['off_target'][0]) + '-' + str(data['off_target'][1]),
            str(data['shifts'][0]) + '-' + str(data['shifts'][1]),
            str(data['pk'][0]) + '-' + str(data['pk'][1]),
            str(data['goal'][0]) + '-' + str(data['goal'][1]),
            str(data['off_target'][0]) + '-' + str(data['off_target'][1]),
            str(data['goal_time'][0]) + '-' + str(data['goal_time'][1])
        ])
