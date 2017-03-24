key = list(input('Enter the key:\n').upper().replace(' ', '').replace('J', 'I'))
msg = input('Enter the message:\n').upper().replace(' ', '')
j_indices = [i for i, x in enumerate(msg) if x == 'J']  # used for decryption
msg = list(msg.replace('J', 'I'))

ab = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
table = [[0 for c in range(5)] for r in range(5)]
msg_digrams = []
x1 = []  # Have indices of all the first letters in the message digrams
x2 = []  # Have indices of all the second letters in the message digrams
result = []


def create_table():
    t = key + ab
    for i in range(len(t) - 1):  # Remove repeated letters
        j = i + 1
        while j < len(t):
            if t[i] == t[j]:
                del t[j]
            else:
                j += 1
    # Convert the table to 5x5 2D grid
    for i in range(5):
        for j in range(5):
            table[i][j] = t[j + i * 5]

    return table


def prepare_message():
    global msg
    for i in range(len(msg) - 1):  # add X if duplicate letters after each other
        if msg[i] == msg[i + 1]:
            msg.insert(i + 1, 'X')

    if len(msg) % 2 == 1:  # padding if odd numbers
        msg += 'X'

    i = 0
    while i < len(msg):
        msg_digrams.append(msg[i:i + 2])
        i += 2

    return msg_digrams


def get_indices():
    # Get indices of the the digrams
    for x in range(len(msg_digrams)):
        for y in range(len(msg_digrams[0])):
            for i in range(5):
                j = get_index(msg_digrams[x][y], i)
                if j != -1:
                    if y == 0:
                        x1.append(i)
                        x1.append(j)
                        break
                    if y == 1:
                        x2.append(i)
                        x2.append(j)
                        break


def get_index(value, row):
    try:
        return table[row].index(value)
    except ValueError:
        return -1


def encrypt():
    # Start Encryption
    idx = 0
    for i in range(int(len(x1) / 2)):
        if x1[idx] == x2[idx]:  # Two letters are in the same row
            # Letter 1
            if x1[idx + 1] == len(table) - 1:  # wrap if it was on the end of the row
                result.append(table[x1[idx]][0])
            else:
                result.append(table[x1[idx]][x1[idx + 1] + 1])

            # Letter 2
            if x2[idx + 1] == len(table) - 1:  # wrap if it was on the end of the row
                result.append(table[x2[idx]][0])
            else:
                result.append(table[x2[idx]][x2[idx + 1] + 1])

        elif x1[idx + 1] == x2[idx + 1]:  # Two letters are in the same column
            # Letter 1
            if x1[idx] == len(table) - 1:  # wrap if it was on the end of the column
                result.append(table[0][x1[idx + 1]])
            else:
                result.append(table[x1[idx] + 1][x1[idx + 1]])

            # Letter 2
            if x2[idx] == len(table) - 1:  # wrap if it was on the end of the column
                result.append(table[0][x2[idx + 1]])
            else:
                result.append(table[x2[idx] + 1][x2[idx + 1]])

        else:  # Two letters are not on the same row or column (rectangle)
            result.append(table[x1[idx]][x2[idx + 1]])  # Letter 1
            result.append(table[x2[idx]][x1[idx + 1]])  # Letter 2
        idx += 2

    return ''.join(result)

if __name__ == '__main__':
    create_table()
    prepare_message()
    get_indices()
    res = encrypt()
    i = 0
    while i < len(res):
        print(res[i: i + 2], end=' ')
        i += 2
