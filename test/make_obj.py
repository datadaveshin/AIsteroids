

obj = {}
def make_obj(state, action, state_prime):
    sa = state + action
    if sa in obj:
        if state_prime in obj[sa]:
            obj[sa][state_prime] += 1
        else:
            obj[sa][state_prime] = 1
    else:
        obj[sa] = {}
        obj[sa][state_prime] = 1


print obj
make_obj('sq1', 'mv1', 'sq2')
print obj
make_obj('sq1', 'mv1', 'sq2')
print obj
make_obj('sq1', 'mv1', 'sq2')
print obj

print obj
make_obj('sq1', 'mv2', 'sq2')
print obj
make_obj('sq1', 'mv2', 'sq2')
print obj
make_obj('sq1', 'mv2', 'sq2')
print obj


print obj
make_obj('sq1', 'mv2', 'sq2')
print obj
make_obj('sq1', 'mv2', 'sq2')
print obj
make_obj('sq1', 'mv2', 'sq2')
print obj

print obj
make_obj('sq2', 'mv2', 'sq1')
print obj
make_obj('sq2', 'mv2', 'sq2')
print obj
make_obj('sq2', 'mv2', 'sq4')
print obj
