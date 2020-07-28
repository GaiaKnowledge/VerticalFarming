import numpy as np
from matplotlib import pyplot as plt

from .interval import Interval

class Pbox(object):

    def __init__(self, left=None, right=None, steps=200, shape=None, mean_left=None, mean_right=None, var_left=None, var_right=None, interpolation='linear'):

        if (left is not None) and (right is None):
            right = left

        if left is None and right is None:
            left = -np.inf
            right = np.inf

        if isinstance(left, Interval):
            left = np.array([left.left()])

        if isinstance(right, Interval):
            right = np.array([right.right()])

        if len(left) != steps:
            left = interpolate(left, interpolation=interpolation, left=False, steps=steps)

        if len(right) != steps:
            right = interpolate(right, interpolation=interpolation, left=True, steps=steps)

        self.left = left
        self.right = right

        self.steps = steps
        self.n = self.steps
        self.shape = shape
        self.mean_left = -np.inf
        self.mean_right = np.inf
        self.var_left = 0
        self.var_right = np.inf

        self._computemoments()
        if shape is not None: self.shape = shape
        if mean_left is not None: self.mean_left = np.max([mean_left, self.mean_left])
        if mean_right is not None: self.mean_right = np.min([mean_right, self.mean_right])
        if var_left is not None: self.var_left = np.max([var_left, self.var_left])
        if var_right is not None: self.var_right = np.min([var_right, self.var_right])
        self._checkmoments()

    def __repr__(self):
        if self.mean_left == self.mean_right:
            mean_text = f'{round(self.mean_left, 4)}'
        else:
            mean_text = f'[{round(self.mean_left, 4)}, {round(self.mean_right, 4)}]'

        if self.var_left == self.var_right:
            var_text = f'{round(self.var_left, 4)}'
        else:
            var_text = f'[{round(self.var_left, 4)}, {round(self.var_right, 4)}]'

        range_text = f'[{round(np.min([self.left, self.right]), 4), round(np.max([self.left, self.right]), 4)}'

        if self.shape is None:
            shape_text = ' '
        else:
            shape_text = f' {self.shape}' # space to start; see below lacking space

        return f'Pbox: ~{shape_text}(range={range_text}, mean={mean_text}, var={var_text})'

    def __iter__(self):
        for val in np.array([self.left,self.right]).flatten():
            yield val

    def __neg__(self):
        if self.shape in ['uniform','normal','cauchy','triangular','skew-normal']:
            s = self.shape
        else:
            s = ''

        return Pbox(
            left = -np.flip(self.right),
            right = -np.flip(self.left),
            shape = s,
            mean_left = -self.mean_right,
            mean_right = -self.mean_left,
            var_left = self.var_left,
            var_right = self.var_right
        )

    def __add__(self, other):

        return self.add(other, method = 'f')

    def __radd__(self,other):
        return self.add(other, method = 'f')

    def __sub__(self,other):

        return self.sub(other, method = 'f')

    def __rsub__(self,other):
        self = - self
        return self.add(other, method = 'f')

    def __mul__(self,other):
        return self.mul(other, method = 'f')

    def __rmul__(self,other):
        return self.mul(other, method = 'f')

    def __truediv__(self, other):

        return self.div(other, method = 'f')

    def __rtruediv__(self,other):

        try:
            return other * self.recip()
        except:
            return NotImplemented

    ### Local functions ###
    def _computemoments(self):    # should we compute mean if it is a Cauchy, var if it's a t distribution?
        self.mean_left = np.max([self.mean_left, np.mean(self.left)])
        self.mean_right = np.min([self.mean_right, np.mean(self.right)])

        if not (np.any(self.left <= -np.inf) or np.any(np.inf <= self.right)):
            V, JJ = 0, 0
            j = np.array(range(self.n))

            for J in np.array(range(self.n)) - 1:
                ud = [*self.left[j < J], *self.right[J <= j]]
                v = sideVariance(ud)

                if V < v:
                    JJ = J
                    V = v

            self.var_right = V

    def _checkmoments(self):

        a = Interval(self.mean_left, self.mean_right) #mean(x)
        b = dwMean(self)

        self.mean_left = np.max([left(a), left(b)])
        self.mean_right = np.min([right(a), right(b)])

        if self.mean_right < self.mean_left:
            # use the observed mean
            self.mean_left = left(b)
            self.mean_right = right(b)

        a = Interval(self.var_left, self.var_right) #var(x)
        b = dwVariance(self)

        self.var_left = np.max([left(a), left(b)])
        self.var_right = np.min([right(a),right(b)])

        if self.var_right < self.var_left:
            # use the observed variance
            self.var_left = left(b)
            self.var_right = right(b)

    ### Public funtions ###
    def add(self, other, method = 'f'):

        if method not in ['f','p','o','i']:
            raise ArithmeticError("Calculation method unkown")

        if other.__class__.__name__ == 'Interval':
            other = Pbox(other, steps = self.steps)

        if other.__class__.__name__ == 'Pbox':

            if self.steps != other.steps:
                raise ArithmeticError("Both Pboxes must have the same number of steps")

            if method == 'f':

                nleft  = np.empty(self.steps)
                nright = np.empty(self.steps)

                for i in range(0,self.steps):
                    j = np.array(range(i, self.steps))
                    k = np.array(range(self.steps - 1, i-1, -1))

                    nleft[i] = np.min(self.right[j] + other.right[k])

                    jj = np.array(range(0, i + 1))
                    kk = np.array(range(i, -1 , -1))

                    nright[i] = np.max(self.left[jj] + other.left[kk])

            elif method == 'p':

                nleft  = self.left + other.left
                nright = self.right + other.right

            elif method == 'o':

                nleft  = self.left + np.flip(other.left)
                nright = self.right + np.flip(other.right)

            elif method == 'i':

                nleft  = []
                nright = []
                for i in self.left:
                    for j in other.left:
                        nleft.append(i+j)
                for ii in self.right:
                    for jj in other.right:
                        nright.append(ii+jj)

            nleft.sort()
            nright.sort()

            return Pbox(
                left    = nleft,
                right   = nright,
                steps   = self.steps
            )

        else:
            try:
                # Try adding constant
                if self.shape in ['uniform','normal','cauchy','triangular','skew-normal']:
                    s = self.shape
                else:
                    s = ''

                return Pbox(
                    left       = self.left + other,
                    right      = self.right + other,
                    shape      = s,
                    mean_left  = self.mean_left + other,
                    mean_right = self.mean_right + other,
                    var_left   = self.var_left,
                    var_right  = self.var_right,
                    steps      = self.steps
                )

            except:
                return NotImplemented

    def sub(self, other, method = 'f'):

        if method == 'o':
            method = 'p'
        elif method == 'p':
            method = 'o'

        return self.add(-other, method)

    def mul(self, other, method = 'f'):

        if method not in ['f','p','o','i']:
            raise ArithmeticError("Calculation method unkown")

        if other.__class__.__name__ == 'Interval':
            other = Pbox(other, steps = self.steps)

        if other.__class__.__name__ == 'Pbox':

            if self.steps != other.steps:
                raise ArithmeticError("Both Pboxes must have the same number of steps")

            if method == 'f':

                nleft  = np.empty(self.steps)
                nright = np.empty(self.steps)

                for i in range(0,self.steps):
                    j = np.array(range(i, self.steps))
                    k = np.array(range(self.steps - 1, i-1, -1))

                    nleft[i] = np.min(self.right[j] * other.right[k])

                    jj = np.array(range(0, i + 1))
                    kk = np.array(range(i, -1 , -1))

                    nright[i] = np.max(self.left[jj] * other.left[kk])

            elif method == 'p':

                nleft  = self.left * other.left
                nright = self.right * other.right

            elif method == 'o':

                nleft  = self.left * np.flip(other.left)
                nright = self.right * np.flip(other.right)

            elif method == 'i':

                nleft  = []
                nright = []
                for i in self.left:
                    for j in other.left:
                        nleft.append(i*j)
                for ii in self.right:
                    for jj in other.right:
                        nright.append(ii*jj)

            nleft.sort()
            nright.sort()

            return Pbox(
                left    = nleft,
                right   = nright,
                steps   = self.steps
            )

        else:
            try:
                # Try adding constant
                if self.shape in ['uniform','normal','cauchy','triangular','skew-normal']:
                    s = self.shape
                else:
                    s = ''

                return Pbox(
                    left       = self.left * other,
                    right      = self.right * other,
                    shape      = s,
                    mean_left  = self.mean_left * other,
                    mean_right = self.mean_right * other,
                    var_left   = self.var_left,
                    var_right  = self.var_right,
                    steps      = self.steps
                )

            except:
                return NotImplemented

    def div(self, other, method = 'f'):

        if method == 'o':
            method = 'p'
        elif method == 'p':
            method = 'o'

        return self.mul(1/other, method)

    def recip(self):
        return Pbox(
            left  = 1 / np.flip(self.right),
            right = 1 / np.flip(self.left),
            steps = self.steps
        )

    def show(self,now = True,**kwargs):
        # If you want to know why numpy is the WORST thing about numpy
        # see this code snippet
        left, right = self.get_x()
        y  = self.get_y()


        plt.plot(left,y,**kwargs)
        plt.plot(right,y,**kwargs)
        if now:
            plt.show()
        else:
            return plt

    def get_interval(self, *args):

        if len(args) == 1:

            if args[0] == 1:
                # asking for whole pbox bounds
                return Interval(min(self.left),max(self.right))

            p1 = (1-args[0])/2
            p2 = 1-p1

        elif len(args) == 2:

            p1 = args[0]
            p2 = args[1]

        else:
            raise Exception('Too many inputs')

        y  = np.append(np.insert(np.linspace(0,1,self.steps),0,0),1)

        y1 = 0
        while y[y1] < p1:
            y1 += 1

        y2 = len(y)-1
        while y[y2] > p2:
            y2 -= 1

        x1 = self.left[y1]
        x2 = self.right[y2]
        return Interval(x1,x2)

    def get_probability(self, val):
        p  = np.append(np.insert(np.linspace(0,1,self.steps),0,0),1)

        i = 0
        while i < self.steps and self.left[i] < val:
            i += 1


        ub = p[i]

        j = 0

        while j < self.steps and self.right[j] < val:
            j += 1


        lb = p[j]

        return Interval(lb,ub)

    def support(self):
        return np.linspace(0,1,self.steps)

    def get_x(self):
        # returns the x values for plotting
        left = np.append(np.insert(self.left,0,min(self.left)),max(self.right))
        right = np.append(np.insert(self.right,0,min(self.left)),max(self.right))
        return left, right

    def get_y(self):
        # returns y values for plotting
        return np.append(np.insert(np.linspace(0,1,self.steps),0,0),1)
