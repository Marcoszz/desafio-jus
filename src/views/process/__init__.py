import sys
sys.path.append("models")
sys.path.append("services")

from flask_restx import Resource, Namespace
from models.process import process_input_model
from services.process import process_service

ns = Namespace("processo", description="Rotas relacionadas ao processo.")

@ns.route("/")
class Process(Resource):
    @ns.doc(description="Recupera dados (em todos os graus) do processo.")
    @ns.expect(process_input_model)
    def post(self):
        payload = ns.payload

        try:
            return {"response": process_service.get_process(payload["processId"])}
        except Exception as e:
            print(type(e))