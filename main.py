from corpora.Switchboard.Switchboard import Switchboard
from corpora.viot.Viot import Viot
from trainers.svm_trainer import SVMTrain
import sys
import os
import csv

#switchboard = Switchboard("/home/zeio/datasets/swbd")
viot = Viot(sys.argv[-1])
# print loaded corpus in csv format
# print(dir(viot))
# print(viot.corpus)


svm_trainer = SVMTrain([viot])
#svm_trainer.train_task("svm-models-viot")
#svm_trainer.train_som("svm-models-viot")
svm_trainer.train_all("svm-models-viot")

