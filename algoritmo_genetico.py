from random import random 

#A classe profuto vai instanciar as variáveis dos produtos, que são nome, espaço ocupado em m3 e o valor em reais
class Product():
    def __init__(self, name, space, value):
        self.name = name
        self.space = space
        self.value = value 
    
class Individual():
    def __init__(self, space, value, space_limit, generation=0):
        #estaço é o volume ocupado no momento
        self.space = space
        #valor é R$
        self.value = value
        #qual o limite de volume, no exemplo, não pode passar de 3 m3
        self.space_limit = space_limit
        #Cada individuo tem uma nota, se é bom ou não
        self.note_avaliation = 0
        #Espaço usado é para gerar a avaliação
        self.space_used = 0
        self.generation = generation
        self.chromossome = []

        #Inicialização aleatória do cromossomo com 14 genes(total de produtos)
        for i in range(len(space)):
            if random() < 0.5:
                self.chromossome.append('0')
            else:
                self.chromossome.append('1')

    #fitness - medida de qualidade do cromossomo e se o cromossoom tem uma boa avaliação para saber se pode ser usado como referencia para as próximas gerações
    def fitness(self):
        note = 0
        sum_spaces = 0 
        #Ao percorrer o cromossomo, faço uma validação de acordo com o cromossomo, para saber qual o espaço usado e qual a nota(valor de carga)
        #[0, 1, ,1 ,1, 0, 0, 1]
        for i in range(len(self.chromossome)):
            if self.chromossome[i] == '1':
                note += self.value[i]
                sum_spaces += self.space[i]
        #Se o espaço usado no momento for maior que o espaço total, o individuo não serve para o problema, então vamos rebaixar ele
        if sum_spaces > self.space_limit:
            note = 1 
        self.note_avaliation = note
        self.space_used = sum_spaces 
    
    #crossover é a reprodução, onde será juntado dois genes
    def crossover(self, other_individual):
        #random vai retornar um valor entre 0 e 1
        #multipplicar pelo tamanho do cromossomo e aredondar para achar o ponto de corte do cromossomo
        cut = round(random() * len(self.chromossome))

        son1 = other_individual.chromossome[0:cut] + self.chromossome[cut::]
        son2 = self.chromossome[0:cut] + other_individual.chromossome[cut::]

        sons = [Individual(self.space, self.value, self.space_limit, self.generation +1), Individual(self.space, self.value, self.space_limit, self.generation +1) ]

        #Inicializando o cromossomo apos a reprodução, que no caso é a interação dos dois cromossomos acima
        sons[0].chromossome = son1
        sons[1].chromossome = son2

        return sons 

    #A mutação 
    def mutation(self, mutation_rate):
        #Ao percorrer os cromossomos, a cada indice criamos uma possivel chance de haver uma mutação, no qual, aleatoriamente o cromossomo vai mudar
        
        for i in range(len(self.chromossome)):
            if random() < mutation_rate:
                if self.chromossome[i] == '1':
                    self.chromossome[i] = '0'
                else:
                    self.chromossome[i] = '1'
        
        return self


#Essa classe que vai comandar o algoritmo
class AlgoritmoGenetico():
    def __init__(self, size_population):
        #quantos individuos vamos usar
        self.size_population = size_population
        #Quais os são individuos
        self.population = []
        self.generation= 0
        self.best_solution = 0
        self.sum_roulette = 0
    
    #cria a quantidade de indiviuos de acordo com parametro
    def inicialize_population(self, spaces, values, space_limit):
        for i in range(self.size_population):
            #espaços e valores são iguais para todos, apenas o cromossomo que é diferente porque é aleatorio
            self.population.append(Individual(spaces, values, space_limit))
        #A melhor solucao é o primeiro indivio
        self.best_solution = self.population[0]

    #Apenas para ordenar de acordo com melhor nota
    def order_population(self):
        self.population = sorted(self.population, key= lambda population: population.note_avaliation,reverse=True)

    #O melhor indivio será o primeiro da lista porque foi ordenado 
    def better_individual(self, individual):
        if individual.note_avaliation > self.best_solution.note_avaliation:
            self.best_solution = individual
    
    #Apens somar a nota de todos os individuos da populacao para ver a melhora dela no decorrer das gerações
    def sum_avaliation(self):
        sum = 0
        for individual in self.population:
            sum += individual.note_avaliation
        self.sum_roulette = sum
        return sum

    #Essa função vai selecionar dois pais para fazer a reprodução e gerar um individuo melhor
    def seleciona_pai(self, sum_avaliation):
        #soma avaliação é a oma das avaliações de todos os indiviuos da população
        #método da roleta viciada
        #a variavel pai indica qual o indice do melhor pai na lista de população
        dad = -1
        #valor sorteado será um valor randomico
        value_drawn = random() * sum_avaliation 
        sum = 0 
        i = 0
        #enquanto o indice for menor que o tamaho da população e a soma menor que o valor sorteado
        #Teoricamente, vamos rodando a roleta até ela parar
        while i < len(self.population) and sum < value_drawn:
            sum += self.population[i].note_avaliation
            dad  += 1
            i += 1
        return dad

    def show_generation(self):
        better = self.population[0]
        print('--------')
        print(f'Generation = {self.population[0].generation}')
        print(f'Value = {better.note_avaliation}')
        print(f'Chromossome = {better.chromossome}')
        print('--------')


    def run(self, mutation_rate, generations, spaces, values, space_limit):
        #inicia a populacao com as variaveis dos items
        self.inicialize_population(spaces, values, space_limit)

        #gera uma avaliação individual para cada individuo de acordo com o desempenho
        for individual in self.population:
            individual.fitness()
        
        #ordena
        self.order_population()

        self.show_generation()

        #Fazendo um loop pelo total de gerações
        for generation in range(generations):
            sum_avaliation = self.sum_avaliation()
            new_population = []
            # selecionar dois pais para fazer o crossover a partir da roleta, fazendo um loop de 10 vezes, pois depois do crossover ele gera dois filhos cada
            for _ in range(0, self.size_population, 2):
                #retorna os indices dos pais
                dad1 = self.seleciona_pai(sum_avaliation)
                dad2 = self.seleciona_pai(sum_avaliation)

                #Novos individuos na lista
                sons = self.population[dad1].crossover(self.population[dad2])

                #adiciona os 2 novos individuos na nova população
                new_population.append(sons[0].mutation(mutation_rate))
                new_population.append(sons[1].mutation(mutation_rate))

            #Passa a nova população, com 20 individuos  possivelmente melhores como novo parametro, para sobrescrever a antiga
            self.population = list(new_population)
            for individual in self.population:
                individual.fitness()
            
            #ordena novamente
            self.order_population()

            self.show_generation()
            better = self.population[0]
            self.better_individual(better)
        print(f'''Best Solution 
             G = {self.best_solution.generation}
             Value = {self.best_solution.note_avaliation}
             Space = {self.best_solution.space}
             Chromossome = {self.best_solution.chromossome}
            ''')
        return self.best_solution.chromossome

        









