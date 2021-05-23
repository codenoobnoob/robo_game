import math

# for i in range(1, 11):
#     x = 1/5
#     print(math.sin(i*x))
easing_frames = 20

speed = 5

part = math.pi/10
easing_starts = 0
for i in range(1, 11):
    easing_starts += part*i*speed

print(math.sin(math.pi/2))
print(easing_starts)
