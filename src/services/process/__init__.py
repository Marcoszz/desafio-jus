import sys
sys.path.append("utils")

from utils.processValidations import process_validations
from exceptions import ProcessNotFromExpectedAreaException, ProcessNotFromStateJusticeSegmentException

class ProcessService:
    def get_process(self, process):
        if not process_validations.validate_region(process):
            raise ProcessNotFromExpectedAreaException()

        if not process_validations.validate_segment(process):
            raise ProcessNotFromStateJusticeSegmentException()
            
        return process

process_service = ProcessService()