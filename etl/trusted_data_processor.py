from data_processor import DataProcessor

class TrustedDataProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def _process(self):
        print("Processing raw data")