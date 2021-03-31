from figures import Circle

a=Circle(2)
b=Circle(3)
for square in a,b:
    print(f'square = {square.get_area_circle()}')