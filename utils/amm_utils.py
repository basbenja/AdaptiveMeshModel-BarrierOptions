def trend(r, sigma):
    return r - (sigma**2)/2

def p_u(h, k, r, sigma):
    a = (sigma**2 * (k/h**2)) / 2
    b = trend(r, sigma)**2 * (k**2/h**2)
    c = trend(r, sigma) * k/h
    return a + b + c

def p_d(h, k, r, sigma):
    a = (sigma**2 * (k/h**2)) / 2
    b = trend(r, sigma)**2 * (k**2/h**2)
    c = trend(r, sigma) * k/h
    return a + b - c

def p_m(h, k, r, sigma):
    return 1 - p_u(h, k, r, sigma) - p_d(h, k, r, sigma)