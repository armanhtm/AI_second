import operator
from random import randint
from toolz import partition


# this class hold information of kromozom
class kromozom_class:
    def __init__(self, kromozom, score):
        self.kromozom = kromozom
        self.score = score

    def chance_number(self, first, second):
        self.first = first
        self.second = second


# this function create new random kromozoms
def newKromozom(number, length):
    kromozoms = [[randint(0, 2) for i in range(number)] for j in range(length)]
    return kromozoms


# this function return competence of kromozom
def competenceFunction(level, kromozom):
    live = True
    sequence = 0
    sequence_counter = 0
    step = 0
    score = 0
    for i in range(1, len(level)):
        current_step = level[i]

        if current_step == '_':
            sequence_counter += 1
            step += 1
            if kromozom[i - 1] == 0:
                score += 10
            else:
                score += 5

        if current_step == 'G':

            if i >= 2 and kromozom[i - 2] == 1 and kromozom[i - 1] == 0:
                score += 20
                sequence_counter += 1
                step += 1

            if kromozom[i - 1] == 1:
                score += 5
                sequence_counter += 1
                step += 1

            if (i >= 2 and kromozom[i - 2] != 1) and (kromozom[i - 1] == 0 or kromozom[i - 1] == 2):
                if sequence_counter > sequence:
                    sequence = sequence_counter
                sequence_counter = 0
                live = False

            if i == 1 and kromozom[0] == 1:
                step += 1
                sequence_counter += 1
                score += 5
            if i == 1 and kromozom[0] != 1:
                if sequence_counter > sequence:
                    sequence = sequence_counter
                sequence_counter = 0
                live = False

        if current_step == 'M':
            sequence_counter += 1
            step += 1
            if kromozom[i - 1] == 0:
                score += 30
            if kromozom[i - 1] == 2:
                score += 20
            if kromozom[i - 1] == 1:
                score += 10

        if current_step == 'L':
            if kromozom[i - 1] == 2:
                score += 10
                sequence_counter += 1
                step += 1
            else:
                live = False
                if sequence_counter > sequence:
                    sequence = sequence_counter
                sequence_counter = 0

        if sequence_counter > sequence:
            sequence = sequence_counter

    if kromozom[len(kromozom) - 1] == 1:
        score += 10

    if live:
        score *= 1.1

    print(sequence, step, score, live)
    return (sequence + step) * score


# this function selects number kromozom with chance percentage
def select(chance, number, kromozoms):
    # no chance
    if chance == 0:
        kromozoms.sort(key=lambda x: x.score, reverse=True)
        return kromozoms[:number]

    # completely chance
    if chance == 100:
        output_kromozoms = []
        kromozoms_index = []
        counter = number
        while counter != 0:
            i = randint(0, len(kromozoms) - 1)
            if not kromozoms_index.__contains__(i):
                kromozoms_index.append(i)
                output_kromozoms.append(kromozoms[i])
                counter -= 1
        return output_kromozoms

    # select with chance and score
    if chance == 50:
        sum_score = 0
        output_kromozom = []
        for i in range(len(kromozoms)):
            kromozoms[i].chance_number(sum_score, sum_score + kromozoms[i].score)
            sum_score += kromozoms[i].score
        for i in range(number):
            random = randint(0, sum_score)
            for kromozom0 in kromozoms:
                if kromozom0.first <= random <= kromozom0.second:
                    output_kromozom.append(kromozom0)

        return output_kromozom


p1 = kromozom_class("ali", 10)
p2 = kromozom_class("alli", 40)
p3 = kromozom_class("allli", 30)
array = []
array.append(p1)
array.append(p2)
array.append(p3)
for kromozom in select(50, 2, array):
    print(kromozom.score)

# kromozoms = newKromozom(5, 6)
# print(kromozoms)
# print(competenceFunction("____G_ML__G_", [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]))
