import string

# Variable Initialization (extracted from the file)
a, b, c, d = 11, 38, 60, 23
e, f, g, h = 41, 26, 51, 13
i, j, k, l = 22, 45, 25, 50
m, n, o, p = 37, 28, 59, 6

# Limited to Printable ASCII Range (32–126)
all_ascii_chars = [chr(i) for i in range(32, 127)]


def to_unsigned_8bit(val):
    return val & 0xFF


def bitwise_not_8bit(val):
    return to_unsigned_8bit(~val)


def check_condition(char, pos):
    ch = ord(char)
    if pos == 0:
        return (ch - 113) & 0xFF == (a & b)
    elif pos == 1:
        return (ch - 36) & 0xFF == (c | d)
    elif pos == 2:
        return (ch - 30) & 0xFF == 2 * e
    elif pos == 3:
        return (ch - 5) & 0xFF == (g ^ h)
    elif pos == 4:
        return (ch - 21) & 0xFF == (i | j)
    elif pos == 5:
        return (ch - 54) & 0xFF == (k & l)
    elif pos == 6:
        return (ch - 49) & 0xFF == 2 * m
    elif pos == 7:
        return (ch - 56) & 0xFF == (o | p)
    elif pos == 8:
        return (ch - 44) & 0xFF == (e & f)
    elif pos == 9:
        return (ch - 64) & 0xFF == (bitwise_not_8bit(h) & g)
    elif pos == 10:
        return (ch - 50) & 0xFF == (i ^ j)
    elif pos == 11:
        return (ch - 37) & 0xFF == (k >> 1)
    elif pos == 12:
        return (ch - 53) & 0xFF == (m ^ n)
    elif pos == 13:
        return (ch - 101) & 0xFF == (o & p)
    elif pos == 14:
        return (ch - 132) & 0xFF == (bitwise_not_8bit(b) | a)
    elif pos == 15:
        return (ch - 45) & 0xFF == (bitwise_not_8bit(d) & c)
    elif pos == 16:
        return (ch - 21) & 0xFF == (e | f)
    elif pos == 17:
        return (ch - 90) & 0xFF == 2 * h
    elif pos == 18:
        return (ch - 101) & 0xFF == (i & j)
    elif pos == 19:
        return (ch - 59) & 0xFF == (c ^ i)
    elif pos == 20:
        return (ch - 152) & 0xFF == (bitwise_not_8bit(o) | m)
    elif pos == 21:
        return (ch - 47) & 0xFF == (p ^ n)
    else:
        return False


def find_flag_char(pos):
    for char in all_ascii_chars:
        if check_condition(char, pos):
            return char
    return None


def brute_force_flag():
    flag = []
    for pos in range(22):
        char = find_flag_char(pos)
        if char:
            flag.append(char)
        else:
            print(f"조건을 만족하는 문자를 찾지 못했습니다: 위치 {pos}")
            return None

    return "".join(flag)


# Find the dynamic part of the flag
dynamic_flag = brute_force_flag()

if dynamic_flag:
    # Ensure the flag ends correctly
    if dynamic_flag.endswith('}I'):
        dynamic_flag = dynamic_flag[:-1]
    # Print the full flag
    print("찾은 플래그:", dynamic_flag)
else:
    print("플래그를 찾는 데 실패했습니다.")
