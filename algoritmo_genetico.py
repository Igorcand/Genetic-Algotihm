from random import random 

#A classe profuto vai instanciar as variáveis dos produtos, que são nome, espaço ocupado em m3 e o valor em reais
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor 
    
class Individuo():
    def __init__(self, espaco, valores, limite_espaco, geracao=0):
        #estaço é o volume ocupado no momento
        self.espaco = espaco
        #valor é R$
        self.valores = valores
        #qual o limite de volume, no exemplo, não pode passar de 3 m3
        self.limite_espaco = limite_espaco
        #Cada individuo tem uma nota, se é bom ou não
        self.nota_avaliacao = 0
        #Espaço usado é para gerar a avaliação
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = []

        #Inicialização aleatória do cromossomo com 14 genes(total de produtos)
        for i in range(len(espaco)):
            if random() < 0.5:
                self.cromossomo.append('0')
            else:
                self.cromossomo.append('1')

    #fitness - medida de qualidade do cromossomo e se o cromossoom tem uma boa avaliação para saber se pode ser usado como referencia para as próximas gerações
    def avaliacao(self):
        nota = 0
        soma_espacos = 0 
        #Ao percorrer o cromossomo, faço uma validação de acordo com o cromossomo, para saber qual o espaço usado e qual a nota(valor de carga)
        #[0, 1, ,1 ,1, 0, 0, 1]
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espaco[i]
        #Se o espaço usado no momento for maior que o espaço total, o individuo não serve para o problema, então vamos rebaixar ele
        if soma_espacos > self.limite_espaco:
            nota = 1 
        self.nota_avaliacao = nota 
        self.espaco_usado = soma_espacos 
    
    #crossover é a reprodução, onde será juntado dois genes
    def crossover(self, outro_individuo):
        #random vai retornar um valor entre 0 e 1
        #multipplicar pelo tamanho do cromossomo e aredondar para achar o ponto de corte do cromossomo
        corte = round(random() * len(self.cromossomo))
        #[0, 0, 0, |1, 1, 1, 0, 1, 0]    = [0, 0, 0, 1, 1, 1, 0, 1, 0]
        #[0, 1, 0, |1, 1, 1, 0, 1, 0]    = [0, 1, 0, 1, 1, 1, 0, 1, 0]

        #[0, 0, 0, |0, 1, 1, 0, 0, 1]
        #[0, 0, 1, |1, 1, 1, 0, 1, 0]

        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]


        filhos = [Individuo(self.espaco, self.valores, self.limite_espaco, self.geracao +1), Individuo(self.espaco, self.valores, self.limite_espaco, self.geracao +1) ]

        #Inicializando o cromossomo apos a reprodução, que no caso é a interação dos dois cromossomos acima
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2

        return filhos 

    #A mutação 
    def mutacao(self, taxa_mutacao):
        #Ao percorrer os cromossomos, a cada indice criamos uma possivel chance de haver uma mutação, no qual, aleatoriamente o cromossomo vai mudar
        #se NONE
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        
        return self


