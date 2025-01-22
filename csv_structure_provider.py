import os
from pathlib import Path

class Config:
    BASE_CSV_DIR = None
    ENG_DIR = None
    JP_DIR = None
    QUEST_DIR = "quest"
    CUTSCENE_DIR = "cut_scene"

    @classmethod
    def initialize_language_base_directories(cls, base_dir):
        # Ensure the base_dir is a valid directory path
        if base_dir and os.path.isdir(base_dir):
            cls.BASE_CSV_DIR = base_dir
            cls.ENG_DIR = os.path.join(cls.BASE_CSV_DIR, 'eng')
            cls.JP_DIR = os.path.join(cls.BASE_CSV_DIR, 'jp')
            print(f"Base directory initialized: {cls.BASE_CSV_DIR}")
            print(f"English directory: {cls.ENG_DIR}")
            print(f"Japanese directory: {cls.JP_DIR}")
        else:
            print("Invalid base directory provided")


def list_csv_files_in_directory(base_path):
    csv_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):
                full_path = os.path.join(root, file)
                csv_files.append(full_path)
    return csv_files


def list_quest_files_for_language(language_name):
    return list_quest_files_for_language(language_name, Config.BASE_CSV_DIR)


def list_quest_files_for_language(language_name, csv_directory):
    if language_name.lower() == 'eng':
        return list_quest_files_for_eng(csv_directory)
    elif language_name.lower() == 'jp':
        return list_quest_files_for_jp(csv_directory)
    else:
        raise ValueError(f"Unsupported language: {language_name}")


def list_quest_files_for_eng(csv_directory):
    eng_quest_path = os.path.join(os.path.join(csv_directory, 'eng'), Config.QUEST_DIR)
    return list_csv_files_in_directory(eng_quest_path)

def list_cutscene_files_for_eng(csv_directory):
    eng_ct_path = os.path.join(os.path.join(csv_directory, 'eng'), Config.CUTSCENE_DIR)
    return list_csv_files_in_directory(eng_ct_path)


def list_quest_files_for_jp(csv_directory):
    jp_quest_path = os.path.join(os.path.join(csv_directory, 'jp'), Config.QUEST_DIR)
    return list_csv_files_in_directory(jp_quest_path)

def list_cutscene_files_for_jp(csv_directory):
    jp_ct_path = os.path.join(os.path.join(csv_directory, 'jp'), Config.CUTSCENE_DIR)
    return list_csv_files_in_directory(jp_ct_path)
