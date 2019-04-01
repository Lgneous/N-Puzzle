def parse(f):
    state = 
    for raw_line in f:
        line = raw_line.split('#')[0].strip()
        if not line:
            continue
        
