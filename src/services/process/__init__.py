import sys
sys.path.append("utils")
sys.path.append("src")
sys.path.append("services")

from utils.process_validator import validator
from exceptions import ProcessNotFromExpectedAreaException, ProcessNotFromStateJusticeSegmentException, ProcessNotFoundException
from services.selenium import selenium_service
from constants import REGIONS, URLS
from json import loads, dumps

import crawler
from subprocess import check_output, run, PIPE

class ProcessService:
    def get_process(self, process):
        if not validator.region(process):
            raise ProcessNotFromExpectedAreaException()

        if not validator.segment(process):
            raise ProcessNotFromStateJusticeSegmentException()
        
        urls = selenium_service.get_process_urls(self.get_court_urls(process), process)
        
        if not len(urls):
            raise ProcessNotFoundException()
        
        try:
            command = ["python", "services/crawler/crawler.py", "--urls", urls[0], urls[1]]  
        except:
            command = ["python", "services/crawler/crawler.py" "--urls", urls[0]]
            
        
        call = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print(call.stderr, "\n")
        
        formatted_response = call.stdout.replace("'", "\"").replace("None", "null")
        
        return loads(formatted_response)
    
    def get_court_urls(self, process):
        region = process.split('-')[1].split('.')[3]

        if region == REGIONS["AL"]:
            return URLS["TJAL"]
        else:
            return URLS["TJCE"]

process_service = ProcessService()