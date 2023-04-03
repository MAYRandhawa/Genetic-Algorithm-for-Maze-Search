from random import *
from pyamaze import *

def Generate_Random_Population():
    '''Generating random population "population" '''
    return [[[1]+[randint(1, rows) for _ in range(columns-2)]+[rows], [randint(0, 1) for _ in range(2)]] for _ in range(pop_size)]

def Check_Turns():
    '''Returning Turns of a particular chromosome'''
    return [sum([1 for k in range(columns-1) if j[k] != j[k+1]]) for j, o in population]

def Check_Obstacle(a: tuple, b: tuple):
    '''Check the obstacle in the way of Robot in a particular cell & according to its movement.'''
    if (b[0]-a[0] != 0):
        if (b[0]-a[0] > 0):
            if dic_maze[a]['S'] == 0: return 1
        else:
            if dic_maze[a]['N'] == 0: return 1
    elif (b[1]-a[1] != 0):
        if (b[1]-a[1] > 0):
            if dic_maze[a]['E'] == 0: return 1
        else:
            if dic_maze[a]['W'] == 0: return 1
    return 0

def Check_infsteps_pathlength(l: list):
    '''Returning Infeasibile Steps, Path & Path Length of a particular chromosome'''
    chr, [Orn, Dir] = l
    path, inf_steps, p_p, k = [], [], (1, 1), 1
    if check == 1: path.append((1, 1))
    if rows != columns: Orn = 0
    decisoin = Orn ^ Dir
    for gene in range(0, len(chr)-1):
        next = gene+1
        limit = (chr[gene+1]+1) if chr[gene+1] > chr[gene] else (chr[gene+1]-1)
        while k != limit:
            if Orn == 0: n_p = (k, next+decisoin)
            else: n_p = (next+decisoin, k)
            if check == 1 and n_p not in ((1, 1), (rows, columns)): path.append(n_p)
            inf_steps.append(Check_Obstacle(p_p, n_p))
            p_p = n_p
            if chr[gene+1] > chr[gene]: k += 1
            else: k -= 1
        if chr[gene+1] > chr[gene]: k -= 1
        else: k += 1
    Len = len(inf_steps)
    if rows < columns or rows == columns:
        inf_steps.append(Check_Obstacle(p_p, (rows, columns)))
        Len -= 1
    if check == 1:
        path.append((rows, columns))
        return path, len(inf_steps), sum(inf_steps)
    return len(inf_steps), sum(inf_steps)

def Crossover(l: list):
    s_p, cr_p = int(pop_size/2), randint(2, columns-2)
    for i in range(s_p, (pop_size-1), 2):
        l[i][0] = l[i-s_p][0][0:cr_p]+l[i-s_p+1][0][cr_p:]
        l[i+1][0] = l[i-s_p+1][0][0:cr_p] + l[i-s_p][0][cr_p:]

def Mutation(l: list):
    for i in range(pop_size):
        Gene, Or_Dir = l[i]
        Gene[randint(2, columns-2)] = randint(1, rows)
        if i >= int(pop_size/2): Or_Dir[0], Or_Dir[1] = randint(0, 1), randint(0, 1)

def Actual_Fitness(t, p_l, f):
    f_f = 1-(f-inf_min)/(max(f_storing)-inf_min)
    # f_inf=1-(infeasible-min(f_storing))/(max(f_storing)-min(f_storing))
    f_t = 1-(t-min(t_storing))/(max(t_storing)-min(t_storing))
    f_l = 1-(p_l-min(p_l_storing)) / (max(p_l_storing)-min(p_l_storing))
    return (100*w_f*f_f)*((w_l*f_l)+(w_t*f_t))/(w_l+w_t)

'''Main Funtion'''
rows = 10
columns = 10
pop_size = 200
iter = 0
inf_min, w_f, w_t, w_l = 0, 3, 3, 2
p_l_storing, f_storing, t_storing, fitness, check = [], [], [], [], 0
m = maze(rows, columns)
m.CreateMaze(rows, columns, loopPercent=100)
a = agent(m, 1, 1, filled=True, footprints=True, color='yellow')
dic_maze = m.maze_map
population = Generate_Random_Population()
while (iter < 2500):
    print(f'Generation: {iter}')
    p_l_storing, f_storing, fitness = [], [], []
    t_storing = Check_Turns()
    inf_steps = [Check_infsteps_pathlength(chromosome) for chromosome in population]
    for i in range(pop_size):
        p_l_storing.append(inf_steps[i][0])
        f_storing.append(inf_steps[i][1])
    for i in range(pop_size):
        fitness.append(Actual_Fitness(t_storing[i], p_l_storing[i], f_storing[i]))
        if f_storing[i] == 0:
            check = 1
            sol_p, sol_p_l, sol_f = Check_infsteps_pathlength(population[i])
            sol_t = t_storing[i]
            print(f'\033[92m\nChromosome = {population[i][0]}\nTurns = {sol_t}\nPath Length = {sol_p_l}\nInfeasible Steps = {sol_f}\nPath = {sol_p}\n')
            # m.tracePath({a: sol_p}, delay=100)
            m.run()
            break
    if check == 1:
        break
    # Sorting on the basis of Actual_Fitness
    pop = list(zip(population, fitness))
    Sorted_pop = sorted(pop, key=lambda x: x[1], reverse=True)
    population = [x[0] for x in Sorted_pop]
    t = list(zip(t_storing, fitness))
    Sorted_t = sorted(t, key=lambda x: x[1], reverse=True)
    t_storing = [x[0] for x in Sorted_t]
    Crossover(population)
    Mutation(population)
    iter += 1
else:
    print(f'\033[91m------------------------------\nSolution not found. Try Again!\n------------------------------')
