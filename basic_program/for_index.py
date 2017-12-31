lines=['a', 'b', 'c']
for line, index in zip(lines, range(len(lines))):
    print "%s value with indes %d" % (line, index)