from math import pi
from subprocess import call

def triangular(center, width):
        def triangle(x, special_function = ''):
                r = width / 2.0
                k = 1.0 / r
                
                left = center - r
                right = center + r
                
                if special_function == '':
                        if left <= x <= center:
                                return k * (x - left) + 0
                        elif center <= x <= right:
                                return -k * (x - center) + 1
                        else:
                                return 0
                elif special_function == 'area':
                        if x >= 1:
                                x = 1

                        l = (1.0 - x) * width
                        return width / 2.0 - (1 - x) * l / 2.0
                elif special_function == 'center':
                        return center
                elif special_function == 'properties':
                        return "triangular center = " + str(center) + " width = " + str(width)

        return triangle

def trapezoidal_left(left, first, second):
        def trapezoid_left(x, special_function = 'none'):
                width = (second - first)
                k = 1.0 / width

                if special_function == 'none':
                        lleft = first - width
                        rright = first + width

                        if left <= x <= first:
                                return 1
                        elif first <= x <= rright:
                                return -k * (x - first) + 1
                        else:
                                return 0
                elif special_function == 'area':
                        if x >= 1:
                                x = 1

                        l = (1 - x) * (second - first)
                        
                        return  (first - left) * x + (second - first) / 2.0 - ( (1 - x) * l ) / 2.0
                elif special_function == 'center':
                        d_sq = width ** 2 + 1.0
                        a = first - left
                        b = second - left
                        c = 1

                        return left + b / 2.0 + (2 * a + b) * (1 - d_sq) / ( 6 * (b ** 2 - a ** 2) )
                elif special_function == 'properties':
                        return "trapezoidal_left left = " + str(left) + " first = " + str(first) + \
                                " second = " + str(second)

        return trapezoid_left

def trapezoidal_right(first, second, right):
        def trapezoid_right(x, special_function = 'none'):
                width = (second - first)
                k = 1.0 / width

                if special_function == 'none':
                        rright = first + width

                        if first <= x <= rright:
                                return k * (x - first) + 0
                        elif second <= x <= right:
                                return 1
                        else:
                                return 0
                elif special_function == 'area':
                        if x >= 1:
                                x = 1

                        l = (1 - x) * (second - first)
                        return  (right - second) * x + (second - first) / 2.0 - (1 - x) * l / 2.0
                elif special_function == 'center':
                        d_sq = width ** 2 + 1.0
                        a = right - second
                        b = right - first
                        c = 1

                        return first + b / 2.0 + (2 * a + b) * (1 - d_sq) / ( 6 * (b ** 2 - a ** 2) )
                elif special_function == 'properties':
                        return "trapezoidal_right first = " + str(first) + \
                                " second = " + str(second) + " right = " + str(right)

        return trapezoid_right

def trapezoidal(center, w1, w2):
        def trapezoid(x, special_function = 'none'):
                tr = trapezoidal_left(center, center + w1, center + w2)

                x = abs(x - center)

                if special_function == 'none':
                        return tr(center + x)
                elif special_function == 'area':
                        return 2 * tr(center + x, 'area')                       
                elif special_function == 'center':
                        return center
                elif special_function == 'properties':
                        return "trapezoidal center = " + str(center) + \
                                " w1 = " + str(w1) + " w2 = " + str(w2)

        return trapezoid

class FuzzyControl:
        def __init__(self):
                # map of list of labels (functions)
                self.inputs = {}
                self.outputs = {}
                self.rules = []

        def rule_set(self, rng, memberships):
                rs = {}
                for m in memberships:
                        name = m[-1]
                        if m[0] == 'triangle':
                                center = m[1]
                                width = m[2]
                                rs[name] = triangular(center, width)
                        elif m[0] == 'trapezoid_left':
                                x1 = m[1]
                                x2 = m[2]
                                rs[name] = trapezoidal_left(rng[0], x1, x2)
                        elif m[0] == 'trapezoid_right':
                                x1 = m[1]
                                x2 = m[2]
                                rs[name] = trapezoidal_right(x1, x2, rng[1])
                        elif m[0] == 'trapezoid':
                                center = m[1]
                                w1 = m[2]
                                w2 = m[3]
                                rs[name] = trapezoidal(center, w1, w2)
                return rs

        def add_input(self, name, rng, memberships):
                self.inputs[name] = self.rule_set(rng, memberships)
                #print 'params', name, rng, memberships

        def add_output(self, name, rng, memberships):
                self.outputs[name] = self.rule_set(rng, memberships)

        def add_rule(self, antecedents, conclusions):
                for c in conclusions:
                        self.rules.append( ( antecedents, (c, conclusions[c]) ) )

        def matching_degree(self, x, antecedents):
                dof = 1
                for i in x:
                        f = self.inputs[i][antecedents[i]]
                        #print '\t', f(0, 'properties'), "f(", x[i], ") = ", f(x[i])
                        dof *= f(x[i])
                
                return dof

        def output(self, inputs):
                outs = {}
                #print 'INPTS', self.inputs
                for output in self.outputs:
                        total_sum = 0.0
                        total_area = 0.0
                        for r in self.rules:
                                antecedents = r[0]
                                conclusion = r[1]

                                if conclusion[0] != output:
                                        continue

                                dof = self.matching_degree(inputs, antecedents)
                                #print r, dof

                                f = self.outputs[ conclusion[0] ][ conclusion[1] ]
                                area = f(dof, 'area')

                                total_sum += f(dof, 'center') * area
                                total_area += area

                        if total_area != 0:
                            outs[output] = 1.0 * total_sum / total_area
                        else:
                            outs[output] = -1024

                return outs

