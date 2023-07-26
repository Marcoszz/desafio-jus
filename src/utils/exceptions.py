class ProcessNotFoundException(Exception):
    def __init__(self):
        super().__init__("Processo não encontrado!")

class ProcessNotFromExpectedAreaException(Exception):
    def __init__(self):
        super().__init__("Processo não pertence aos tribunais definidos (TJAL e TJCE)!")

class ProcessNotFromStateJusticeSegmentException(Exception):
    def __init__(self):
        super().__init__("Processo não pertence ao segmento da justiça dos estados!")