# Public functions

# Funcitons
def env_int(*args):
    left = min([min(i) if is_iterable(i) else i for i in args])
    right = max([max(i) if is_iterable(i) else i for i in args])
    return Interval(left, right)

def left(imp):
    if isinstance(imp, Interval) or isinstance(imp, pbox.Pbox):
        return imp.left()
    elif is_iterable(imp):
        return min(imp)
    else:
        return imp

def right(imp):
    if isinstance(imp, Interval) or isinstance(imp, pbox.Pbox):
        return imp.right()
    elif is_iterable(imp):
        return max(imp)
    else:
        return imp

def left_list(implist, verbose=False):
    if not is_iterable(implist):
        return np.array(implist)

    return np.array([left(imp) for imp in implist])

def right_list(implist, verbose=False):
    if not is_iterable(implist):
        return np.array(implist)

    return np.array([right(imp) for imp in implist])

def qleftquantiles(pp, x, p): # if first p is not zero, the left tail will be -Inf
    return [max(left_list(x)[right_list(p) <= P]) for P in pp]

def qrightquantiles(pp, x, p):  # if last p is not one, the right tail will be Inf
    return [min(right_list(x)[P <= left_list(p)]) for P in pp]

def quantiles(x, p, steps=200):
    left = qleftquantiles(ii(steps=steps), x, p)
    right = qrightquantiles(jj(steps=steps), x, p)
    return pbox.Pbox(left=left, right=right)  # quantiles are in x and the associated cumulative probabilities are in p

