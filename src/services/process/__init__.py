import sys
sys.path.append("utils")
sys.path.append("src")
sys.path.append("services")

from utils.process_validator import validator
from exceptions import InvalidCourtException, InvalidSegmentException, ProcessNotFoundException
from services.selenium import selenium_service
from constants import REGIONS, URLS
from json import loads, dumps

import crawler
from subprocess import run, PIPE

class ProcessService:
    def get_process(self, process):
        if not validator.region(process):
            raise InvalidCourtException()

        if not validator.segment(process):
            raise InvalidSegmentException()
        
        process_urls = selenium_service.get_process_urls(self.get_court_urls(process), process)
        
        if not len(process_urls):
            raise ProcessNotFoundException()
        elif len(process_urls) == 2:
            command = ["python", "services/crawler/crawler.py", "--urls", process_urls[0], process_urls[1]]  
        else:
            command = ["python", "services/crawler/crawler.py" "--urls", process_urls[0]]
            
        call = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print(call.stderr, "\n")
        
        return loads(call.stdout.strip())
    
    def get_court_urls(self, process):
        region = process.split('-')[1].split('.')[3]

        if region == REGIONS["AL"]:
            return URLS["TJAL"]
        else:
            return URLS["TJCE"]

process_service = ProcessService()