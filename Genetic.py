class Genetic(object):

    def __init__(self, f, pop_size = 100, n_variables = 2):
        self.f = f
        self.minim = -100
        self.maxim = 100
        self.pop_size = pop_size
        self.n_variables = n_variables
        self.population = self.initializePopulation()
        self.evaluatePopulation()

    def initializePopulation(self):
        return [np.random.randint(self.minim, self.maxim, size=(self.n_variables)) 
                           for i in range(self.pop_size)]

    def evaluatePopulation(self):
        return [self.f(i[0], i[1]) for i in self.population]
        #return [(i[0]-4)**2 + i[1]**2 for i in self.population]

    def nextGen(self):
        results = self.evaluatePopulation()
        print(results)
        children = [self.population[np.argmin(results)]] #list of minimum element
        print(children)

        while len(children) < self.pop_size:
            # Tournament selection
            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)
            if results[randA] < results[randB]:
                p1 = self.population[randA]
            else: 
                p1 = self.population[randB]

            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)  
            if results[randA] < results[randB]: 
                p2 = self.population[randA]
            else: p2 = self.population[randB]   

            signs = []
            for i in zip(p1, p2):
                if i[0] < 0 and i[1] < 0: signs.append(-1)
                elif i[0] >= 0 and i[1] >= 0: signs.append(1)
                else: signs.append(np.random.choice([-1,1]))

            # Convert values to binary
            p1 = [format(abs(i), '010b') for i in p1]
            p2 = [format(abs(i), '010b') for i in p2]

            # Recombination
            child = []
            for i, j in zip(p1, p2):
                for k, l in zip(i, j):
                    if k == l: 
                        child.append(k) #append common Gen
                    else: 
                        child.append(str(np.random.randint(min(k, l),max(k,l))))

                    

            child = ''.join(child)
            g1 = child[0:len(child)//2] 
            g2 = child[len(child)//2:len(child)]
            children.append(np.asarray([signs[0]*int(g1, 2), 
                                        signs[1]*int(g2, 2)]))
        self.population = children

    def run(self):
        x1 = -1000
        x2 = 1000
        while x1 < x2:
            x1 += 1
            self.nextGen()
        return self.population[0]
import numpy as np
import math
f = lambda x, y: -0.0001 * math.pow(math.fabs(math.sin(x) * math.sin(y) * (math.exp(math.fabs(100 - math.sqrt((x*x + y*y))/math.pi)))) + 1,0.1)
gen = Genetic(f)
minim = gen.run()
print("############################################")
print('Minimum of function      X =', minim[0], ', Y =', minim[1],'    #')
print("############################################")