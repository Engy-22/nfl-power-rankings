from __future__ import division
import nfldb
import team_data

def init():
    'Initialize nfldb connection'

    global db

    db = nfldb.connect()

def generate_query(team):
    'Generate a base query to the NFLDB'

    team_query = nfldb.Query(db)
    team_query.game(season_year=2015, season_type='Regular', team=team['id'], week=[1, 2, 3, 4])

    for game in team_query.as_games():
        team['games'] += 1

        if game.winner == team['id']:
            team['wins'] += 1

        if game.home_team == team['id']:
            team['points_scored'] += game.home_score
            team['points_against'] += game.away_score
            team['point_differential'] += (game.home_score - game.away_score)
            team['turnover_differential'] += (game.home_turnovers - game.away_turnovers)
            team['opponents'].append(game.away_team)
        else:
            team['points_scored'] += game.away_score
            team['points_against'] += game.home_score
            team['point_differential'] += (game.away_score - game.home_score)
            team['turnover_differential'] += (game.away_turnovers - game.home_turnovers)
            team['opponents'].append(game.home_team)

def calc_team_record_ranking(team):
    for opp in team['opponents']:
        team['opponent_games'] += teams[opp]['games']
        team['opponent_wins'] += teams[opp]['wins']

    team['points_scored_avg'] = team['points_scored'] / team['games']
    team['points_against_avg'] = team['points_against'] / team['games']
    team['point_differential_avg'] = team['point_differential'] / team['games']
    team['sos'] = team['opponent_wins'] / team['opponent_games']
    team['win_percentage'] = team['wins'] / team['games']

def calc_points_ranking(teams, pointsKey, rankingKey):
    prevAvg = None
    index = 32
    indexSeries = 0

    for id, team in sorted(teams.iteritems(), key=lambda (x, y): y[pointsKey], reverse=True):
        if prevAvg == team[pointsKey]:
            indexSeries += 1
        elif indexSeries > 0:
            indexSeries = 0

        prevAvg = team[pointsKey]
        team[rankingKey] = index + indexSeries
        index -= 1

def calc_power_ranking(team):
    team['win_value'] = ((team['wins'] * 2.5) * team['sos']) * 0.50
    team['point_differential_value'] = (team['point_differential_avg'] * team['sos']) * 0.25
    team['points_scored_value'] = ((team['points_scored_ranking'] * 0.3125) * team['sos']) * 0.10
    team['points_against_value'] = ((team['points_against_ranking'] * 0.3125) * team['sos']) * 0.10
    team['turnover_differential_value'] = team['turnover_differential'] * 0.05

    team['power_ranking'] = team['win_value'] + team['point_differential_value'] + team['points_scored_value'] + team['points_against_value'] + team['turnover_differential_value']

def print_power_rankings(teams):
    index = 1

    for id, team in sorted(teams.iteritems(), key=lambda (x, y): y['power_ranking'], reverse=True):
        # print '%d. %s, %.1f' % (index, team['id'], team['power_ranking'])
        print '%d. %s, %.1f, wv: %.1f, pdv: %.1f, psv: %.1f, pav: %.1f, tdv: %.1f' % (index, team['id'], team['power_ranking'], team['win_value'], team['point_differential_value'], team['points_scored_value'], team['points_against_value'],  team['turnover_differential_value'])
        index += 1

init()

global teams

teams = team_data.get_data()

for id, team in teams.iteritems():
    team['games'] = 0
    team['wins'] = 0
    team['points_scored'] = 0
    team['points_against'] = 0
    team['point_differential'] = 0
    team['turnover_differential'] = 0
    team['opponents'] = []
    team['opponent_games'] = 0
    team['opponent_wins'] = 0
    generate_query(team)

for id, team in teams.iteritems():
    calc_team_record_ranking(team)

calc_points_ranking(teams, 'points_scored_avg', 'points_scored_ranking')
calc_points_ranking(teams, 'points_against_avg', 'points_against_ranking')

for id, team in teams.iteritems():
    calc_power_ranking(team)

print_power_rankings(teams)