from flask_restx import Api

api = Api(
    title="Desafio Jusbrasil", 
    description="API feita para recuperação de dados de um processo em todos os seus graus.",
    validate=True
    )