import numpy as np
import random
import time
from colorama import Fore, Style, init

init(autoreset=True)

def final_test(test_fin, pop_total):
    fin = True
    for i in range(len(pop_total)):
        if test_fin[0][i] != pop_total[i] or test_fin[1][i] != pop_total[i]:
            fin = False
    return fin

def array_overflow(grid, num_pop, neighbors, l, c): 
    l = (l % grid.shape[0] + grid.shape[0]) % grid.shape[0]
    c = (c % grid.shape[1] + grid.shape[1]) % grid.shape[1]
    if grid[l, c] == num_pop * 10 + 1 or grid[l, c] == num_pop * 10 + 3:
        neighbors += 1
    return neighbors

def neighborhood(grid, num_pop, i, j, rang): 
    neighbors = 0
    for l in range(i - rang, i + rang + 1):
        for c in range(j - rang, j + rang + 1):
            neighbors = array_overflow(grid, num_pop, neighbors, l, c)
    return neighbors

def end_gen_transition(grid, num_pop):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == num_pop * 10 + 2:
                grid[i, j] = num_pop * 10 + 1
            elif grid[i, j] == num_pop * 10 + 3:
                grid[i, j] = 0

def rule_4b(grid, total_population, num_pop, i, j): 
    exception = False
    for n_pop in range(len(total_population)):
        neighbors = neighborhood(grid, n_pop, i, j, 1)
        if n_pop != num_pop and neighbors == 3:
            neighbors1 = neighborhood(grid, n_pop, i, j, 2)
            neighbors2 = neighborhood(grid, num_pop, i, j, 2)
            if neighbors1 == neighbors2:
                if total_population[n_pop] > total_population[num_pop]:
                    grid[i, j] = n_pop * 10 + 2
                elif total_population[n_pop] < total_population[num_pop]:
                    grid[i, j] = num_pop * 10 + 2
                else:
                    exception = True
            elif neighbors1 > neighbors2:
                grid[i, j] = n_pop * 10 + 2
            else:
                grid[i, j] = num_pop * 10 + 2
    if grid[i, j] == 0 and not exception:
        grid[i, j] = num_pop * 10 + 2

def next_generation(grid, total_population, test_fin):
    populations = np.zeros_like(total_population)
    for num_pop in range(len(total_population)):
        end_gen_transition(grid, num_pop)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == num_pop * 10 + 1:
                    neighbors = neighborhood(grid, num_pop, i, j, 1)
                    neighbors -= 1
                    if neighbors < 2 or neighbors > 3:
                        grid[i, j] = num_pop * 10 + 3
                if grid[i, j] == 0:
                    neighbors = neighborhood(grid, num_pop, i, j, 1)
                    if neighbors == 3:
                        rule_4b(grid, total_population, num_pop, i, j)
                if grid[i, j] == num_pop * 10 + 1 or grid[i, j] == num_pop * 10 + 2:
                    populations[num_pop] += 1
    for i in range(len(populations)):
        test_fin[0][i] = test_fin[1][i]
        test_fin[1][i] = total_population[i]
        total_population[i] = populations[i]

def initialization(grid, total_population, test_fin, fill_rate):
    grid.fill(0)
    nb_cell_dep = round(grid.size * fill_rate)
    nb_cell_dep //= len(total_population)
    pop = 0
    for i in range(0, len(total_population) * 10, 10):
        rand_column = 0
        rand_row = 0
        for j in range(nb_cell_dep):
            while True:
                rand_row = random.randint(0, grid.shape[0] - 1)
                rand_column = random.randint(0, grid.shape[1] - 1)
                if grid[rand_row, rand_column] == 0:
                    break
            grid[rand_row, rand_column] = i + 1
        total_population[pop] = nb_cell_dep
        test_fin[1][pop] = nb_cell_dep
        pop += 1

def display_title():
    print(Fore.BLUE + "=====================================")
    print(Fore.RED + "     Game of Life with Populations    ")
    print(Fore.BLUE + "=====================================" + Style.RESET_ALL)

def display_grid(grid, visu, total_population, generation):
    print()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 0 or grid[i, j] % 10 == 3:
                if grid[i, j] % 10 == 3 and visu:
                    print(Fore.YELLOW + "*", end=" ")
                else:
                    print(".", end=" ")
            elif grid[i, j] % 10 == 1 or grid[i, j] % 10 == 2:
                if grid[i, j] % 10 == 2 and visu:
                    print(Fore.RED + "-", end=" ")
                else:
                    print(Fore.GREEN + "#", end=" ")
        print()

    if visu:
        print(Fore.BLUE + " T" + str(generation) + "+" + Style.RESET_ALL)
        print()
        display_grid(grid, False, total_population, generation)
    else:
        generation += 1
        print(Fore.BLUE + " T" + str(generation), end="")
        for i in range(1, len(total_population) + 1):
            print(Fore.GREEN + " / Pop " + str(i) + ": " + str(total_population[i - 1]), end="")
        print(Style.RESET_ALL)
        print()

def main():
    display_title()

    n_row = int(input("How many rows? "))
    n_column = int(input("How many columns? "))
    nb_pop = int(input("How many populations? "))
    fill_rate = float(input("Initial cell fill rate? (between 0.1 and 0.9) "))
    visu_str = input("Game with future state visualization? (True/False) ")
    visu = visu_str.lower() == 'true'

    grid = np.zeros((n_row, n_column), dtype=int)
    generation = 0
    total_population = np.zeros(nb_pop, dtype=int)
    test_fin = np.zeros((2, nb_pop),

 dtype=int)
    initialization(grid, total_population, test_fin, fill_rate)
    display_grid(grid, False, total_population, generation)

    while not final_test(test_fin, total_population):
        time.sleep(1)
        next_generation(grid, total_population, test_fin)
        display_grid(grid, visu, total_population, generation)
        generation += 1

if __name__ == "__main__":
    main()