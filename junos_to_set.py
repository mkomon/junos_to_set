#!/usr/bin/env python3

'''
Convert JunOS configuration from curly-brackets style to set-form. Handles
inactive directives, skips comments starting with hash mark (#).

'''

class Stack(object):
    def __init__(self):
        self.data = []
    def push(self, element, is_inactive=False):
        self.data.append(element)
    def pop(self):
        if not len(self.data):
            raise Exception("Stack is empty, can't pop!")
        last = self.data[-1]
        self.data = self.data[:-1]
        return last
    def __str__(self):
        return ' '.join([i[0] for i in self.data])

def main():
    import sys
    if len(sys.argv) != 2:
        print("Invalid arguments! Usage: %s <input filename>" % sys.argv[0])
        sys.exit(1)
    input_filename = sys.argv[1]
    stack = Stack()
    with open(input_filename, 'r') as f:
        for line in f:
            line = ''.join([x for x in line if x not in ['\r', '\n']]).strip()
            if line.startswith('#'):
                print(line)
                continue
            is_inactive = True if line.startswith('inactive') else False
            if is_inactive:
                line = line[10:]
            if line.endswith('{'):
                stack.push((line[:-2], is_inactive))
            if line.endswith(';'):
                print('set', str(stack), line[:-1])
                if is_inactive:
                    print('deactivate', str(stack), line[:-1])
            if line.endswith('}'):
                line, is_inactive = stack.pop()
                if is_inactive:
                    print('deactivate', str(stack), line)

if __name__ == '__main__':
    main()