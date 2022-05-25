def is_within_inclusive(min, max, val):
    return val >= min and val <= max

def is_within_range_inclusive(range, val):
    return  range == None or is_within_inclusive(range[0], range[1], val)


def merge_stock(stock1, stock2, remove_zero=True):
    new_stock = stock1.copy()
    for i, i1 in enumerate(stock1):
        for i2 in stock2:
            if i1[0] == i2[0]:
                new_stock.pop(i)
                new_stock.insert(i, (i1[0], i1[1]+i2[1]))
                break
    new_stock += [c for c in stock2 if c[0] not in [p[0] for p in new_stock]]
    if remove_zero:
        new_stock = [c for c in new_stock if c[1] != 0]
    return new_stock

def cancel_stock(stock1, stock2, remove_zero=True):
    new_stock = stock1.copy()
    for i, i1 in enumerate(stock1):
        for i2 in stock2:
            if i1[0] == i2[0]:
                new_stock.pop(i)
                new_stock.insert(i, (i1[0], i1[1]-i2[1]))
                break
    new_stock += [(c[0], -c[1]) for c in stock2 if c[0] not in [p[0] for p in new_stock]]
    if remove_zero:
        new_stock = [c for c in new_stock if c[1] != 0]
    return new_stock

def is_contain_stock(main_stock, minor_stock):
    stock = main_stock.copy()
    for i1 in minor_stock:
        has_found = False
        for i, i2 in enumerate(main_stock):
            if i1[0] == i2[0]:
                if i1[1] <= i2[1]:
                    stock.pop(i)
                    stock.insert(i, (i1[0],i2[1]-i1[1]))
                    has_found = True
                    break
                else:
                    return False
        if not has_found:
            return False
    return True
                
def concat_type_string(types, division_string=" OR "):
    s = ""
    for t in types:
        s += t.__name__ + division_string
    return s[:-len(division_string)]

if __name__ == "__main__":
    print(concat_type_string((int, str)))
