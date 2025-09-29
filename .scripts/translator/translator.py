import asyncio
import concurrent.futures as cft
import multiprocessing
import os
import os.path as path
import queue
import time
from argparse import ArgumentParser

from tqdm import tqdm

from auto_translate.file_handling import LANGUAGE_MAPPER, load_yaml, get_all_files, validate_all_files
from google_translate import GoogleTranslator
from utils import set_proxy_queue


def save(translated: dict, output_file, target_language):
    # Create directory if it does not exist
    directory = os.path.dirname(output_file)
    os.makedirs(directory, exist_ok=True)
    with open(output_file, "w", encoding="UTF-8-sig") as f:
        f.write(f"l_{target_language}:\n")
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
    # check for syntax errors before translation
    has_syntax_error = validate_all_files(source, target)
    if has_syntax_error:
        raise ValueError(f'Aborting translation, there are YML syntax errors!')
    all_files: list[tuple] = get_all_files(source, target)
    with cft.ProcessPoolExecutor(
            max_workers=4
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