def interp_step(u, steps=200):
    u = np.sort(u)

    seq = np.linspace(start=0, stop=len(u) - 0.00001, num=steps, endpoint=True)
    seq = np.array([trunc(seq_val) for seq_val in seq])
    return u[seq]

def interp_cubicspline(vals, steps=200):
    vals = np.sort(vals) # sort
    vals_steps = np.array(range(len(vals))) + 1
    vals_steps = vals_steps / len(vals_steps)

    steps = np.array(range(steps)) + 1
    steps = steps / len(steps)

    interped = interp.CubicSpline(vals_steps, vals)
    return interped(steps)

def interp_left(u, steps=200):
    p = np.array(range(len(u))) / (len(u) - 1)
    pp, x = ii(steps=steps), u
    return qleftquantiles(pp, x, p)

def interp_right(d, steps=200):
    p = np.array(range(len(d))) / (len(d) - 1)
    pp, x = jj(steps=steps), d
    return qrightquantiles(pp, x, p)

def interp_outer(x, left, steps=200):
    if (left) :
        return interp_left(x, steps=steps)
    else:
        return interp_right(x, steps=steps)

def interp_linear(V, steps=200):
    m = len(V) - 1

    if m == 0: return np.repeat(V, steps)
    if steps == 1: return np.array([min(V), max(V)])

    d = 1 / m
    n = round(d * steps * 20)

    if n == 0:
        c = V
    else:
        c = []
        for i in range(m):
            v = V[i]
            w = V[i + 1]
            c.extend(np.linspace(start=v, stop=w, num=n))

    u = [c[round((len(c) - 1) * (k + 0) / (steps - 1))] for k in range(steps)]

    return np.array(u)

