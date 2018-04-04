from datetime import timedelta, date

from marshmallow import fields

from app.database import get_db
from data_models.game import Game
from .season import SeasonSchema
from .standings import Standings
from . import ModelSchema

ROUNDS_TOTAL = 4


class _TeamPair:
    SERIES_MAX_WINS = 4

    def __init__(self, num, tid1, tid2):
        self.num = num
        self.tid1 = tid1
        self.tid2 = tid2
        self.wins1 = 0
        self.wins2 = 0

    def get_key(self):
        # less tid should be first to have the same ids order as in scores map key
        return min(self.tid1, self.tid2), max(self.tid1, self.tid2)

    def set_score(self, score):
        self.wins1 = score[self.tid1]
        self.wins2 = score[self.tid2]

    def is_finished(self):
        return self.wins1 == _TeamPair.SERIES_MAX_WINS or self.wins2 == _TeamPair.SERIES_MAX_WINS

    def get_winner(self):
        if self.wins1 == _TeamPair.SERIES_MAX_WINS:
            return self.tid1
        elif self.wins2 == _TeamPair.SERIES_MAX_WINS:
            return self.tid2
        return 0


class PlayOff:
    def __init__(self, season):
        self.season = season
        self.rounds = []

    def get_data(self):
        schema = _PlayOffSchema()
        today = date.today()
        if today + timedelta(days=14) < self.season.po_start:
            # collect Play-Off info not earlier than 2 weeks before Play-Off start
            return schema.dumps(self)

        db = get_db()
        current_round = 0
        self._create_round0(db)
        if self.season.po_start < today:
            scores = Game.get_play_off_scores(db, self.season.start, self.season.end)
            if len(scores) > 0:
                while self._set_round_scores(current_round, scores):
                    current_round += 1
                    self._create_next_round(current_round)
        return schema.dumps(self)

    def _create_round0(self, db):
        def process_conf(conf, total):
            nonlocal pair_num
            div1, div2 = None, None
            for st in total:
                if conf.div1.teams[0] == st:
                    div1 = conf.div1
                    div2 = conf.div2
                    break
                elif conf.div2.teams[0] == st:
                    div1 = conf.div2
                    div2 = conf.div1
                    break
            self.rounds[0].append(_TeamPair(pair_num, div1.teams[0], conf.wc[1]))
            pair_num += 1
            self.rounds[0].append(_TeamPair(pair_num, div1.teams[1], div1.teams[2]))
            pair_num += 1
            self.rounds[0].append(_TeamPair(pair_num, div2.teams[0], conf.wc[0]))
            pair_num += 1
            self.rounds[0].append(_TeamPair(pair_num, div2.teams[1], div2.teams[2]))
            pair_num += 1

        standings = Standings(self.season)
        all_standings = standings.get_all_standings(db)
        wild_cards = standings.get_wild_cards(db)
        self.rounds.append([])
        pair_num = 0
        # to have the same team pairs order we sort conferences, divisions and teams by id
        if wild_cards[0].cid < wild_cards[1].cid:
            process_conf(wild_cards[0], all_standings)
            process_conf(wild_cards[1], all_standings)
        else:
            process_conf(wild_cards[1], all_standings)
            process_conf(wild_cards[0], all_standings)

    def _create_next_round(self, round_num):
        self.rounds.append([])
        prev_round = self.rounds[round_num - 1]
        for i in range(0, len(prev_round), 2):
            tid1 = prev_round[i].get_winner()
            tid2 = prev_round[i + 1].get_winner()
            if tid1 != 0 or tid2 != 0:
                self.rounds[round_num].append(_TeamPair(i // 2, tid1, tid2))

    def _set_round_scores(self, round_num, scores):
        finished = False
        for r in self.rounds[round_num]:
            key = r.get_key()
            if key in scores:
                r.set_score(scores[key])
                if r.is_finished():
                    finished = True
        return finished and round_num + 1 < ROUNDS_TOTAL


class _TeamPairSchema(ModelSchema):
    num = fields.Integer()
    tid1 = fields.Integer()
    tid2 = fields.Integer()
    wins1 = fields.Integer()
    wins2 = fields.Integer()


class _PlayOffSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    rounds = fields.List(fields.Nested(_TeamPairSchema, many=True))
