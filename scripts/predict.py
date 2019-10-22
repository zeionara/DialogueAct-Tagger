import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config import Config, Model
import argparse
from predictors.svm_predictor import SVMPredictor
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ISO_DA")

def increment_if_equal(hyp, ref, counter):
    if ref == hyp:
        counter[0] += 1
    counter[1] += 1
    return counter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DialogueActTag - Tag a sentence with the ISO dialogue act taxonomy')
    parser.add_argument('-model', dest='model', type=str,
                        help='the model folder to use for prediction')
    parser.add_argument('-class', dest='layer', type=str, default="all",
                        help='which level of the taxonomy to tag. Options are: \n'
                             'all -- trains all the classifiers (default)'
                             'dim -- trains the dimension classifier'
                             'task -- trains the task CF classifier'
                             'som -- trains the SOM CF classifier')
    parser.add_argument('-s', dest='sentences', type=str, help="sentences to tag")
    #parser.add_argument('-s', dest='sentence', type=str, help="the sentence to tag")
    parser.add_argument('-p', dest='prev', type=str, default="Other", help="[optional] the previous sentence in the dialogue")

    args = parser.parse_args()
    if args.model is None or args.sentences is None:
        parser.print_help(sys.stderr)
        exit(1)

    logger.info("Restoring model config from meta.json")
    cfg = Config.from_json(f"{args.model}/meta.json")
    if cfg.model_type == Model.SVM:
        logger.info("Loading SVM tagger")
        tagger = SVMPredictor(cfg)
    else:
        raise NotImplementedError(f"Unknown classifier type: {cfg.model_type}")
    logger.info("Tagging utterances")

    with open(args.sentences, "r") as file:
        lines = file.readlines()
        test_pairs = [line.replace("\n", "").split("|") for line in lines]
        print(f"{'command'}\t{'true_tag'}\t{'task_tag'}\t{'som_tag'}")
        task_counter = [0, 0]
        som_counter = [0, 0]
        for pair in test_pairs:
            task_tag = tagger.tag_task(pair[0], args.prev)
            som_tag = tagger.tag_som(pair[0], args.prev)
            print(f"{pair[0]}\t{pair[1]}\t{task_tag}\t{som_tag}")
            task_counter = increment_if_equal(task_tag, pair[1], task_counter)
            som_counter = increment_if_equal(som_tag, pair[1], som_counter)

    print(f"Task accuracy: {task_counter[0]/task_counter[1]}")
    print(f"Som accuracy: {som_counter[0]/som_counter[1]}")

    # print(f"Dialogue act tag: {tagger.dialogue_act_tag(args.sentence, args.prev)}")
    # print(f"Task tag: {tagger.tag_task(args.sentence, args.prev)}")
    # print(f"Task som: {tagger.tag_task(args.sentence, args.prev)}")
