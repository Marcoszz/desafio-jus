import sys
sys.path.append("src")

from constants import REGIONS, SEGMENTS

class ProcessValidator():
    def region(self, process):
        region = process.split('-')[1].split('.')[3]

        if region != REGIONS["AL"] and region != REGIONS["CE"]:
            return False
        
        return True

    def segment(self, process):
        segment = process.split('-')[1].split('.')[2]

        if segment != SEGMENTS["STATE_JUSTICE"]:
            return False
        
        return True
    
validator = ProcessValidator()