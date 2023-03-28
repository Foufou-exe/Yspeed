import sys

sys.path.append("..")

from yspeed import Yspeed

if __name__ == "__main__":
    ys = Yspeed()
    result = ys.run_speedtest()
    ys.display_results(result)
