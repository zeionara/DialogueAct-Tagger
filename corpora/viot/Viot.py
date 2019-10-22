import os
import re
from corpora.Corpus import Corpus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ISO_DA")


class Viot(Corpus):
    def __init__(self, file):
        Corpus.__init__(self, file)
        self.file = file
        self.load_data()

    def get_corpus_name(self):
        return "VoiceIoT"

    def load_data(self):
        # check whether the folder contains a valid Switchboard installation
        try:
            assert os.path.exists(self.file)
        except AssertionError:
            logging.warning("The folder " + self.file + " does not exist.")
            self.corpus = None
            return
        # Read dialogue files from Switchboard
        self.csv_corpus = self.create_corpus(self.file)

    def create_corpus(self, filename):
        csv_corpus = []
        prev_speaker = None
        segment = 0
        prev_DAs = {"A": "%", "B": "%"}
        with open(filename) as f:
            utterances = f.readlines()
        for line in utterances:
            line = line.strip()
            try:
                sentence, sw_tag = line.split('|')
                speaker = "A"
            except:  # not an SWDA utterance format: probably a header line
                continue
            if speaker != prev_speaker:
                prev_speaker = speaker
                segment += 1
            sentence = re.sub(r'\W+', ' ', sentence)  # this REGEX removes non alphanumeric characters
            sentence = ' '.join(sentence.split())  # this is just to make extra spaces collapse
            csv_corpus.append((sentence, sw_tag, prev_DAs[speaker], segment, None, None))
            prev_DAs[speaker] = sw_tag
        return csv_corpus

    def corpus_tuple_to_iso_task(self, corpus_tuple):
        # if self.da_to_dimension(corpus_tuple) == "Task":
        da = self.da_to_cf(corpus_tuple)
        prevDA = self.da_to_cf((None, corpus_tuple[2], None, None, corpus_tuple[5], None))
        if prevDA is None:
            prevDA = "Other"
        if da is not None:
            return tuple([corpus_tuple[0]] + [da, prevDA] + list(corpus_tuple[2:]))
        else:
            return None

    def corpus_tuple_to_iso_som(self, corpus_tuple):
        # if self.da_to_dimension(corpus_tuple) == "SocialObligationManagement":
        da = self.da_to_cf(corpus_tuple)
        prevDA = self.da_to_cf((None, corpus_tuple[2], None, None, corpus_tuple[5], None))
        if prevDA is None:
            prevDA = "Other"
        if da is not None:
            return tuple([corpus_tuple[0]] + [da, prevDA] + list(corpus_tuple[2:]))
        else:
            return None

    def corpus_tuple_to_iso_task_dimension(self, corpus_tuple):
        da = self.da_to_dimension(corpus_tuple)
        prevDA = self.da_to_cf((None, corpus_tuple[2], None, None, corpus_tuple[5], None))
        # if prevDA is None:
        #     prevDA = "Other"
        # if da is not None:
        #     if da != "Task":
        #         da = "Other"
        return tuple([corpus_tuple[0]] + [da, prevDA] + list(corpus_tuple[2:]))
        # else:
        #     return None

    def corpus_tuple_to_iso_som_dimension(self, corpus_tuple):
        da = self.da_to_dimension(corpus_tuple)
        prevDA = self.da_to_cf((None, corpus_tuple[2], None, None, corpus_tuple[5], None))
        # if prevDA is None:
        #     prevDA = "Other"
        # if da is not None:
        #     if da != "SocialObligationManagement":
        #         da = "Other"
        return tuple([corpus_tuple[0]] + [da, prevDA] + list(corpus_tuple[2:]))
        # else:
        #     return None

    def corpus_tuple_to_iso_fb_dimension(self, corpus_tuple):
        da = self.da_to_dimension(corpus_tuple)
        prevDA = self.da_to_cf((None, corpus_tuple[2], None, None, corpus_tuple[5], None))
        # if prevDA is None:
        #     prevDA = "Other"
        # if da is not None:
        #     if da != "Feedback":
        #         da = "Other"
        return tuple([corpus_tuple[0]] + [da, prevDA] + list(corpus_tuple[2:]))
        # else:
        #     return None

    @staticmethod
    def da_to_dimension(corpus_tuple):
        return corpus_tuple[1]

    @staticmethod
    def da_to_cf(corpus_tuple):
        return corpus_tuple[1]