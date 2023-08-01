import sys
sys.path.append("src")

from constants import REGIONS, SEGMENTS

class ProcessValidator():
    def region(self, process):
        region = process.split('-')[1].split('.')[3]

        return not (region != REGIONS["AL"] and region != REGIONS["CE"])  

    def segment(self, process):
        segment = process.split('-')[1].split('.')[2]

        return not (segment != SEGMENTS["STATE_JUSTICE"])
    
validator = ProcessValidator()