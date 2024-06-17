from functools import reduce
import numpy as np

class Fuzzy:
    @staticmethod
    def complement(mf):
        ''' Applies fuzzy complement of the given mf '''
        return lambda x: 1 - mf(x)

    @staticmethod
    def intersection(*mfs):
        ''' Applies fuzzy intersection by applying the min function to all input mfs '''
        return lambda x: reduce(min, [mf(x) for mf in mfs])

    @staticmethod
    def union(*mfs):
        ''' Applies fuzzy union by applying the max function to all input mfs '''
        return lambda x: reduce(max, [mf(x) for mf in mfs])

    @staticmethod
    def mamdani(rules, startpos, endpos):
        ''' Aggregates rules then defuzzify by applying a Mamdani inference system. '''
        from mf import constmf
        rule_mfs = [Fuzzy.intersection(constmf(rule.antecedent), rule.consequent)
                    for rule in rules]

        xvals = np.arange(startpos, endpos+1, 0.01)
        yvals = np.vectorize(reduce(Fuzzy.union, rule_mfs), otypes=[float])(xvals)

        try:
            return np.sum(xvals * yvals)/np.sum(yvals)
        except ZeroDivisionError:
            return 0

    @staticmethod
    def sugeno(rules):
        ''' Aggregates rules then infer using Sugeno (or TSK) system '''
        num = sum(rule.antecedent * rule.consequent for rule in rules)
        den = sum(rule.antecedent for rule in rules)
        
        return 0 if den == 0 else num/den

class Rule:
    def __init__(self, antecedent, consequent):
        ''' Generates a rule for inference

        Keyword arguments:
        antecedent -- tuple of floats (odd elements) and Fuzzy set operations (even)
        consequent -- fuzzy membership function if Mamdani; crisp value if Sugeno
        '''
        self.antecedent = self.generate_antecedent(antecedent)
        self.consequent = consequent

    def generate_antecedent(self, antecedent):
        if not isinstance(antecedent, tuple):
            return antecedent
        elif len(antecedent) % 2 == 0:
            raise ValueError(f'Invalid antecedent!')
        
        const = antecedent[0]

        for function, value in zip(antecedent[1::2], antecedent[2::2]):
            const = function(const, value)

        return const
