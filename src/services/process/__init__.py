import sys
sys.path.append("utils")
sys.path.append("src")

from utils.process_validator import validator
from exceptions import ProcessNotFromExpectedAreaException, ProcessNotFromStateJusticeSegmentException, ProcessNotFoundException
from ..selenium import selenium_service
from constants import REGIONS, URLS

class ProcessService:
    def get_process(self, process):
        if not validator.validate_region(process):
            raise ProcessNotFromExpectedAreaException()

        if not validator.validate_segment(process):
            raise ProcessNotFromStateJusticeSegmentException()
        
        court_urls = self.get_court_urls(process)
        process_urls = selenium_service.get_process_urls(court_urls, process)
        
        if not len(process_urls):
            raise ProcessNotFoundException()

        return [process, process_urls]
    
    def get_court_urls(self, process):
        identifiers = process.split("-")[1]

        region = identifiers.split(".")[3]

        if region == REGIONS["AL"]:
            return URLS["TJAL"]
        else:
            return URLS["TJCE"]

process_service = ProcessService()