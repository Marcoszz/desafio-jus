class ProcessValidations():
    def __init__(self,):
        self.regions = {
            "AL": "02",
            "CE": "06"
        }
        self.segments = {
            "STATE_JUSTICE": "8"
        }
        
    def validate_region(self, process):
        identifiers = process.split("-")[1]

        region = identifiers.split(".")[3]

        if region != self.regions["AL"] and region != self.regions["CE"]:
            return False
        
        return True

    def validate_segment(self, process):
        identifiers = process.split("-")[1]

        segment = identifiers.split(".")[2]

        if segment != self.segments["STATE_JUSTICE"]:
            return False
        
        return True

process_validations = ProcessValidations()   