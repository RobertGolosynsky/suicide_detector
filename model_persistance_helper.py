import pickle
import traceback

import dill
import re

from config import *

def save_model(pipe, pipe_name):
    if not os.path.exists(current_checkpoint_directory):
        os.makedirs(current_checkpoint_directory)
    pipe_file = os.path.join(current_checkpoint_directory, "{}.{}".format(pipe_name, model_file_extension))
    pickle._dump(pipe, open(pipe_file, "wb"))


def get_models_info():
    dirs = []
    for d in os.walk(model_checkpoints_root):
        m = re.match(folder_regex, d[0])
        if m:
            dirs.append(d + (m.group(folder_regex_group_number),))
    models_info = []
    for d in dirs:
        for model_file in d[2]:
            if model_file.endswith(model_file_extension):
                model_name = model_file[:-(len(model_file_extension)+1)]

                for report_file in d[2]:
                    if "{}.{}".format(model_name, report_file_extension) == report_file:
                        for line in open(os.path.join(d[0], report_file)).readlines():
                            score_match = re.match(f1_score_regex, line)
                            if score_match:
                                f1_score = float(score_match.group(f1_score_regex_group_number))
                                models_info.append({
                                    "model_name": model_name,
                                    "model_date": d[3],
                                    "model_score": f1_score
                                })

    return models_info


def find_model(model_name, model_date):
    try:
        checkpoint_folder = os.path.join(model_checkpoints_root, create_checkpoint_folder_name_from_timestamp_string(model_date))
        model_file_path = os.path.join(checkpoint_folder, "{}.{}".format(model_name, model_file_extension))
        with open(model_file_path, 'rb') as f:
            return pickle.load(f)
    except:
        traceback.print_exc()
        return None


def best_model():
    models_info = sorted(get_models_info(), key= lambda x: x["model_score"], reverse=True)
    if len(models_info) > 0:
        info = models_info[0]
        return find_model(info["model_name"], info["model_date"])
    else:
        return None

