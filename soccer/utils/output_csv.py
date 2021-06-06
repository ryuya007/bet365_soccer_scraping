import csv

import settings


def output_game_info(data):
    """
    parameter:
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
    with open(settings.csv_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([
            data['play_time'],
            str(data['attacks'][0]) + '-' + str(data['attacks'][1]),
        ])
