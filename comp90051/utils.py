"""
utilities
"""

import matplotlib.pyplot as plt

class stack:
    def __init__(self):
        self.list=[]

    def push(self,item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list)==0

class queue:
    def __init__(self):
        self.list=[]

    def push(self,item):
        self.list.insert(0,item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list)==0

    
def plot_results(X_train, Y_train, X_test, Y_test, score_fn, threshold = 0):
    # Plot training set
    plt.plot(X_train[Y_train==-1,0], X_train[Y_train==-1,1], "o", label="Y=-1, train")
    plt.plot(X_train[Y_train==1,0], X_train[Y_train==1,1], "o", label="Y=1, train")
    plt.gca().set_prop_cycle(None) # reset colour cycle

    # Plot test set
    plt.plot(X_test[Y_test==-1,0], X_test[Y_test==-1,1], "x", label="Y=-1, test")
    plt.plot(X_test[Y_test==1,0], X_test[Y_test==1,1], "x", label="Y=1, test")

    # Compute axes limits
    border = 1
    x0_lower = X_train[:,0].min() - border
    x0_upper = X_train[:,0].max() + border
    x1_lower = X_train[:,1].min() - border
    x1_upper = X_train[:,1].max() + border

    # Generate grid over feature space
    resolution = 0.01
    x0, x1 = np.mgrid[x0_lower:x0_upper:resolution, x1_lower:x1_upper:resolution]
    grid = np.c_[x0.ravel(), x1.ravel()]
    s = score_fn(grid).reshape(x0.shape)

    # Plot decision boundary (where s(x) == 0)
    plt.contour(x0, x1, s, levels=[0], cmap="Greys", vmin=-0.2, vmax=0.2)

    plt.legend()
    plt.xlabel("$x_0$")
    plt.ylabel("$x_1$")
    plt.show()
    
