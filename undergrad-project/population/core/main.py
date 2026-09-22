import random
import time
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from tqdm import tqdm

experiment = 10 ** 3


# enviromental_interactions
def enviroment(T, radius):
    c_T1 = np.ones(T)
    c_T1[0:len(c_T1) // 2] = -1
    t = radius // T
    c_T = c_T1
    for i in range(t - 1):
        c_T = np.append(c_T, c_T1)
    return c_T


def model(sigma_resident, sigma_mutant, enviroment_interactions, enviroment_shifted, mean_fitness_resident,
          mean_fitness_mutant, radius, random_A, random_B):
    win = 0
    time = []
    number_of_experiment_offset = 0
    tau = 0
    for i in range(experiment):
        beta = 1
        # b_mutant
        location_A = random_A[i]
        location_B = random_B[i]
        step = 0
        # print('==================================')
        while True:
            step += 1
            go_to_left_A = mean_fitness_mutant + sigma_mutant * enviroment_interactions[location_A]
            go_to_right_A = mean_fitness_resident + sigma_resident * enviroment_shifted[location_A - 1]
            go_to_left_B = mean_fitness_resident + sigma_resident * enviroment_shifted[location_B]
            go_to_right_B = mean_fitness_mutant + sigma_mutant * enviroment_interactions[location_B - 1]
            # fit_B = sum(mean_fitness_mutant + sigma_mutant * enviroment_interactions[location_A:location_B])
            # fit_A = sum(mean_fitness_resident + sigma_mutant * enviroment_interactions)
            # fit_A -= sum(mean_fitness_resident + sigma_resident * enviroment_interactions[location_A:location_B])
            # surat = go_to_left_B + go_to_right_B + go_to_left_A + go_to_right_A
            # total_fitness = fit_A + fit_B
            # tau += np.random.geometric(surat / (2 * total_fitness))
            movement = \
                random.choices([1, 2, 3, 4], weights=[go_to_right_A, go_to_left_A, go_to_right_B, go_to_left_B], k=1)[0]
            if movement == 1:
                location_A = (location_A + 1) % radius
                beta -= 1
            elif movement == 2:
                location_A = (location_A - 1) % radius
                beta += 1
            elif movement == 3:
                location_B = (location_B + 1) % radius
                beta += 1
            else:
                location_B = (location_B - 1) % radius
                beta -= 1

            if beta == radius:
                win += 1
                # time.append(tau)
                time.append(step)
                break

            elif beta == 0:
                break

            if sigma_mutant == sigma_resident:
                if step > (10 ** 5):
                    number_of_experiment_offset += 1
                    break

    time = np.array(time)
    # print('wins:', win)
    # print(time)
    # print('mean', np.mean(time))

    return win / (experiment - number_of_experiment_offset), np.mean(time)


def heat_map_loc():
    start = time.time()
    sigma_A = np.round(np.arange(-1, 1, 0.05), 2)
    sigma_B = np.round(np.arange(-1, 1, 0.05), 2)
    T = np.array([2])
    enviroment_interactions = enviroment(T[0], 16)
    # print(enviroment_interactions)
    rou_A = np.zeros((len(sigma_A), len(sigma_B)))
    rou_B = np.zeros((len(sigma_A), len(sigma_B)))
    print(len(sigma_B))
    random_A = np.random.randint(0, 15, experiment)
    random_B = random_A + 1
    for j in range(len(T)):
        print(T[j])
        for k in range(len(sigma_B)):
            print(k)
            for i in tqdm(range((len(sigma_A)))):
                rou_B[k, i], _ = model(sigma_A[i], sigma_B[k], enviroment_interactions, enviroment_interactions, 1, 1,
                                       16, random_A, random_B)
                rou_A[k, i], _ = model(sigma_B[k], sigma_A[i], enviroment_interactions, enviroment_interactions, 1, 1,
                                       16, random_A, random_B)

    delta = (rou_A - rou_B).T
    # df = pd.DataFrame(delta)
    # df.to_csv('data_time.csv', index=False)
    maximum = 1
    np.save('fix_2', delta)
    # fix2 = np.load('fix_2.npy')
    plt.colorbar(plt.imshow(delta, vmax=maximum, vmin=-maximum, cmap='seismic', interpolation='bicubic'))
    values = np.equal.outer(rou_A, 1 / 16)
    values2 = np.equal.outer(rou_A, rou_B)
    l = np.round(np.arange(-1, 1, 0.5), 2)
    fit = plt.contour(delta, values, levels=l[::2], linestyles="dashed", colors='blue')
    fit2 = plt.contour(delta, values2, levels=l[::2], linestyles="dashed", colors='red')
    plt.clabel(fit, inline=1, fontsize=10)
    plt.clabel(fit2, inline=1, fontsize=2)
    xticks = plt.gca().get_xticks()
    plt.xticks(xticks[1:] - 0.5, xticks[1:] / len(sigma_A) * 2 - 1)
    plt.yticks(xticks[1:] - 0.5, xticks[1:] / len(sigma_B) * 2 - 1)
    plt.title('T = 2')
    plt.xlabel('sigma_A')
    plt.ylabel('sigma_B')
    plt.show()
    end = time.time()
    print(end - start)


def fixation_time():
    start = time.time()
    sigma = np.arange(0, 0.6, 0.2)
    radius = np.array([16, 32, 64])
    rou_A = np.zeros((len(sigma), len(radius)))
    for i in range(len(sigma)):
        print(sigma[i])
        for k in range(0, len(radius)):
            random_A = np.random.randint(0, radius[k] - 1, size=experiment)
            random_B = random_A + 1
            enviroment_interactions = enviroment(radius[k], radius[k])
            _, rou_A[i, k] = model(-sigma[i], sigma[i], enviroment_interactions, enviroment_interactions, 1, 1,
                                   radius[k], random_A, random_B)
    df = pd.DataFrame(rou_A)
    df.to_csv('data_time.csv', index=False)

    # hossein_data_ scenario1
    T_2 = [[6.80E+02, 5.46E+03, 4.37E+04, 8.53E+04, 1.67E+05],
           [7.08E+02, 5.68E+03, 4.55E+04, 8.89E+04, 1.74E+05],
           [8.08E+02, 6.49E+03, 5.20E+04, 1.02E+05, 1.98E+05],
           [1.06E+03, 8.52E+03, 6.82E+04, 1.33E+05, 2.60E+05],
           [1.87E+03, 1.51E+04, 1.21E+05, 2.37E+05, 4.63E+05]]

    T_16 = [[6.80E+02, 6.85E+02, 7.19E+02, 8.54E+02, 1.40E+03],
            [5.46E+03, 5.97E+03, 8.01E+03, 1.45E+04, 4.98E+04],
            [4.37E+04, 4.86E+04, 6.80E+04, 1.31E+05, 4.74E+05],
            [8.53E+04, 9.50E+04, 1.34E+05, 2.59E+05, 9.43E+05],
            [1.67E+05, 1.86E+05, 2.63E+05, 5.13E+05, 1.89E+06]
            ]
    # T_2 = np.array(T_2)
    for i in range(len(sigma)):
        # plt.plot(radius, T_2[i])
        plt.plot(radius, rou_A[i], 'o-', linestyle='dashed')
    plt.grid()
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel('N')
    plt.ylabel('fixation time')
    plt.show()
    end = time.time()
    print(end - start)


def shift():
    start = time.time()
    radius = 16
    sigma = np.array([0, 0.2, 0.4, 0.6, 0.7, 0.8])
    m = np.arange(0, 18, 2)
    random_A = np.random.randint(0, radius - 1, size=experiment)
    random_B = random_A + 1
    rou_A = np.zeros((len(sigma), len(m)))
    for i in range(len(sigma)):
        print(i)
        for k in (range(len(m))):
            if k > 2:
                rou_A[i, k] = rou_A[i, k - 2]
            else:
                enviroment_interactions = enviroment(4, radius)
                # print(enviroment_interactions)
                enviroment_shifted = np.roll(enviroment_interactions, m[k])
                # print('shifted', enviroment_shifted)
                rou_A[i, k], _ = model(sigma[i], sigma[i], enviroment_interactions, enviroment_shifted, 1, 1, radius,
                                       random_A, random_B)
    for k in range(len(sigma)):
        plt.plot(m, rou_A[k], linestyle='dashed')
    df = pd.DataFrame(rou_A)
    df.to_csv('data.csv', index=False)

    # hossein_data
    T_4 = [[6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02],
           [6.25E-02, 6.00E-02, 6.25E-02, 6.00E-02, 6.25E-02, 6.00E-02, 6.25E-02, 6.00E-02, 6.25E-02],
           [6.25E-02, 5.45E-02, 6.25E-02, 5.45E-02, 6.25E-02, 5.45E-02, 6.25E-02, 5.45E-02, 6.25E-02],
           [6.25E-02, 4.35E-02, 6.25E-02, 4.35E-02, 6.25E-02, 4.35E-02, 6.25E-02, 4.35E-02, 6.25E-02],
           [6.25E-02, 3.50E-02, 6.25E-02, 3.50E-02, 6.25E-02, 3.50E-02, 6.25E-02, 3.50E-02, 6.25E-02],
           [6.25E-02, 2.51E-02, 6.25E-02, 2.51E-02, 6.25E-02, 2.51E-02, 6.25E-02, 2.51E-02, 6.25E-02]]
    periods = [np.array(T_4).T]
    colors = ['yellow', 'orange', 'green', 'red', 'purple', 'yellow']
    for k in range(len(periods)):
        plt.plot(m, periods[k])
    plt.grid()
    plt.xlabel('m')
    plt.ylabel('fixation probability')
    plt.show()
    end = time.time()
    print(end - start)


def shift_time():
    start = time.time()
    radius = 16
    sigma = np.array([0, 0.2, 0.4, 0.6, 0.7, 0.8])
    m = np.arange(0, 18, 2)
    random_A = np.random.randint(0, radius - 1, size=experiment)
    random_B = random_A + 1
    rou_A = np.zeros((len(sigma), len(m)))
    for i in range(len(sigma)):
        print(i)
        for k in (range(len(m))):
            # if k > 2:
            #     rou_A[i, k] = rou_A[i, k - 2]
            # else:
            enviroment_interactions = enviroment(16, radius)
            # print(enviroment_interactions)
            enviroment_shifted = np.roll(enviroment_interactions, m[k])
            # print('shifted', enviroment_shifted)
            _, rou_A[i, k] = model(sigma[i], sigma[i], enviroment_interactions, enviroment_shifted, 1, 1, radius,
                                   random_A, random_B)
    for k in range(len(sigma)):
        plt.plot(m, rou_A[k], linestyle='dashed')
    df = pd.DataFrame(rou_A)
    df.to_csv('data.csv', index=False)

    # hossein_data
    T_4 = [[6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02],
           [6.25E-02, 6.00E-02, 6.25E-02, 6.00E-02, 6.25E-02, 6.00E-02, 6.25E-02, 6.00E-02, 6.25E-02],
           [6.25E-02, 5.45E-02, 6.25E-02, 5.45E-02, 6.25E-02, 5.45E-02, 6.25E-02, 5.45E-02, 6.25E-02],
           [6.25E-02, 4.35E-02, 6.25E-02, 4.35E-02, 6.25E-02, 4.35E-02, 6.25E-02, 4.35E-02, 6.25E-02],
           [6.25E-02, 3.50E-02, 6.25E-02, 3.50E-02, 6.25E-02, 3.50E-02, 6.25E-02, 3.50E-02, 6.25E-02],
           [6.25E-02, 2.51E-02, 6.25E-02, 2.51E-02, 6.25E-02, 2.51E-02, 6.25E-02, 2.51E-02, 6.25E-02]]
    periods = [np.array(T_4).T]
    colors = ['yellow', 'orange', 'green', 'red', 'purple', 'yellow']
    # for k in range(len(periods)):
    #     plt.plot(m, periods[k])
    plt.grid()
    plt.xlabel('m')
    plt.ylabel('fixation time')
    plt.show()
    end = time.time()
    print(end - start)


def move_in_vertical():
    start = time.time()
    sigma = np.arange(0, 0.8 + 0.05, 0.05)
    print(len(sigma))
    T = np.array([2, 4, 8, 16])
    random_A = np.random.randint(0, 15, experiment)
    random_B = random_A + 1
    df = [[model(-sigma[i], sigma[i], enviroment(T[j], 16), enviroment(T[j], 16), 1.1, 1, 16,
                 random_A, random_B) for i in range(len(sigma))] for j in range(len(T))]

    df = pd.DataFrame(df)
    df.to_csv('data.csv', index=False)

    # hossein_data
    T_16 = np.array(
        [6.25E-02, 6.39E-02, 6.82E-02, 7.49E-02, 8.36E-02, 9.39E-02, 1.05E-01, 1.17E-01, 1.28E-01, 1.39E-01, 1.50E-01,
         1.60E-01, 1.69E-01, 1.78E-01, 1.86E-01, 1.94E-01, 2.01E-01,
         ])
    T_8 = np.array(
        [6.25E-02, 6.24E-02, 6.20E-02, 6.13E-02, 6.03E-02, 5.91E-02, 5.75E-02, 5.55E-02, 5.32E-02, 5.05E-02, 4.74E-02,
         4.39E-02, 4.01E-02, 3.60E-02, 3.15E-02, 2.68E-02, 2.18E-02,
         ])
    T_2 = np.array(
        [6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02,
         6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02, 6.25E-02
         ])
    T_4 = np.array(
        [6.25E-02, 6.24E-02, 6.20E-02, 6.13E-02, 6.04E-02, 5.93E-02, 5.78E-02, 5.61E-02, 5.41E-02, 5.17E-02, 4.91E-02,
         4.62E-02, 4.29E-02, 3.92E-02, 3.52E-02, 3.07E-02, 2.57E-02])
    periods = [T_2, T_4, T_8, T_16]
    colors = ['blue', 'orange', 'green', 'red']
    for k in range(len(periods)):
        plt.plot(sigma, periods[k], color=colors[k])

    plt.xlabel('sigma')
    plt.ylabel('fixation probability of "A"')
    plt.grid()
    plt.show()
    end = time.time()
    print(end - start)


heat_map_loc()
