import glob
import math
import shutil
import multiprocessing
import collections
import os
import random

from logzero import logger

from UnicodeTokenizer.UnicodeTokenizer import UnicodeTokenizer
from matplotlib.pyplot import sca

from common import read, load_frequency

tokenizer = UnicodeTokenizer()


def get_langs():
    alphabet = ''.join(chr(x) for x in range(ord('a'), ord('z')+1))
    langs = [x+y for x in alphabet for y in alphabet]
    return langs


def lang_files(lang):
    # C:/data/wiki-20220606-cirrussearch-content-txt-bz2/aawiki-20220606-cirrussearch-content.txt.bz2
    files = glob.glob(
        f"F:/data/wiki-20220606-cirrussearch-content-txt-bz2/{lang}*-20220606-cirrussearch-content.txt.bz2")

    return list(files)


def token(line):
    return tokenizer.tokenize(line)


def count_files(files):
    counter = collections.Counter()
    logger.info(f" reading:{files} ")
    for i, src in enumerate(files):
        logger.info(
            f" lang:{files[i]} file:{i}/{len(files)} counter:{len(counter)} ")
        n_line = 0
        reader = read(src)
        for l in reader:
            n_line += 1
            if not l:
                continue
            if n_line == 1:  # may warning msg
                continue
            tokens = token(l)
            for x in tokens:
                if not x:
                    continue
                counter[x] += 1
    logger.info(
        f" n_line:{n_line} counter:{len(counter)} ")
    return counter


def scan_lang(lang):
    files = lang_files(lang)
    logger.info(f"{lang} found {len(files)} files")

    dir = f"C:/data/languages/{lang}"
    if len(files) == 0:
        logger.warning(f"{lang} no files")
        if os.path.exists(dir):
            shutil.rmtree(dir)
            logger.warning(f"{dir} removed")
        return lang+" none"

    os.makedirs(dir, exist_ok=True)
    tgt = f"{dir}/word_frequency.tsv"
    if os.path.exists(tgt):
        logger.warning(f"{tgt} exists, remove")
        # return
        os.remove(tgt)
    counter = count_files(files)
    if not counter:
        logger.warning(f" word_counter:{len(counter)} --> None  ")
        if os.path.exists(dir):
            shutil.rmtree(dir)
            logger.warning(f"{dir} removed")
        return lang+" 0"

    words = list(counter.items())
    del counter
    words.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    with open(tgt, "w") as f:
        for k, v in words:
            f.write(f"{k}\t{v}"+'\n')
    logger.info(f" word_counter:{len(words)} --> {tgt}  ")
    return lang+f' {len(words)}'


def coung_global():
    counter = collections.Counter()
    langs = get_langs()
    dir = f"C:/data/languages/global"
    os.makedirs(dir, exist_ok=True)
    freq_paths = [
        f"C:/data/languages/{lang}/word_frequency.tsv" for lang in langs]
    for src in freq_paths:
        if not os.path.exists(src):
            continue
        for l in open(src):
            l = l.strip()
            w = l.split('\t')
            k, v = w
            v = int(v)
            counter[k] += math.pow(v, 0.75)
        logger.info(f"src???{src} counter:{len(counter)}")
    words = [(k, int(v)) for k, v in counter.items() if v > 1.1]
    del counter
    words.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    total = 0
    tgt = f"{dir}/word_frequency.tsv"
    with open(tgt, "w") as f:
        for k, v in words:
            f.write(f"{k}\t{v}"+'\n')
            total += 1
    logger.info(f" word_counter:{total} --> {tgt}")


if __name__ == "__main__":
    import multiprocessing

    langs = get_langs()
    langs = ['en']+[x for x in langs if x != 'en']
    with multiprocessing.Pool(8) as pool:
        re = pool.imap_unordered(scan_lang, langs)
        for i, x in enumerate(re):
            logger.info((i, x))

    coung_global()
