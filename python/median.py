#! /usr/bin/python


def median(lists):
    med = 0
    lists = sorted(lists)
    print lists

    if len(lists)%2==0:
        med = ( lists[len(lists)/2 - 1] + lists[len(lists)/2] ) / 2 
    else:
        med = lists[(len(lists)-1)/2]
    return med

lost = [1,2,3,4,5]

print median(lost)
