def parse_file(filename: str = 'input.txt'):
    lines = []
    with open(filename) as fp:
        line = fp.readline()
        while line:
            if line:
                lines.append(line.strip())
            line = fp.readline()
    return lines
