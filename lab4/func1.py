import time
import numpy as np
import threading
import random

def zero(n,m, num = 0):
    res = []
    for i in range(n):
        res.append([])
        for j in range(m):
            res[i].append(random.randint(1,100))
    return res

def zero_vector(n):
    res = []
    for i in range(n):
        res.append(0)
    return res

# def mult(matr1, matr2):
#     start = time.clock()
#     m1 = len(matr1[0])
#     n1 = len(matr1)
#     m2 = len(matr2[0])
#     n2 = len(matr2)
#     result = zero(n1, m2)
#
#     if m1 == n2:
#         for i in range(n1):
#             for j in range(m2):
#                 for k in range(m1):
#                     result[i][j] += matr1[i][k] * matr2[k][j]
#     return result

def vinograd(matr1, matr2):
    start = 0
    m1 = len(matr1[0])
    n1 = len(matr1)
    m2 = len(matr2[0])
    n2 = len(matr2)
    result = zero(n1, m2)
    h_vec = zero_vector(n1)
    v_vec = zero_vector(m2)
    if m1 == n2:
        for i in range(n1):
            for j in range(m1 // 2):
                h_vec[i] = h_vec[i] + matr1[i][j * 2] * matr1[i][j * 2 + 1]

        for i in range(m2):
            for j in range(n2 // 2):
                v_vec[i] = v_vec[i] + matr2[j * 2][i] * matr2[j * 2 + 1][i]
        start = time.clock()
        for i in range(n1):
            for j in range(m2):
                result[i][j] = -h_vec[i] - v_vec[j]
                for k in range(m1 // 2):
                    result[i][j] = result[i][j] + \
                    (matr1[i][2*k + 1] + matr2[2 * k][j]) * \
                                   (matr1[i][2 * k] + matr2[2 * k + 1][j])
        if m1 % 2:
            for i in range(n1):
                for j in range(m1):
                    result[i][j] = result[i][j] + matr1[i][m1 - 1] * matr2[m1 - 1][j]

    return result

def vinograd_opt(matr1, matr2):
    start = 0
    m1 = len(matr1[0])
    n1 = len(matr1)
    m2 = len(matr2[0])
    n2 = len(matr2)
    result = zero(n1, m2)
    h_vec = zero_vector(n1)
    v_vec = zero_vector(m2)
    if m1 == n2:
        m1_new = m1 % 2
        n2_new = n2 % 2
        for i in range(n1):
            for j in range(0,m1 - m1_new,2):
                h_vec[i] += matr1[i][j] * matr1[i][j + 1]

        for i in range(m2):
            for j in range(0,n2 - n2_new,2):
                v_vec[i] += matr2[j][i] * matr2[j + 1][i]

        start = time.clock()
        for i in range(n1):
            for j in range(m2):
                tmp = -h_vec[i] - v_vec[j]
                for k in range(0,m1 - m1_new,2):
                    tmp += (matr1[i][k + 1] + matr2[k][j]) * \
                                   (matr1[i][k] + matr2[k + 1][j])
                result[i][j] = tmp
        if m1_new:
            for i in range(n1):
                for j in range(m2):
                    result[i][j] += matr1[i][m1 - 1] * matr2[m1 - 1][j]

    return result, time.clock() - start

def vinograd_opt_parallel(matr1, matr2, threads_num):
    start = 0
    m1 = len(matr1[0])
    n1 = len(matr1)
    m2 = len(matr2[0])
    n2 = len(matr2)
    result = zero(n1, m2)
    h_vec = zero_vector(n1)
    v_vec = zero_vector(m2)
    if m1 == n2:
        m1_new = m1 % 2
        n2_new = n2 % 2
        for i in range(n1):
            for j in range(0,m1 - m1_new,2):
                h_vec[i] += matr1[i][j] * matr1[i][j + 1]

        for i in range(m2):
            for j in range(0,n2 - n2_new,2):
                v_vec[i] += matr2[j][i] * matr2[j + 1][i]

        start = time.clock()
        step = n1 // threads_num
        if step == 0:
            step = n1

        step1 = step
        threads = []

        for i in range(0, n1, step):
            if i + step > n1:
                step1 = n1 - i
            thread = threading.Thread(target=main_cycle, args=(result,matr1, matr2, h_vec, v_vec, i, i + step1, m1, m2, m1_new))
            threads.append(thread)
            thread.start()
            # main_cycle(result,matr1, matr2, h_vec, v_vec, i, i + step, m1, m2, m1_new)


        if m1_new:
            for i in range(n1):
                for j in range(m2):
                    result[i][j] += matr1[i][m1 - 1] * matr2[m1 - 1][j]

    return result, time.clock() - start

def main_cycle(result,matr1, matr2, h_vec, v_vec, n1_start, n1_end, m1, m2, m1_new):
    for i in range(n1_start, n1_end, 1):
        for j in range(m2):
            tmp = -h_vec[i] - v_vec[j]
            for k in range(0, m1 - m1_new, 2):
                tmp += (matr1[i][k + 1] + matr2[k][j]) * \
                       (matr1[i][k] + matr2[k + 1][j])
            result[i][j] = tmp

def print_matr(a):
    for i in range(len(a)):
        for j in range(len(a[0])):
            print(a[i][j], end = ' ')
        print('')



# a = zero(500,500, num = 50)
# b = zero(500,500, num = 50)
a = [
    [1,2,25,4,55],
    [2,2,3,6,5],
    [6,22,33,44,5],
]
b = [
[1,2,3,4,5,6],
[1,2,3,4,5,6],
[1,2,3,4,5,6],
[1,2,3,4,5,6],
[1,2,3,4,5,6],
]
print('Матрица А:')
print_matr(a)
print('Матрица B:')
print_matr(b)
print('Результат умножения оптимизированным методом Винограда:')
print_matr(vinograd_opt(a,b)[0])
print('Результат умножения многопоточным оптимизированным методом Винограда:')
print_matr(vinograd_opt_parallel(a,b, 1)[0])

