import random
from random import randint
import turtle
import matplotlib.pyplot as plt


# this class hold information of kromozom
class kromozom_class:
    def __init__(self, kromozom, score, live):
        self.kromozom = kromozom
        self.score = score
        self.live = live


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

        if (kromozom[i - 1] == 2 or kromozom[i - 1] == 1) and kromozom[i] != 0:
            live = False
            score -= 10

        if sequence_counter > sequence:
            sequence = sequence_counter

    if kromozom[len(kromozom) - 1] == 1:
        score += 10

    if live and win:
        score *= 1.1

    # print(sequence, step, score, live)
    return (sequence + step) * score, live


# this function selects number kromozom with chance percentage
def select(chance, number, kromozoms):
    # no chance
    if chance == False:
        kromozoms.sort(key=lambda x: x.score, reverse=True)
        return kromozoms[:number]

    # select with chance and score
    if chance == True:
        sum_score = 0
        kromozoms.sort(key=lambda x: x.score, reverse=False)
        output_kromozom = []
        for i in range(len(kromozoms)):
            sum_score += kromozoms[i].score
        for i in range(number):
            # random = randint(int(sum_score / 2), sum_score)
            rand = pow(random.random(), 0.25)
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
def Recombination_main(kromozoms_parent, multiplication, single_dot):
    kromozoms_child = []
    counter = -1
    while counter < len(kromozoms_parent) - 1:
        if counter + 1 >= len(kromozoms_parent):
            break
        for kromozom in Recombination(kromozoms_parent[counter + 1], kromozoms_parent[counter + 2], multiplication,
                                      single_dot):
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







def calculate_average_score(kromozoms):
    sum_score = 0
    for kromozom in kromozoms:
        sum_score += kromozom.score

    return sum_score / len(kromozoms)


def list_to_string(list_int):
    string_ints = [str(element) for element in list_int]
    string = ""
    for i in string_ints:
        string += i
    return string

kromozoms = []
kromozoms_class = []
level = input("enter level : ")
population = int(input("population number : "))
generation_number = int(input("Generation number : "))
chance_number = int(input("1=best selection or 2=best_chance selection?(1/2) : "))
recombination_dot_number = input("single dot recombination : (y/n)")
if recombination_dot_number == 'y':
    single_dot = True
else:
    single_dot = False
mutation_percentage = int(input("Percentage of Mutation : "))
if chance_number == 1:
    chance = False
else:
    chance = True
consider_win = input("care about wining : (y/n)")
if consider_win == 'y':
    win = True
else:
    win = False
kromozoms = new_kromozoms(len(level), population)
print("start")
best = []
index = []
worst = []
average = []
output_kromozoms_class = []
for i in range(generation_number):
    for kromozom in kromozoms:
        number = competenceFunction(level, kromozom)[0]
        live = competenceFunction(level, kromozom)[1]
        p1 = kromozom_class(kromozom, number, live)
        kromozoms_class.append(p1)
    selected_kromozoms_class = select(chance, 100, kromozoms_class)
    selected_kromozoms_class.sort(key=lambda x: x.score, reverse=True)
    last = len(selected_kromozoms_class) - 1
    average_score = calculate_average_score(selected_kromozoms_class)
    print(i, "-->", "best:", selected_kromozoms_class[0].score, "   ", selected_kromozoms_class[0].live, "   ",
          selected_kromozoms_class[0].kromozom)
    print("      ", "worst:", selected_kromozoms_class[last].score, "   ", selected_kromozoms_class[last].live, "   ",
          selected_kromozoms_class[last].kromozom)
    print("      ", "average:", average_score)
    best.append(selected_kromozoms_class[0].score)
    index.append(i)
    worst.append(selected_kromozoms_class[len(selected_kromozoms_class) - 1].score)
    average.append(average_score)
    selected_kromozoms = []
    output_kromozoms_class = selected_kromozoms_class[0].kromozom
    for kromozom_class_0 in selected_kromozoms_class:
        selected_kromozoms.append(kromozom_class_0.kromozom)
    recombination_kromozoms = []
    recombination_kromozoms = Recombination_main(selected_kromozoms, 4, single_dot)
    mutation_kromozoms = []
    mutation_kromozoms = Mutation_main(recombination_kromozoms, mutation_percentage,1,False)
    kromozoms = mutation_kromozoms
path = list_to_string(output_kromozoms_class)
plt.plot(index, best,label="best_score")
plt.plot(index, worst, label="worst_score")
plt.plot(index, average, label="average_score")
plt.title("Graph")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.legend()
plt.show()
high_score = selected_kromozoms_class[0].score
alive = selected_kromozoms_class[0].live
wn = turtle.Screen()
wn.bgcolor("blue")
mario = turtle.Turtle()
mario.penup()
mario.goto(((len(level) - len(level) / 2) + 1) * -14.7, -22.5)
mario.shape("turtle")
mario.color("purple")
earth = turtle.Turtle()
earth.penup()
earth.goto(-400,-250)
earth.pendown()
earth.shape("square")
earth.shapesize(20,120)
earth.color("maroon")
field = turtle.Turtle()
field.penup()
field.goto(-400,-50)
field.pendown()
field.shape("square")
field.shapesize(2,120)
field.color("green")
sun = turtle.Turtle()
sun.penup()
sun.goto(300,300)
sun.pendown()
sun.shape("circle")
sun.shapesize(5)
sun.color("yellow")
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(-450, 300)
pen.write("Score : {}   alive : {} ".format(
            high_score, alive), align="center", font=("candara", 24, "bold"))

for i in range(1, len(level)):
    current_step = level[i]
    if current_step == 'G':
        Gumpa = turtle.Turtle()
        Gumpa.penup()
        Gumpa.goto((i - len(level) / 2) * 14.7 , -25)
        Gumpa.pendown()
        Gumpa.shape("square")
        Gumpa.shapesize(0.5)
        Gumpa.color("red")
    if current_step == 'L':
        Lukido = turtle.Turtle()
        Lukido.penup()
        Lukido.goto((i - len(level) / 2) * 14.7, 0)
        Lukido.pendown()
        Lukido.shape("circle")
        Lukido.shapesize(0.5)
        Lukido.color("red")
    if current_step == 'M':
        Mashroom = turtle.Turtle()
        Mashroom.penup()
        Mashroom.goto((i - len(level) / 2) * 14.7, -25)
        Mashroom.pendown()
        Mashroom.shape("triangle")
        Mashroom.shapesize(0.5)
        Mashroom.color("gold")

flag = turtle.Turtle()
flag.penup()
flag.goto(((len(level) - len(level) / 2) + 1) * 14.7, -25)
flag.pendown()
flag.left(90)
flag.forward(25)
flag.color("green")
flag.right(90)
flag.forward(8)
mario.pendown()
mario.speed(2)
mario.forward(7.35)
for i in range(len(path)):
    if i >= 2:
        if path[i - 2] == '1':
            mario.right(90)
            mario.forward(25)
            mario.left(90)
        if path[i - 2] == '2':
            mario.left(90)
            mario.forward(5)
            mario.right(90)
    if path[i] == '0':
        mario.forward(14.7)
    if path[i] == '1':
        mario.forward(14.7)
        mario.left(90)
        mario.forward(25)
        mario.right(90)
    if path[i] == '2':
        mario.forward(14.7)
        mario.right(90)
        mario.forward(5)
        mario.left(90)
wn.mainloop()
