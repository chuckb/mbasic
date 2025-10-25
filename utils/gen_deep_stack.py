#!/usr/bin/env python3
"""Generate deep GOSUB stack test"""

def generate_test(depth, filename):
    lines = []
    lines.append(f'10 PRINT "GOSUB Stack Test - {depth} levels"')
    lines.append('20 GOSUB 1000')
    lines.append('30 PRINT "A: Back to main - SUCCESS"')
    lines.append('40 END')

    for i in range(depth):
        base = 1000 + i * 1000
        next_base = base + 1000
        label = chr(ord('B') + i)

        lines.append(f'{base} PRINT "{label}: In {base}"')
        if i < depth - 1:
            lines.append(f'{base+10} GOSUB {next_base}')
            lines.append(f'{base+20} PRINT "{label}2: Back in {base}"')
        lines.append(f'{base+30} RETURN')

    program = '\n'.join(lines) + '\n'

    # Write with CRLF
    with open(filename, 'wb') as f:
        f.write(program.replace('\n', '\r\n').encode('ascii'))

if __name__ == '__main__':
    generate_test(20, 'tests/stk20.bas')
    generate_test(30, 'tests/stk30.bas')
    generate_test(40, 'tests/stk40.bas')
    generate_test(50, 'tests/stk50.bas')
    print("Generated stack tests: stk20.bas, stk30.bas, stk40.bas, stk50.bas")
