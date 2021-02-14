"""Helper functions to test solving a small QUBO using a direct enumeration method (brute force)."""


def enumeration_function(q_matrix):
    # print("This is the test Q matrix: ", q_matrix)
    n = len(q_matrix[0])
    energy_list = []
    for k in range(0, 2**n):
        bin_k = int2bin(k, n)
        w = []
        for m in range(0, n):
            w.append(int(bin_k[m]))
        # Starting adding terms to the objective function here.
        running_total = 0
        for m in range(0, n):
            running_total = running_total + w[m]*q_matrix[m][m]
        for m in range(1, n):
            for j in range(0, m):
                running_total = running_total + w[j]*w[m]*q_matrix[j][m]
        # Done loading objective function.
        energy_list.append([running_total, w])

    sorted_energy_list = sorted(energy_list, key=lambda output: output[0])

    # This returns the y value which minimizes the objective function, e.g. [1, 0, 1, 0, ...]
    return sorted_energy_list[0][1]


def int2bin(nn, m):
    """returns the binary of integer nn, using N number of digits"""
    return "".join([str((nn >> j) & 1) for j in range(m - 1, -1, -1)])
