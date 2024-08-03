# raiseEx.py
def area(radius):
    if radius < 0:
        raise RuntimeError("negative radius")
    else:
        return 3.14*radius*radius

print(area(-2))
