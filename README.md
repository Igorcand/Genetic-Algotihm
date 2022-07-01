# Genetic-Algotihm
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/Igorcand/Genetic-Algotihm/blob/master/LICENSE) 

# About the Project
GENETIC ALGOTIHM is a IA project used biologic expressions like Generations, Population, Mutation, Crossover, Chromossome, etc. 
The project idea is: Exist a truck and we have to put products inside there, but have some informations, each product have got a value and a volumn and the truck have delimited volumn, so we have to choice the better solution to maximize the value inside the truck without extrapolate the volume.

# How the project works
Como a ideia é maximizar o lucro dentro de um valor de volume fixo, a ideia é que, partindo do aleatorio, o algoritmo ache a melhor solução dentro do volume possivel. 

No codigo temos 3 classes principais que são utilizadas, os Produtos, os Individuos e o Algoritmo Genetico. 
A classe dos produtos atribui ao objeto de classe os valores do produto que são importate para o codigo, como o nome, valor e volume ocupado.

A classe dos Indiviuduos gera uma combinação, inicialmente aleatoria, de quais produtos irão estar no caminhão e quais não irão, definindo o que chamamos de Cromossomo. Então cada individuo tem um cromossomo unico e consiste entre valores de 0 e 1, e cada numero é um gene, uma parte menor do cromossomo. O gene 0 indica que o produto especifico naquele indice não estará no caminhão e o gene 1 indica que o produto estará no caminhão. Esta classes tem funções importantes dentro ela que são Fitness, Crossover e Mutação. 
Função Fitness: gera uma nota para cada individuo avaliando o seu cromossomo. A avaliação é feita percorrendo o cromossomo e identificando onde existe o numero 1, que indica que este produto estará no caminhão. Ao somar todo os valores e volumes, se o volume dos produtos for maior que o volome permitido no caminhão, este individuo tem um cromossomo ruim, logo não é bom para o decorrer do código, então a função atribui uma nota baixa de 1. Se ao percorrer o cromossomo, a soma dos volumes estiver dentro do permitido, este é um cromossomo possivel, então a nota desse individuo é igual a soma dos valores de cada produto.

Função Crossover: Está função é responsável por fazer o cruzamento de dois individuos e gerar dois individuos diferentes. A ideia é selecionar dois pais para que tenham seus cromossomos disponiveis para fazer o cruzamento e gerar dois filhos parecidos porem diferente. O cruzamento é feito a partir de um valor gerado aleatoriamente, em que é selecionado um indice do cromossomo para partir os dois cromossomos dos individuos no mesmo indice, gerando então 4 partes de cromossomo. Depois disso é feito a função da primeira parte do individuo 1 com a segunda do individuo 2 e a primeira parte do indivudo 2 com a segunda parte do indivudo 1. Feito isso, foi gerado dois filhos semelhantes aos pais, sendo que os pais selecionados provavelmente eram possíveis, pois ja haviam feito a avaliação de cada individuo.

Função Mutação: O objetivo desse método, é deixar o algoritmo ainda mais parecido com uma evolução biologica, podendo então existir mutações nos individuos, sem que haja uma ordem ou frequencia. A mutação é feita percorrendo o cromossomo, e em cada gene do cromossomo existe o número 0 ou 1, indicando se o produto não está ou está no caminhãp. O que o código faz é gerar um numero aleatório entre 0 e 1 e sempre verificar se é menor que a taxa de mutação padrão que foi defenida, se o numero sorteado for menor então irá acontecer a mutação, e a mutação consiste em alterar se o produto estará ou não no caminhão, alterando o 0 para 1 ou o 1 para 0.


A classe do Algotimo Genetico é a principal, que controla as outras duas anteriores, precisando apenas chamar o a função resolver de  dentro desta classe juntamente com os parametros que a classe ja irá acionar as outras.


O código então irá rodar a quantidade de vezes que foi definida na variavél GERAÇÔES, fazendo repetidas vezes o processo de: avaliar os indivudos gerando sua nota, ordenar os individuos da melhor nota para a pior, selecionar os pais utilizando o método de roleta viciada, fazer o crossover dos pais selecinados até criar uma nova população.

Feito isso, no final das gerações, o código tenderá a estar melhor que no começo, mas não necessariamente, a ultima geração será a melhor e nem o melhor individuo estará na ultima geração. Poderá ter existido o melhor individuo em alguma geração intermediaria, mas o código sempre salvará o melhor individuos de todos até aparecer outro melhor.

OBS: Quanto mais produtos existirem, maior será o cromossomo e mais demorado será para achar o resultado, então quanto maior a lista de produtos disponiveis maior terá que ser o numero de gerações.

# Variáveis Globais
limite = É o volume limite do caminhão, em metros cubicos (m3)
numero de gerações = É quantas vezes o loop será rodado
tamanho_população = É quantos cromossomos diferentes existirá em cada geração
taxa_mutação = É a probabilidade de acontecer uma mutação no cromossomo

# Technology used

## Back end
- Python

# How run this project

```bash
# clone this repository
git clone https://github.com/Igorcand/Genetic-Algotihm.git

# Enter the folder 
Genetic-Algotihm

# Edit the global variables

# Execute the file 
algoritmo_genetico.py 
```


# Author

Igor Cândido Rodrigues

https://www.linkedin.com/in/igorc%C3%A2ndido/
