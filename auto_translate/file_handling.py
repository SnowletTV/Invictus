import os
from os import path as path

import yaml

LANGUAGE_MAPPER = {
    'english': 'en',
    'german': 'de',
    'italian': 'it',
    'french': 'fr',
    'spanish': 'es'
}


def clean_yaml(text: str) -> str:
    for i in range(0, 10):
        text = text.replace(f":{i}", ":")
    return text


def read_file_into_string(file_name: str) -> str:
    with open(file_name, encoding='utf_8_sig') as f:
        text = f.read()
    return text


def load_yaml(file_name: str) -> dict:
    text = read_file_into_string(file_name)
    clean_text = clean_yaml(text)
    data = yaml.safe_load(clean_text)
    return data


def get_all_files(source_language: str, target_language: str) -> list[tuple]:
    all_source_files = []
    source_folder: str = path.abspath(path.join(__file__, f'../../localization/{source_language}'))
    for _path, sub_dir, files in os.walk(source_folder):
        _files = [path.abspath(path.join(_path, file)) for file in files]
        all_source_files.extend(_files)
    # create the equivalent target language path e.g. _english.yml to _german.yml
    all_files = [(source, source.replace(f'_{source_language}.yml', f'_{target_language}.yml')) for source in
                 all_source_files]
    # also adjust the target language folder name, e.g. /english/... to /german/...
    all_files = [(x[0], x[1].replace(f'\\{source_language}\\', f'\\{target_language}\\')) for x in all_files]
    return all_files


def validate_all_files(source: str, target: str = 'english') -> bool:
    error_found = False
    all_files = get_all_files(source, target)
    for source_file, _ in all_files:
        try:
            load_yaml(source_file)
        except Exception as e:
            print(f"Error in file '{source_file}': {e}")
            error_found = True
    return error_found


if __name__ == '__main__':
    language_errors = {}
    for source, source_code in LANGUAGE_MAPPER.items():
        has_syntax_error = validate_all_files(source)
        if has_syntax_error:
            language_errors[source] = 'ERROR'
        else:
            language_errors[source] = 'OK'

    print(f'{"Language":<15} {"Status":<15}')
    print('-' * 30)
    for source, status in language_errors.items():
        print(f'{source:<15} {status:<15}')
    print('-' * 30)

    if 'ERROR' in language_errors.values():
        raise ValueError(f"Aborting translation, there are YML syntax errors!")