if __name__ == '__main__':
    product_list = []
    product_list.append(Product('Geladeira Dako', 0.751, 999.90))
    product_list.append(Product('Iphone 6', 0.0000899, 2911.12))
    product_list.append(Product('TV 55', 0.400, 4346.99))
    product_list.append(Product('TV 50', 0.290, 3999.90))
    product_list.append(Product('TV 42', 0.200, 2999.00))
    product_list.append(Product('Notebook Dell', 0.00350, 2499.00))
    product_list.append(Product('Ventilador Panasonic', 0.496, 199.90))
    product_list.append(Product('Microondas Eletrolux', 0.0424, 308.66))
    product_list.append(Product('Microondas LG', 0.0544, 429.90))
    product_list.append(Product('Microondas Panasonic', 0.0319, 299.29))
    product_list.append(Product('Geladeira Brastemp', 0.635, 849.00))
    product_list.append(Product('Geladeira Consul', 0.870, 1199.89))
    product_list.append(Product('Notebook Lenovo', 0.498, 1999.90))
    product_list.append(Product('Notebook Asus', 0.527, 3999.00))
    product_list.append(Product('Geladeira Frost', 0.721, 2999.90))
    product_list.append(Product('Apple Watch 6', 0.0000899, 1111.12))
    product_list.append(Product('TV 85', 0.650, 6346.99))
    product_list.append(Product('TV 70', 0.590, 5999.90))
    product_list.append(Product('TV 60', 0.510, 4999.00))
    product_list.append(Product('Notebook Apple', 0.0350, 10499.00))
    product_list.append(Product('Refrigerador Novo Mundo', 0.696, 3199.90))
    product_list.append(Product('Iphone X ', 0.000424, 4508.66))
    product_list.append(Product('Tablet Sansung LG', 0.0544, 1429.90))
    product_list.append(Product('Sofá 3 lugares', 0.5909, 5099.29))
    product_list.append(Product('Sofá Retrátil', 0.335, 849.00))
    product_list.append(Product('Geladeira Magazine', 0.870, 2199.89))
    product_list.append(Product('Refrigerador Brastemp', 0.792, 5209.90))
    product_list.append(Product('Sofá Mobly', 0.927, 8959.00))
    product_list.append(Product('Geladeira Frost 2', 0.7671, 2349.90))
    product_list.append(Product('Apple Watch 6 2', 0.0003499, 1123.12))
    product_list.append(Product('TV 88 2', 0.689, 6346.99))
    product_list.append(Product('TV 75 2', 0.2350, 5369.90))
    product_list.append(Product('TV 62 2', 0.230, 3499.00))
    product_list.append(Product('Notebook Apple 2.0', 0.3650, 8959.00))
    product_list.append(Product('Refrigerador Novo Mundo 2.0', 0.4326, 987.90))
    product_list.append(Product('Iphone XR', 0.05424, 4218.66))
    product_list.append(Product('Tablet Sansung Tab A', 0.564, 3229.90))
    product_list.append(Product('Sofá 6 lugares ', 0.98509, 4599.29))
    product_list.append(Product('Sofá Retrátil 2.0', 0.6575, 8939.00))
    product_list.append(Product('Geladeira Magazine Turbo', 0.4900, 4599.89))
    product_list.append(Product('Refrigerador Brastemp Master', 0.892, 2309.90))
    product_list.append(Product('Rolex', 0.0007, 30000.00))


    spaces = []
    values = []
    names = []

    for product in product_list:
        spaces.append(product.space)
        values.append(product.value)
        names.append(product.name)

    limit = 5
    generations = 150
    mutation_rate = 0.01
    size_population = 20

    #inicializa o algoritmo passando o tamanho da população
    ag = AlgoritmoGenetico(size_population)
    result = ag.run(mutation_rate,generations, spaces, values, limit)

    for i in range(len(product_list)):
        if result[i] == '1':
            print(f'Nome = {product_list[i].name}, Espaco = {product_list[i].space}, Valor = {product_list[i].value}')



    