#Essa classe que vai comandar o algoritmo
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        #quantos individuos vamos usar
        self.tamanho_populacao = tamanho_populacao
        #Quais os são individuos
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.soma_roleta = 0
    
    #cria a quantidade de indiviuos de acordo com parametro
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            #espaços e valores são iguais para todos, apenas o cromossomo que é diferente porque é aleatorio
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        #A melhor solucao é o primeiro indivio
        self.melhor_solucao = self.populacao[0]

    #Apenas para ordenar de acordo com melhor nota
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key= lambda populacao: populacao.nota_avaliacao,reverse=True)

    #O melhor indivio será o primeiro da lista porque foi ordenado 
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
    
    #Apens somar a nota de todos os individuos da populacao para ver a melhora dela no decorrer das gerações
    def soma_avaliacao(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        self.soma_roleta = soma
        return soma

    #Essa função vai selecionar dois pais para fazer a reprodução e gerar um individuo melhor
    def seleciona_pai(self, soma_avaliacao):
        #print(f'SELECIONA PAI INICIADO')
        #soma avaliação é a oma das avaliações de todos os indiviuos da população
        #método da roleta viciada
        # c = 0
        # for i in self.populacao:
        #     print(f'indiviuo {i.nota_avaliacao} - indice {c}')
        #     c+= 1
        #print(f'soma_avaliacao = {soma_avaliacao}')
        #a variavel pai indica qual o indice do melhor pai na lista de população
        pai = -1
        #valor sorteado será um valor randomico
        valor_sorteado = random() * soma_avaliacao # 60000
        #print(f'valor_sorteado = {valor_sorteado}')
        soma = 0 #13000/ 34000 / 51000
        i = 0
        #enquanto o indice for menor que o tamaho da população e a soma menor que o valor sorteado
        #Teoricamente, vamos rodando a roleta até ela parar
        while i < len(self.populacao) and soma < valor_sorteado:
            # 0 - valor 13000
            # 1 - valor 21000
            # 2 - valor 1
            # 3 - valor 1
            # 4 - valor 17000
            # 1 - 6000

            #ruim = 40000


            #[1 - 30000, 2 - 27000, 3-25000, 4-20000, 5-15000, 6 - 10000]
            #pai1 - 3
            #print(f'individuo = {self.populacao[i].nota_avaliacao}  --- soma = {soma}')
            soma += self.populacao[i].nota_avaliacao
            pai  += 1
            i += 1
        #print(f'pai escolhido foi o {pai}')
        #print(f'finalizou')
        return pai

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print(f'Geracao = {self.populacao[0].geracao} - soma roleta = {round(self.soma_roleta, 1)} - melhor geração  = {round(melhor.nota_avaliacao, 1)}')
        #print(f'Valor = {melhor.nota_avaliacao}')
        #print(f'Espaco = {melhor.espaco}')
        #print(f'Cromossomo = {melhor.cromossomo}')


    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espaco):
        #inicia a populacao com as variaveis dos items
        self.inicializa_populacao(espacos, valores, limite_espaco)

        #gera uma avaliação individual para cada individuo de acordo com o desempenho
        for individuo in self.populacao:
            individuo.avaliacao()
        
        #ordena
        self.ordena_populacao()

        self.visualiza_geracao()

        #Fazendo um loop pelo total de gerações
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacao()
            nova_populacao = []
            # selecionar dois pais para fazer o crossover a partir da roleta, fazendo um loop de 10 vezes, pois depois do crossover ele gera dois filhos cada
            for _ in range(0, self.tamanho_populacao, 2):
                #retorna os indices dos pais
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)

                #Novos individuos na lista
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                #adiciona os 2 novos individuos na nova população
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            #Passa a nova população, com 20 individuos  possivelmente melhores como novo parametro, para sobrescrever a antiga
            self.populacao = list(nova_populacao)
            for individuo in self.populacao:
                individuo.avaliacao()
            
            #ordena novamente
            self.ordena_populacao()

            self.visualiza_geracao()
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
        print(f'''Melhor solucao 
             G = {self.melhor_solucao.geracao}
             Valor = {self.melhor_solucao.nota_avaliacao}
             Espaco = {self.melhor_solucao.espaco}
             Cromossomo = {self.melhor_solucao.cromossomo}
            ''')
        return self.melhor_solucao.cromossomo

        









