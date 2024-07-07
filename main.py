import random
from copy import deepcopy
import time
from termcolor import colored
step = 0


def neighbours(pole, a, b):
    d = {(i, j): pole[i][j] for i in range(len(pole)) for j in range(len(pole[0]))}
    return list([i for i in [(a + 1, b + 1), (a, b + 1), (a + 1, b), (a - 1, b + 1), (a - 1, b), (a, b - 1), (a + 1, b - 1), (a - 1, b - 1)] if d.get(i)])


class Field:

    def __init__(self, n, m, gen=None):
        self.n = n
        self.m = m
        if not gen:
            self.f = []
            for q in range(n):
                cur = []
                for j in range(m):
                    e = random.random()
                    if e <= 0.1:
                        cur.append(Maniac((q, j)))
                    elif e <= 0.35:
                        cur.append(Frank((q, j)))
                    elif e <= 0.45:
                        cur.append(Gypsy((q, j)))
                    elif e <= 0.45 + 0.28:
                        cur.append(Dead((q, j)))
                    else:
                        cur.append(Living((q, j)))
                self.f.append(cur)
                cur = []
        else:
            self.f = gen
        self.next_f = deepcopy(self.f)

    def __str__(self):
        re = ""
        # print(len(self.f))
        for q in self.f:
            re += " ".join(map(lambda x: colored(str(x), x.COLOR), q))
            re += "\n"
        return re[:-1]

    def __next__(self):
        for q in range(self.n):
            for j in range(self.m):
                if not isinstance(self.f[q][j], Dead):
                    self.f = deepcopy(self.f[q][j].action(self.f, self.next_f))

        return self.f

    def __iter__(self):
        while any(any(not isinstance(y, Dead) for y in x) for x in self.f):
            self.f = next(self)
            yield self


class Creature:
    TYPE = "0"
    COLOR = "white"

    def __init__(self, pos=(0, 0)):
        self.pos = pos

    def __str__(self):
        return self.TYPE

    def action(self, prev, new):
        return


class Dead(Creature):
    TYPE = "0"
    COLOR = "white"


class Living(Creature):
    TYPE = "1"
    COLOR = "blue"

    def action(self, prev, new):
        # print(prev)
        # print(new)
        living_count = 0
        for q in neighbours(prev, *self.pos):
            if not isinstance(prev[q[0]][q[1]], Dead):
                living_count += 1
        if living_count < 2 or living_count > 3:
            new[self.pos[0]][self.pos[1]] = Dead()

        return new


class Maniac(Creature):
    TYPE = "M"
    COLOR = "red"

    def action(self, prev, new):
        # print(prev)
        # print(new)
        living_count = 0
        for q in neighbours(prev, *self.pos):
            if not isinstance(prev[q[0]][q[1]], Dead):
                if random.random() <= 0.25:
                    new[q[0]][q[1]] = Dead()
                living_count += 1

        # print(living_count)
        # print(neighbours(prev, *self.pos))
        if living_count == 0:
            new[self.pos[0]][self.pos[1]] = Dead()

        return new


class Frank(Creature):
    TYPE = "F"
    COLOR = "green"

    def action(self, prev, new):
        # print(prev)
        # print(new)
        living_count = 0
        amount_of_neighbours = 0
        for q in neighbours(prev, *self.pos):
            if isinstance(prev[q[0]][q[1]], Dead):
                if random.random() <= 0.2:
                    creation = None
                    e = random.random()
                    if e <= 0.1:
                        creation = Maniac(q)
                    elif e <= 0.25:
                        creation = Frank(q)
                    elif e <= 0.35:
                        creation = Gypsy(q)
                    else:
                        creation = Living(q)
                    new[q[0]][q[1]] = creation
            else:
                living_count += 1
            amount_of_neighbours += 1

        if living_count == amount_of_neighbours:
            new[self.pos[0]][self.pos[1]] = Dead()

        return new


class Gypsy(Creature):
    TYPE = "G"
    COLOR = "yellow"

    def __init__(self, pos=(0, 0)):
        self.pos = pos
        global step
        self.age = step

    def action(self, prev, new):
        available = []
        for q in neighbours(prev, *self.pos):
            if isinstance(prev[q[0]][q[1]], Dead):
                available.append(q)

        global step
        if step - self.age >= 20:
            new[self.pos[0]][self.pos[1]] = Dead()
            return new

        # print(self.pos, available)
        if len(available):
            next_step = random.choice(available)
            new[self.pos[0]][self.pos[1]], new[next_step[0]][next_step[1]] = prev[next_step[0]][next_step[1]], prev[self.pos[0]][self.pos[1]]
            self.pos = next_step
            # print(self.pos, next_step, new[self.pos[0]][self.pos[1]])

        return new


f = Field(10, 10)
print(f"Step #0")
print(f)
step = 1
time.sleep(5)
for i in f:
    print(f"Step #{step}")
    print(i)
    step += 1
    time.sleep(2)

