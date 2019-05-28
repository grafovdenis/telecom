import numpy as np

K = 4


def encode(num):
    # Return given 4 bits plus parity bits for bits (0,2,3), (0,1,2) and (0,1,2)
    b0 = parity(num, [0, 2, 3])
    b1 = parity(num, [0, 1, 3])
    b2 = parity(num, [0, 1, 2])

    return [b0, b1, num[3], b2, num[2], num[1], num[0]]  # again saying, works only for 7,4


def parity(s, indexes):
    return int(s[indexes[0]]) ^ int(s[indexes[1]]) ^ int(s[indexes[2]])


def get_syndrome_num(num):
    s0 = syndrome(num, [0, 2, 4, 6])
    s1 = syndrome(num, [1, 2, 5, 6])
    s2 = syndrome(num, [3, 4, 5, 6])
    result = s0 + s1 * 2 + s2 * 4
    return result


def syndrome(num, indexes):
    return int(num[indexes[0]]) ^ int(num[indexes[1]]) ^ int(num[indexes[2]] ^ int(num[indexes[3]]))


# recover encoded message with error in (syndrome) digit
def recover(num, syndrome):
    if syndrome == 0:
        return num
    result = num
    result[syndrome] = 0 if result[syndrome] == 1 else 1
    return result


def transform(matrix):
    return np.matrix([matrix.item(2), matrix.item(4), matrix.item(5), matrix.item(6),
                      matrix.item(0), matrix.item(1), matrix.item(3)])


if __name__ == "__main__":
    print("  Source | Encoded")
    for i in range(0, 16):
        rand = np.random.randint(2, size=4)
        print(rand, encode(rand))
    print("\n")

    num = np.array([1, 0, 1, 1])
    encoded = encode(num)
    print("Syndrome for correct message:", get_syndrome_num(encoded))
    print("Syndrome example for:", num)
    print(encoded)
    print("Let error be in 6 digit:")
    encoded[6] = 0 if encoded[6] == 1 else 1
    print(encoded)
    print("Error in", get_syndrome_num(encoded) - 1, "digit")
    print("Recovered message:")
    print(recover(encoded, get_syndrome_num(encoded) - 1))
    print("\n\n")

    print("Generator matrix example:")
    num_matrix = np.matrix([[0, 1, 0, 1]])
    print(num_matrix)

    gm = np.matrix([[1, 0, 0, 0, 1, 1, 0],
                    [0, 1, 0, 0, 1, 0, 1],
                    [0, 0, 1, 0, 0, 1, 1],
                    [0, 0, 0, 1, 1, 1, 1]])

    encoded_matrix = num_matrix * gm

    encoded_matrix = encoded_matrix.transpose()

    for i in range(encoded_matrix.__len__()):
        encoded_matrix[i] = encoded_matrix[i] % 2

    encoded_matrix = encoded_matrix.transpose()
    print("Encoded matrix:", encoded_matrix)

    damaged = np.matrix([[0, 1, 0, 1, 0, 1, 1]])

    print("Damaged matrix:", damaged)

    b = np.matrix([[0, 1, 1],
                   [1, 0, 1],
                   [1, 1, 0],
                   [1, 1, 1],
                   [0, 0, 1],
                   [0, 1, 0],
                   [1, 0, 0]]
                  )

    encoded_error = np.flip(encoded_matrix * b)
    damaged_error = np.flip(damaged * b)

    # transform indexes from [2 4 5 6 0 1 3] to [0 1 2 3 4 5 6]
    result = transform(encoded_matrix)
    damaged_result = transform(damaged)

    print("Result matrix :", result)
    print("Damaged result:", damaged)

    for i in range(damaged_error.__len__()):
        damaged_error[i] = damaged_error[i] % 2

    for i in range(encoded_error.__len__()):
        encoded_error[i] = encoded_error[i] % 2

    dmg_err = damaged_error.item(2) * 4 + damaged_error.item(1) * 2 + damaged_error.item(0)
    enc_err = encoded_error.item(2) * 4 + encoded_error.item(1) * 2 + encoded_error.item(0)

    print("Syndrome of correct message:", enc_err)
    print("Syndrome of damaged message:", dmg_err, "(means that mistake is in 3rd digit)")