def interpolate(u, interpolation='linear', left=True, steps=200):
    if interpolation == 'outer':
        return interp_outer(u, left, steps=steps)
    elif interpolation == 'spline':
        return interp_cubicspline(u, steps=steps)
    elif interpolation == 'step':
        return interp_step(u, steps=steps)
    else:
        return interp_linear(u, steps=steps)

def sideVariance(w, mu=None):
    if not isinstance(w, np.ndarray): w = np.array(w)
    if mu is None: mu = np.mean(w)
    return max(0, np.mean((w - mu) ** 2))

def dwMean(pbox):
    return Interval(np.mean(pbox.right), np.mean(pbox.left))

def dwVariance(pbox):
    if np.any(np.isinf(pbox.left)) or np.any(np.isinf(pbox.right)):
        return Interval(0, np.inf)

    if np.all(pbox.right[0] == pbox.right) and np.all(pbox.left[0] == pbox.left):
        return Interval(0, (pbox.right[0] - pbox.left[0]) ** (2 / 4))

    vr = sideVariance(pbox.left, np.mean(pbox.left))
    w = np.copy(pbox.left)
    n = len(pbox.left)

    for i in reversed(range(n)):
        w[i] = pbox.right[i]
        v = sideVariance(w, np.mean(w))

        if np.isnan(vr) or np.isnan(v):
            vr = np.inf
        elif vr < v:
            vr = v

    if pbox.left[n - 1] <= pbox.right[0]:
        vl = 0.0
    else:
        x = pbox.right
        vl = sideVariance(w, np.mean(w))

        for i in reversed(range(n)):
            w[i] = pbox.left[i]
            here = w[i]

            if 1 < i:
                for j in reversed(range(i-1)):
                    if w[i] < w[j]:
                        w[j] = here

            v = sideVariance(w, np.mean(w))

            if np.isnan(vl) or np.isnan(v):
                vl = 0
            elif v < vl:
                vl = v

    return Interval(vl, vr)

def straddles(x):
    return (left(x) <= 0) and (0 <= right(x)) # includes zero

def straddlingzero(x):
    return (left(x) < 0) and (0 < right(x)) # neglects zero as an endpoint
