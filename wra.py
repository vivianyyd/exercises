def parse():
    """Parses a matrix formatted with only spaces and newlines; converts to Wolfram-Alpha compatible format."""
    matrix = '{'
    print("Input a matrix:")
    while True:
        line = input()
        if len(line) == 0:
            break
        matrix += '{' + ','.join(x for x in line.split(' ') if len(x) != 0) + '},'
    matrix = matrix[0:-1] + '}'
    print(matrix)


parse()