if __name__ == '__main__':
    lista_produtos = []
    lista_produtos.append(Produto('Geladeira Dako', 0.751, 999.90))
    lista_produtos.append(Produto('Iphone 6', 0.0000899, 2911.12))
    lista_produtos.append(Produto('TV 55', 0.400, 4346.99))
    lista_produtos.append(Produto('TV 50', 0.290, 3999.90))
    lista_produtos.append(Produto('TV 42', 0.200, 2999.00))
    lista_produtos.append(Produto('Notebook Dell', 0.00350, 2499.00))
    lista_produtos.append(Produto('Ventilador Panasonic', 0.496, 199.90))
    lista_produtos.append(Produto('Microondas Eletrolux', 0.0424, 308.66))
    lista_produtos.append(Produto('Microondas LG', 0.0544, 429.90))
    lista_produtos.append(Produto('Microondas Panasonic', 0.0319, 299.29))
    lista_produtos.append(Produto('Geladeira Brastemp', 0.635, 849.00))
    lista_produtos.append(Produto('Geladeira Consul', 0.870, 1199.89))
    lista_produtos.append(Produto('Notebook Lenovo', 0.498, 1999.90))
    lista_produtos.append(Produto('Notebook Asus', 0.527, 3999.00))

    lista_produtos.append(Produto('Geladeira Frost', 0.721, 2999.90))
    lista_produtos.append(Produto('Apple Watch 6', 0.0000899, 1111.12))
    lista_produtos.append(Produto('TV 85', 0.650, 6346.99))
    lista_produtos.append(Produto('TV 70', 0.590, 5999.90))
    lista_produtos.append(Produto('TV 60', 0.510, 4999.00))
    lista_produtos.append(Produto('Notebook Apple', 0.0350, 10499.00))
    lista_produtos.append(Produto('Refrigerador Novo Mundo', 0.696, 3199.90))
    lista_produtos.append(Produto('Iphone X ', 0.000424, 4508.66))
    lista_produtos.append(Produto('Tablet Sansung LG', 0.0544, 1429.90))
    lista_produtos.append(Produto('Sofá 3 lugares', 0.5909, 5099.29))
    lista_produtos.append(Produto('Sofá Retrátil', 0.335, 849.00))
    lista_produtos.append(Produto('Geladeira Magazine', 0.870, 2199.89))
    lista_produtos.append(Produto('Refrigerador Brastemp', 0.792, 5209.90))
    lista_produtos.append(Produto('Sofá Mobly', 0.927, 8959.00))

    lista_produtos.append(Produto('Geladeira Frost 2', 0.7671, 2349.90))
    lista_produtos.append(Produto('Apple Watch 6 2', 0.0003499, 1123.12))
    lista_produtos.append(Produto('TV 88 2', 0.689, 6346.99))
    lista_produtos.append(Produto('TV 75 2', 0.2350, 5369.90))
    lista_produtos.append(Produto('TV 62 2', 0.230, 3499.00))
    lista_produtos.append(Produto('Notebook Apple 2.0', 0.3650, 8959.00))
    lista_produtos.append(Produto('Refrigerador Novo Mundo 2.0', 0.4326, 987.90))
    lista_produtos.append(Produto('Iphone XR', 0.05424, 4218.66))
    lista_produtos.append(Produto('Tablet Sansung Tab A', 0.564, 3229.90))
    lista_produtos.append(Produto('Sofá 6 lugares ', 0.98509, 4599.29))
    lista_produtos.append(Produto('Sofá Retrátil 2.0', 0.6575, 8939.00))
    lista_produtos.append(Produto('Geladeira Magazine Turbo', 0.4900, 4599.89))
    lista_produtos.append(Produto('Refrigerador Brastemp Master', 0.892, 2309.90))
    lista_produtos.append(Produto('Rolex', 0.0007, 30000.00))


    espacos = []
    valores = []
    nomes = []

    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)

    limite = 5
    numero_geracoes = 150
    taxa_mutacao = 0.01
    tamanho_populacao = 20

    #inicializa o algoritmo passando o tamanho da população
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao,numero_geracoes, espacos, valores, limite)
    print(resultado)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print(f'Nome = {lista_produtos[i].nome}, Espaco = {lista_produtos[i].espaco}, Valor = {lista_produtos[i].valor}')



    
