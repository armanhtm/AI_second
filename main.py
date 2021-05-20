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
        output_kromozom = []
        for i in range(len(kromozoms)):
            kromozoms[i].chance_number(sum_score, sum_score + kromozoms[i].score)
            sum_score += kromozoms[i].score
        for i in range(number):
            random = randint(1, sum_score)
            for kromozom0 in kromozoms:
                if kromozom0.first <= random <= kromozom0.second:
                    output_kromozom.append(kromozom0)

        return output_kromozom


# this function is for Recombinance two kromozom to childs
def Recombination(parent_kromozom1, parent_kromozom2, child_number):
    child_kromozom = []
    for i in range(child_number):
        random = randint(1, len(parent_kromozom1))
        child_kromozom.append(parent_kromozom1[:random] + parent_kromozom2[random:])
        child_kromozom.append(parent_kromozom2[:random] + parent_kromozom1[random:])
    return child_kromozom


# this function is for Recombination in main
def Recombination_main(kromozoms_parent, multiplication):
    kromozoms_child = []
    counter = -1
    while counter < len(kromozoms_parent) - 1:
        if counter+1 >= len(kromozoms_parent) or counter+2 >= len(kromozoms_parent):
            break
        for kromozom in Recombination(kromozoms_parent[counter + 1], kromozoms_parent[counter + 2], multiplication):
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


kromozoms = []
kromozoms_class = []
level = input("enter level:")
kromozoms = new_kromozoms(12, 50)
#print("jkdfj",kromozoms[0])
#print(select(0,5,kromozoms))
print("start")
for i in range(200):
    for kromozom in kromozoms:
        number = competenceFunction(level, kromozom)
        p1 = kromozom_class(kromozom,number )
        kromozoms_class.append(p1)
    selected_kromozoms_class = select(0, 100, kromozoms_class)
    print(selected_kromozoms_class[0].score,"   ",selected_kromozoms_class[0].kromozom)
    selected_kromozoms = []
    for kromozom_class_0 in selected_kromozoms_class:
        selected_kromozoms.append(kromozom_class_0.kromozom)
    recombination_kromozoms = []
    recombination_kromozoms = Recombination_main(selected_kromozoms, 4)
    mutation_kromozoms = []
    mutation_kromozoms = Mutation_main(recombination_kromozoms,50,1,False)
    kromozoms = mutation_kromozoms

#print(select(0 , 5 , kromozoms))





p1 = kromozom_class("ali", 10)
p2 = kromozom_class("alli", 40)
p3 = kromozom_class("allli", 30)
array = []
array.append(p1)
array.append(p2)
array.append(p3)
# for kromozom in select(50, 2, array):
#    print(kromozom.score)
l = [0, 1, 2, 3, 4]
l2 = [5, 6, 7, 8, 9]
l3 = [10, 11, 12, 13, 14]
l4 = [15, 16, 17, 18, 19]
l_main = []
l_main.append(l)
#print("jldkjfjdlkj")
#print(new_kromozoms(2,5))
l_main.append(l2)
l_main.append(l3)
#l_main.append(l4)
# print(Recombination_main(l_main, 4))
#print(Mutation_main(l_main, 100, 1, False))
# kromozoms = newKromozom(5, 6)
# print(kromozoms)
# print(competenceFunction("____G_ML__G_", [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]))
