import logging as log
import keras as ks

log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TrainingCall(ks.callbacks.Callback):
    def __init__(self, threshold=float(0.90), epochs=10):
        super(TrainingCall, self).__init__()
        self.threshold = threshold
        self.epochs = epochs

    def on_epoch_end(self, epoch, logs=None): 
        if logs.get('accuracy') >= self.threshold :
            log.info(f"Reached {self.threshold} accuracy so stopping training")
            self.model.stop_training = True
        elif epoch >= self.epochs:
            log.info(f"Reached {self.epochs} epochs so stopping training")
            self.model.stop_training = True
        