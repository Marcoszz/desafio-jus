class ProcessNotFoundException(Exception):
    def __init__(self):
        super().__init__("Processo não encontrado!")

class InvalidCourtException(Exception):
    def __init__(self):
        super().__init__("Processo não pertence aos tribunais definidos (TJAL e TJCE)!")

class InvalidSegmentException(Exception):
    def __init__(self):
        super().__init__("Processo não pertence ao segmento da justiça dos estados!")