import sys
sys.path.append("extensions")

import re

from extensions import api
from flask_restx import fields

PROCESS_FORMAT = r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$'

process_input_model = api.model("ProcessInput", {
    "process": fields.String(
        pattern=PROCESS_FORMAT, 
        example="0710802-55.2018.8.02.0001", 
        required=True,
        description="Número do processo"
        )
})