class Node(object):
    idx = 0
    def __init__(self):
        # Node Number
        self.idx = 1
        self.priority = 1

        # Execution Time
        self.d_exec_t = 0
        self.c_exec_t = 0
        self.period = 100 # ms

        # Graph Info
        self.parent = []
        self.child = []
        self.isSink = False
        self.isSource = False
        self.level = 0