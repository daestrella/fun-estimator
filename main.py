from mf import trimf
from graph import Graph
from fuzzy import Rule, Fuzzy
import argument
import numpy as np

DOMAIN = (-10, 10)
RANGE = (-2, 2)

arg = argument.parse()

exact = arg['function']
DX = arg['dx']

basis = np.array([[x, exact(x)] for x in np.arange(-100, 100)])
estimate = lambda x: Fuzzy.sugeno(
        [Rule((trimf(antecedent-DX, antecedent, antecedent+DX)(x)), consequent)
         for antecedent, consequent in basis])

error = lambda x: exact(x) - estimate(x)

graph = Graph(figsize=(8, 6), x_domain=DOMAIN, y_range=RANGE,
              title='Function estimator using Sugeno inferencing',
              xlabel=r'$x$', ylabel=r'$y$', x_max=100)

graph.plot(label=fr'$f(x) = {arg['LaTeX']}$', y=exact)
graph.plot(label=fr'$g(x) \approx {arg['LaTeX']}$ [Sugeno]', y=estimate)
graph.plot(label=r'$e(x) = f(x) - g(x)', y=error)

graph.show_graph()
