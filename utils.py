from peewee import Model, CharField, IntegerField, SqliteDatabase

db = SqliteDatabase('score.db')


class HighScore(Model):
    player_name = CharField(max_length=64)
    score = IntegerField()

    class Meta:
        database = db


def save_to_db(player_name, score):
    HighScore.create(player_name=player_name, score=score)


def get_top_players(count=3):
    return HighScore.select().order_by(HighScore.score.desc())[:count]


def get_top_player():
    try:
        return get_top_players()[0]
    except IndexError:
        return 0


def get_high_score(count=3):
    scores = [player.score for player in get_top_players(count)]
    scores.extend([0]*(count-len(scores)))
    return scores
