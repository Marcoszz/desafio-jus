# Desafio Jusbrasil

O teste resume-se na construção de uma API que retorne os dados de um processo (em todos os graus) regido pelo TJAL ou TJCE. 

Para mais informações visite [aqui](https://docs.google.com/document/d/12TesK4PrzUR9HGt30bY7npx9fTKHo0JIQEjRpPO6hWU/edit?usp=sharing)

## Setup

Antes de começar, verifique se você atendeu aos seguintes requisitos:

* Você possui docker/docker compose instalado na sua máquina. (Em caso negativo, visite [aqui](https://docs.docker.com/engine/install/))
* Você possui interpretadores de Makefile (Se seu OS for Linux, provável que já tenha por padrão)
* **PS: É altamente recomendado rodar em um PC com OS Linux e distribuição Ubuntu**

## Instalando

Para instalar siga estas etapas:

- Clone o projeto na sua máquina (```git clone```)
- ```make build``` (Cria a network de conversacão entre os serviços rodados)
- **PS: Em caso de permissão negada, rode o comando como o usuário mais privilegiado (sudo)**

## Usando

Para usar siga estas etapas:

- ```make up``` (Sobe os serviços)
- Copie a URL onde serviço flask está sendo rodado (localhost:8000)
- Abra a seção de processo no swagger 
- Faça testes sobre a rota /processo (já deixei um processo válido como exemplo)
- É importante analisar o modelo ProcessInput para identificar quais processos são aceitos como parâmetro da rota

## Testando

Para testar a aplicação:

- Com a aplicação rodando, execute ```make test``` em outro terminal


Em caso de dúvidas ou problemas para executar, por favor entrar em contato por: marcos.mpdcl@gmail.com ou WhatsApp
