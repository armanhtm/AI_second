import operator
import random
from random import randint

import matplotlib.pyplot as plt


# this class hold information of kromozom
class kromozom_class:
    def __init__(self, kromozom, score):
        self.kromozom = kromozom
        self.score = score


# this function create new random kromozoms
def new_kromozoms(number, length):
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

    #print(sequence, step, score, live)
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
        kromozoms.sort(key=lambda x: x.score, reverse=False)
        output_kromozom = []
        for i in range(len(kromozoms)):
            sum_score += kromozoms[i].score
        for i in range(number):
            #random = randint(int(sum_score / 2), sum_score)
            rand = pow(random.random(),0.25)
            rand = int(rand * len(kromozoms))
            output_kromozom.append(kromozoms[rand])
        return output_kromozom


# this function is for Recombinance two kromozom to childs
def Recombination(parent_kromozom1, parent_kromozom2, child_number, single_dot):
    child_kromozom = []
    if single_dot:
        for i in range(child_number):
            random = randint(1, len(parent_kromozom1))
            child_kromozom.append(parent_kromozom1[:random] + parent_kromozom2[random:])
            child_kromozom.append(parent_kromozom2[:random] + parent_kromozom1[random:])
        return child_kromozom
    else:
        for i in range(child_number):
            random1 = 0
            random2 = 0
            while random1 != random2:
                random1 = randint(1, len(parent_kromozom1))
                random2 = randint(1, len(parent_kromozom1))
            child = []
            for i in range(len(parent_kromozom1)):
                if i < random1 or i > random2:
                    child.append(parent_kromozom1[i])
                else:
                    child.append(parent_kromozom2[i])
            child_kromozom.append(child)
        return child_kromozom

# this function is for Recombination in main
def Recombination_main(kromozoms_parent, multiplication,single_dot):
    kromozoms_child = []
    counter = -1
    while counter < len(kromozoms_parent) - 1:
        if counter+1 >= len(kromozoms_parent):
            break
        for kromozom in Recombination(kromozoms_parent[counter + 1], kromozoms_parent[counter + 2], multiplication,single_dot):
            kromozoms_child.append(kromozom)
        counter += 2
    return kromozoms_child


# possibility is between 0 to 100
# bit number that have mutation
# mutation is oriented or not
# mutation function
def Mutation(kromozom, possibility, bit_number, oriented):
    if not oriented:
        possibility_random_number = randint(0, 100)
        if possibility_random_number < possibility:
            for counter in range(bit_number):
                bit_random_number = randint(0, len(kromozom) - 1)
                bit_random_value = randint(0, 2)
                kromozom[bit_random_number] = bit_random_value

        return kromozom

    if oriented:
        pass


# possibility is between 0 to 100
# bit number that have mutation
# mutation is oriented or not
# mutation main function
def Mutation_main(kromozoms, possibility, bit_number, oriented):
    for kromozom in kromozoms:
        Mutation(kromozom, possibility, bit_number, oriented)
    return kromozoms


def show_graph(y, x, title, x_label, y_label):
    plt.plot(y, x)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()




kromozoms = []
kromozoms_class = []
level = input("enter level:")
kromozoms = new_kromozoms(len(level), 200)
#print("jkdfj",kromozoms[0])
#print(select(0,5,kromozoms))
print("start")
best = []
index = []
worst = []
for i in range(200):
    for kromozom in kromozoms:
        number = competenceFunction(level, kromozom)
        p1 = kromozom_class(kromozom,number )
        kromozoms_class.append(p1)
    selected_kromozoms_class = select(50, 100, kromozoms_class)
    print(selected_kromozoms_class[0].score,"   ",selected_kromozoms_class[0].kromozom)
    best.append(selected_kromozoms_class[0].score)
    index.append(i)
    worst.append(selected_kromozoms_class[len(selected_kromozoms_class)-1].score)
    selected_kromozoms = []
    for kromozom_class_0 in selected_kromozoms_class:
        selected_kromozoms.append(kromozom_class_0.kromozom)
    recombination_kromozoms = []
    recombination_kromozoms = Recombination_main(selected_kromozoms, 4,False)
    mutation_kromozoms = []
    mutation_kromozoms = Mutation_main(recombination_kromozoms,20,1,False)
    kromozoms = mutation_kromozoms

#print(select(0 , 5 , kromozoms))


show_graph(index,best,"max score","generation","score")