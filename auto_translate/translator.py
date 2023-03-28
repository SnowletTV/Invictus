import asyncio
import multiprocessing
import os.path as path
import os
import queue
import time
import yaml
from tqdm import tqdm
from argparse import ArgumentParser
from google_translate import GoogleTranslator
import concurrent.futures as cft
from utils import set_proxy_queue, chunk_list_of_tuples

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


def save(translated: dict, output_file, target_language):
    with open(output_file, "w", encoding="UTF-8-sig") as f:
        f.write(f"_{target_language}:\n")
        for k, v in translated.items():
            v = v.replace('\n', r' \n')
            f.write(f'  {k}:0 "{v}"\n')


async def translate_document(source_path, source_language, target_language):
    os.makedirs(path.dirname(source_path), exist_ok=True)
    yaml_data = load_yaml(source_path)
    source_key = f'l_{source_language}'
    if isinstance(yaml_data.get(source_key, None), dict):
        # source data follows the correct yaml structure
        yaml_data = {key: value for key, value in yaml_data[source_key].items()}
    else:
        # source data follows the false yaml structure
        # filter the first entry of each file, e.g. l_english, l_german, ...
        yaml_data = {key: value for key, value in yaml_data.items() if key != f'l_{source_language}'}
    google_translator = GoogleTranslator(
        source=LANGUAGE_MAPPER[source_language],
        target=LANGUAGE_MAPPER[target_language]
    )
    translated = await google_translator.translate_batch(yaml_data)
    return translated


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


async def main_translate(source: str, target: str, source_path: str, target_path: str,
                         _progress: multiprocessing.Queue):
    translated = await translate_document(source_path, source, target)
    save(translated, target_path, target)
    _progress.put(1)


def worker_main(source: str, target: str, all_files: tuple, _queue: multiprocessing.Queue,
                _progress: multiprocessing.Queue):
    set_proxy_queue(_queue)
    asyncio.run(
        main_translate(
            source,
            target,
            all_files[0],
            all_files[1],
            _progress)
    )


def update_progress(progress_queue: multiprocessing.Queue, total_items: list[tuple], pieces: list[list],
                    finished: multiprocessing.Value):
    with tqdm(total=len(total_items)) as progress:
        while True:
            try:
                progress_queue.get(block=False)
                progress.update(1)
            except queue.Empty:
                time.sleep(1)
            if finished.value == len(pieces):
                break  # done all


def increment_finished(finished: multiprocessing.context, finished_lock: multiprocessing.context):
    with finished_lock:
        finished.value += 1


def main(source: str, target: str):
    all_files: list[tuple] = get_all_files(source, target)
    with cft.ProcessPoolExecutor(
            max_workers=8
    ) as pool, multiprocessing.Manager() as manager:
        _queue = manager.Queue()
        _progress = manager.Queue()
        _finished_lock = manager.Lock()
        _finished = manager.Value('i', 0)
        futures = [pool.submit(update_progress, _progress, all_files, all_files, _finished)]
        futures.extend([pool.submit(worker_main, source, target, _p, _queue,
                                    _progress) for _p in all_files])
        for future in cft.as_completed(futures):
            future.result()
            increment_finished(_finished, _finished_lock)
            if future.cancelled() or future.exception() is not None:
                print(f'Future failed unexpectedly: {future}')
    print('Translation is fully completed!')


if __name__ == '__main__':
    parser = ArgumentParser(description='Argument Parser for the auto-translator')
    parser.add_argument(
        "-src",
        "--source",
        type=str,
        help=f'Specify the source language. Allowed values: {LANGUAGE_MAPPER.keys()}',
    )
    parser.add_argument(
        "-tgt",
        "--target",
        type=str,
        help=f'Specify the target language. Allowed values: {LANGUAGE_MAPPER.keys()}',
    )
    _args = parser.parse_args()
    _source = _args.source.lower()
    _target = _args.target.lower()
    if _source == _target:
        raise ValueError(f'The source and target language cannot be the same!')
    if _source not in LANGUAGE_MAPPER.keys() or _target not in LANGUAGE_MAPPER.keys():
        raise ValueError(f'The language is not supported. Allowed languages: {LANGUAGE_MAPPER.keys()}')
    if not _source or not _target:
        raise ValueError('Please ensure to provide no empty values for source and target language!')
    main(source=_source, target=_target)
