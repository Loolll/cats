from modules.place import Place
from modules.animal import Leader
from modules.exceptions import AlreadyInFightException


class AbstractFight:
    active_leaders = set()
    def __init__(self, leader1: Leader, leader2: Leader, place: Place):
        if leader1 in AbstractFight.active_leaders or leader2 in AbstractFight.active_leaders:
            raise AlreadyInFightException
        self.leader1 = leader1
        AbstractFight.active_leaders.add(leader1)
        self.leader2 = leader2
        AbstractFight.active_leaders.add(leader2)
        self.place = place

    def __call__(self, *args, **kwargs):
        with self.leader1 as leader1, self.leader2 as leader2:
            winner = self._fight_loop(leader1,leader2)
            if winner is self.leader1:
                pass
            else:
                pass

    def _fight_loop(self, leader1: Leader, leader2: Leader) -> Leader:
        while not leader1.defeated and not leader2.defeated:
            self._first_move()
            self._second_move()
        if leader2.defeated:
            return leader1
        return leader2

    def _first_move(self):
        pass

    def _second_move(self):
        pass

