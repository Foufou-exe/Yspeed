import sys

sys.path.append("..")

from yspeed import Yspeed

ys = Yspeed()
result = ys.get_speedtest()
print(result)
