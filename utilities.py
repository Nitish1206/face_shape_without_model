import math
def rect_to_bb(rect):

    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w,h)

def distance(point1,point2,l):
    if l==0:
        return abs(point1[0]-point2[0])

    elif l==1:
        return abs(point1[1]-point2[1])

    elif l==2:
        return math.sqrt((distance(point1,point2,0)**2)+(distance(point1,point2,1)**2))

def ratio(distance1,distance2):
    return distance1/distance2


def subtract(distance1,distance2):
    return abs(distance1-distance2)


def angle(slope):
    return (math.degrees(math.atan(slope)))


def slope(point1,point2):
    return (abs(point2[1] - point1[1])) / abs((point2[0]- point1[0]))


def points(lower_limit,upper_limit, shape):
    point_list=[]
    for value in range(lower_limit,upper_limit):
        point_list.append(list(shape[value]))
    return point_list


def standard_dev(list):
    mean=sum(list)/len(list)
    sq_diff_list = []
    for value in list:
        val = (value-mean)**2
        sq_diff_list.append(val)

    varinace=sum(sq_diff_list)/(len(sq_diff_list))
    std_dev=math.sqrt(varinace)
    return std_dev

