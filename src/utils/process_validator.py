import sys
sys.path.append("src")

from constants import REGIONS, SEGMENTS

class ProcessValidator():
    def validate_region(self, process):
        identifiers = process.split("-")[1]

        region = identifiers.split(".")[3]

        if region != REGIONS["AL"] and region != REGIONS["CE"]:
            return False
        
        return True

    def validate_segment(self, process):
        identifiers = process.split("-")[1]

        segment = identifiers.split(".")[2]

        if segment != SEGMENTS["STATE_JUSTICE"]:
            return False
        
        return True
    
validator = ProcessValidator()