from inspect import ismethod

class Test:
        def should_eq(self, name, val1, val2):
                BEGIN_PASS = '\033[92m'
                BEGIN_FAIL = '\033[91m'
                END = '\033[0m'

                if val1 == val2:
                        print(
                                "\t{ " + name + " }" + BEGIN_PASS + " pass --> " + 
                                str(val1) + " = " + str(val2) + END
                        )
                else:
                        print(
                                "\t{ " + name + "}" + BEGIN_FAIL + " fail --> " + 
                                str(val1) + " != " + str(val2) + END
                        )

        def main(self):
                call(["clear"])

                print("")
                print("")
                print("")

                for name in dir(self):
                        attribute = getattr(self, name)
                        if ismethod(attribute) and attribute.__name__.startswith('test'):
                                print(attribute.__name__)
                                attribute()

                print("")
                print("")
                print("")

        def test_triangular(self):
                f = triangular(2, 3)

                self.should_eq("leftmost t(2,3) at (0.5)", f(0.5), 0)
                self.should_eq("middle t(2,3) at (2)", f(2), 1)
                self.should_eq("right middle t(2,3) at(2.75)", f(2.75), 0.5)
                self.should_eq("right middle t(2,3) at (3)", round(f(3), 2), 0.33)
                self.should_eq("rightmost t(2,3) at (3.5)", f(3.5), 0)
                for i in [4, 5, 6]:
                        self.should_eq("right outer t(2,3) = (" + str(i) + ")", f(i), 0)
                for i in [-1, -0.5, 0]:
                        self.should_eq("left outer t(2,3) = (" + str(i) + ")", f(i), 0)

                self.should_eq("area cut t(2,3) x = 1", f(1, 'area'), 1.5)
                self.should_eq("area cut t(2,3) x = 0.5", f(0.5, 'area'), (3.0 / 4.0) * 1.5)
                self.should_eq("area cut t(2,3) x = 0.5", f(0.25, 'area'), 0.65625)
                self.should_eq("area cut t(2,3) x = 0.5", f(0.75, 'area'), 1.40625)

                self.should_eq("center t(2,3)", f(0, 'center'), 2)

        def test_trapezoidal_left(self):
                f = trapezoidal_left(2, 3.5, 4.5)

                self.should_eq("leftmost tr_l(2, 3.5, 4.5) at (2)", f(2), 1)
                self.should_eq("middle left tr_l(2, 3.5, 4.5) at (3)", f(3), 1)
                self.should_eq("middle left tr_l(2, 3.5, 4.5) at (3.25)", f(3.25), 1)

                self.should_eq("triangle left tr_l(2, 3.5, 4.5) at (3.5)", f(3.5), 1)
                self.should_eq("triangle middle tr_l(2, 3.5, 4.5) at (4)", f(4), 0.5)
                self.should_eq("triangle right tr_l(2, 3.5, 4.5) at (4.5)", f(4.5), 0)

                for i in [-1, 0, 1]:
                        self.should_eq("leftmost out of tr_l(2, 3.5, 4.5) at (" + str(i) + ")", f(i), 0)

                for i in [4.75, 5, 6]:
                        self.should_eq("rightmost out of tr_l(2, 3.5, 4.5) at (" + str(i) + ")", f(i), 0)

                self.should_eq("area cut tr_l(2, 3.5, 4.5) x = 1", f(1, 'area'), 2)
                self.should_eq("area cut tr_l(2, 3.5, 4.5) x = 0.5", f(0.5, 'area'), 1.125)
                
                area = round(f(0.25, 'area'), 3)
                should_area = round(1.5 * 0.25 + 0.5 - (0.75 ** 2) / 2.0, 3)
                self.should_eq("area cut x = 0.25", area, should_area)
                
                area = round(f(0.75, 'area'), 3)
                should_area = round( 1.5 * 0.75 + 0.5 - (0.25 ** 2) / 2.0 , 3 )
                self.should_eq("area cut tr_l(2, 3.5, 4.5) x = 0.75", area, should_area)

                self.should_eq("center tr_l(2, 3.5, 4.5)", round(f(0, 'center'), 0), 3)


        def test_trapezoidal_right(self):
                f = trapezoidal_right(2, 3.5, 4.5)

                self.should_eq("triangle leftmost tr_r(2, 3.5, 4.5) at (2)", f(2), 0)
                self.should_eq("triangle middle left tr_r(2, 3.5, 4.5) at (3)", f(2.75), 0.5)
                self.should_eq("triangle middle left tr_r(2, 3.5, 4.5) at (3.25)", f(3.5), 1)

                self.should_eq("left tr_r(2, 3.5, 4.5) at (3.5)", f(3.5), 1)
                self.should_eq("middle tr_r(2, 3.5, 4.5) at (4)", f(4), 1)
                self.should_eq("right tr_r(2, 3.5, 4.5) at (4.5)", f(4.5), 1)

                for i in [-1, 0, 1]:
                        self.should_eq("leftmost out of tr_r(2, 3.5, 4.5) at (" + str(i) + ")", f(i), 0)

                for i in [4.75, 5, 6]:
                        self.should_eq("rightmost out of tr_r(2, 3.5, 4.5) at (" + str(i) + ")", f(i), 0)

                self.should_eq("area cut tr_r(2, 3.5, 4.5) x = 1", f(1, 'area'), 1.75)
                
                area = round(f(0.5, 'area'), 3)
                should_area = round(1 * 0.5 + 0.75 - 1.5 *(0.5 ** 2) / 2.0, 3)
                self.should_eq("area cut tr_r(2, 3.5, 4.5) x = 0.5", area, should_area)
                
                area = round(f(0.75, 'area'), 3)
                should_area = round(1 * 0.75 + 0.75 - 1.5 *(0.25 ** 2) / 2.0, 3)
                self.should_eq("area cut tr_r(2, 3.5, 4.5) x = 0.75", area, should_area)
                
                area = round(f(0.25, 'area'), 3)
                should_area = round(1 * 0.25 + 0.75 - 1.5 *(0.75 ** 2) / 2.0, 3)
                self.should_eq("area cut tr_r(2, 3.5, 4.5) x = 0.75", area, should_area)

                self.should_eq("center tr_r(2, 3.5, 4.5)", round(f(0, 'center'), 0), 3)

        def test_inference_zjuric_example(self):
                controller = FuzzyControl()

                visina_memberships = [
                        ['trapezoid_left', 140, 150, 'VN'],
                        ['trapezoid', 155, 5, 15, 'N'],
                        ['trapezoid', 175, 5, 15, 'OV'],
                        ['trapezoid', 195, 5, 15, 'V'],
                        ['trapezoid_right', 200, 210, 'VN'],
                ]
                controller.add_input('VISINA', (120, 220), visina_memberships)

                masa_memberships = [
                        ['trapezoid_left', 55, 60, 'VM'],
                        ['trapezoid', 62.5, 2.5, 7.5, 'M'],
                        ['trapezoid', 75, 2.5, 7.5, 'PT'],
                        ['trapezoid', 87.5, 2.5, 7.5, 'D'],
                        ['trapezoid_right', 90, 95, 'VD'],
                ]
                controller.add_input('MASA', (0, 100), masa_memberships)

                indeks_zdravlja_membersips = [
                        ['triangle', 20, 20, 'SN'],
                        ['triangle', 40, 20, 'PN'],
                        ['triangle', 60, 20, 'PZ'],
                        ['triangle', 80, 20, 'SZ']
                ]
                controller.add_output('INDEKS_ZDRAVLJA', (0, 100), indeks_zdravlja_membersips)

                controller.add_rule({'VISINA' : 'OV', 'MASA' : 'VM'}, {'INDEKS_ZDRAVLJA' : 'PN'})
                controller.add_rule({'VISINA' : 'OV', 'MASA' : 'M'}, {'INDEKS_ZDRAVLJA' : 'SZ'})
                controller.add_rule({'VISINA' : 'V', 'MASA' : 'VM'}, {'INDEKS_ZDRAVLJA' : 'SN'})
                controller.add_rule({'VISINA' : 'V', 'MASA' : 'M'}, {'INDEKS_ZDRAVLJA' : 'PZ'})

                output = controller.output( { 'VISINA' : 183, 'MASA' : 56 } )['INDEKS_ZDRAVLJA']
                self.should_eq("inference output at (183, 56)", round(output, 0), 43)


def test():
        test_suite = Test()
        test_suite.main()
