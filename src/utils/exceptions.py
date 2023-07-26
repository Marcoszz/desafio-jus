class ProcessNotFoundException(Exception):
    def __init__(self):
        super().__init__("Processo não encontrado!")