import copy
import random
import threading


class Core:

    def color_picker(self, is_random, index, color_set):
        if is_random:
            selected_id = int(random.uniform(0, len(color_set)))
            selected = color_set[selected_id]
            del color_set[selected_id]
            return selected
        else:
            color_c = copy.deepcopy(color_set)
            color_r = color_c[index]
            del color_c[index]
            return color_r

    @staticmethod
    def print_d(is_debug, msgs):
        if is_debug:
            for msg in msgs:
                print(msg)

    @staticmethod
    def func_timeout(func, timeout=60):
        t = threading.Thread(target=func)
        t.setDaemon(True)
        t.start()
        t.join(timeout)
        print("Timeout")
