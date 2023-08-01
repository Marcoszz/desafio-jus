# Desafio Jusbrasil

O teste baseia-se na construção de uma API que retorne os dados de um processo (em todos os graus) regido pelo TJAL ou TJCE. 

Para mais informações visite [aqui](https://docs.google.com/document/d/12TesK4PrzUR9HGt30bY7npx9fTKHo0JIQEjRpPO6hWU/edit?usp=sharing)

## Setup

Antes de começar, verifique se você atendeu aos seguintes requisitos:

* Você possui docker/docker compose instalado na sua máquina. (Em caso negativo, visite [aqui](https://docs.docker.com/engine/install/)
* Você possui interpretadores de Makefile (se for ubuntu já vem por padrão)
* **PS: É altamente recomendado rodar em um OS Linux com distribuição Ubuntu**

## Instalando

Para instalar siga estas etapas:

- Clone o projeto na sua máquina (```git clone```)
- ```make build``` (Cria a network de conversacão entre os serviços rodados)

## Usando

Para usar siga estas etapas:

- ```make up``` (Sobe os serviços)
- Copie a URL onde serviço flask está sendo rodado (está settado para rodar no localhost:8000)
- Exapanda a seção de processo no swagger
- Faça testes sobre a rota /processo (já deixei um processo válido como exemplo)

## Testando

Para testar a aplicação:

- Com a aplicação rodando, execute ```make up```
