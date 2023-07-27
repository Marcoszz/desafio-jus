import sys
sys.path.append("models")
sys.path.append("services")
sys.path.append("utils")

from flask_restx import Resource, Namespace, abort
from models import process_input_model
from services.process import process_service
from exceptions import ProcessNotFromExpectedAreaException, ProcessNotFromStateJusticeSegmentException

ns = Namespace("processo", description="Rotas relacionadas ao processo.")

@ns.route("/")
class Process(Resource):
    @ns.doc(
        description="Recupera dados (em todos os graus) do processo.", 
        responses={
            200: "Success",
            400: "Bad Request",
            404: "Not Found"
            }
        )
    @ns.expect(process_input_model)
    def post(self):
        payload = ns.payload

        try:
            return {"response": process_service.get_process(payload["process"])}
        except Exception as e:
            if type(e) == type(ProcessNotFromExpectedAreaException()) 
            or type(e) == type(ProcessNotFromStateJusticeSegmentException()):
                abort(400, str(e))
            
            abort(500, str(e))


