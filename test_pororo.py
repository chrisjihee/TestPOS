import sys

from pororo import Pororo

from basic.io import *
from basic.time import *


def to_tagged(lemma_tags):
    spaced = [[]]
    for lemma, tag in lemma_tags:
        if tag == 'SPACE':
            spaced.append([])
        else:
            spaced[-1].append(f"{lemma}/{tag}")
    return ' '.join(['+'.join(word) for word in spaced])


def tag_sentences(infiles: Path, outfiles: Path, idx_text: int = -1):
    clock = StopWatch()
    with TimeJob(f"tag_sentences(infiles={infiles}, outfiles={outfiles})"):
        tot_sent, tot_word, tot_anal = 0, 0, timedelta()
        with clock:
            tagger = Pororo(task="pos", lang="ko")
        tot_init = clock.delta()
        for infile in files(infiles):
            idx = idx_text if idx_text >= 0 else 2 if infile.suffix.strip().lstrip('.').lower() == "tsv" else 0
            outfile = new_file(infile, outfiles)
            one_sent, one_word, one_anal = 0, 0, timedelta()
            with infile.open() as inp, outfile.open('w') as out:
                for line in inp.readlines():
                    row = line.rstrip().split('\t')
                    text = row[idx] if len(row) > idx else row[0]
                    with clock:
                        res = tagger(text)
                    one_anal += clock.delta()
                    one_word += len(text.split())
                    one_sent += 1
                    out.write(f"*\t{infile.name}\t{text}\t{to_tagged(res)}\n")
                    out.flush()
            tot_anal += one_anal
            tot_word += one_word
            tot_sent += one_sent
            print(f" + [File] {infile.stem}\t#sent={one_sent:7,d}\t#word={one_word:7,d}\t$anal={one_anal.total_seconds():7.3f}")
        with clock:
            del tagger
        tot_exit = clock.delta()
        print(f" + [Stat] totSent={tot_sent}")
        print(f" + [Stat] totWord={tot_word}")
        print(f" + [Stat] totAnal={tot_anal.total_seconds():.3f}")
        print(f" + [Stat] totInit={tot_init.total_seconds():.3f}")
        print(f" + [Stat] totExit={tot_exit.total_seconds():.3f}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python test_pororo.py (infiles) (outfiles)")
        exit(1)

    tag_sentences(infiles=Path(sys.argv[1]), outfiles=Path(sys.argv[2]))
