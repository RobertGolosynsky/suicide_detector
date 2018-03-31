from os.path import join

import datetime

import os

last_key = "88208b241c65e6ae5e86acdb1b81996f"

dataset_root = "dataset"


suicidal_folder_name = "suicidal"
suicidal_category_name = "suicidal"
not_suicidal_folder_name = "not suicidal"
not_suicidal_category_name = "not suicidal"

suicidal_folder_path = join(dataset_root, suicidal_folder_name)
not_suicidal_folder_path = join(dataset_root, not_suicidal_folder_name)

suicidal_artists_list_file_name = "suicidal_artists.txt"
suicidal_bands_list_file_name = "suicidal_bands.txt"
not_suicidal_artists_list_file_name = "not_suicidal_artists.txt"

suicidal_artists_list_file_path = join(dataset_root, suicidal_artists_list_file_name)
suicidal_bands_list_file_path = join(dataset_root, suicidal_bands_list_file_name)
not_suicidal_artists_list_file_path = join(dataset_root, not_suicidal_artists_list_file_name)

# model extension without '.'
model_file_extension = "model"
report_file_extension = "report"
diagram_file_extension = "png"
model_checkpoints_root = "checkpoints"

f1_score_regex = r".+avg / total\s+[+-]?([0-9]*[.])?[0-9]+\s+[+-]?([0-9]*[.])?[0-9]+\s+([+-]?([0-9]*[.])?[0-9]+)" #$3
f1_score_regex_group_number = 3
folder_regex = r".+checkpoint\s(.+)" #$1
folder_regex_group_number = 1

categories = sorted([suicidal_category_name, not_suicidal_category_name])
diagrams_folder = "image"
font_file = "fonts/Roboto-Bold.ttf"



def create_checkpoint_folder_name(date_time):
    return "checkpoint {}".format(date_time.strftime('%Y-%m-%d %H-%M-%S'))

def create_checkpoint_folder_name_from_timestamp_string(date_time):
    return "checkpoint {}".format(date_time)

now = datetime.datetime.now()
current_checkpoint_directory = os.path.join(model_checkpoints_root, create_checkpoint_folder_name(now))