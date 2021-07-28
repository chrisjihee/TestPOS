from pathlib import Path


def files(path: Path):
    return sorted([x for x in path.parent.glob(path.name) if x.is_file()])


def new_file(infile: Path, outfiles: Path, blank=('', '*', '?')) -> Path:
    parent = outfiles.parent
    parent.mkdir(parents=True, exist_ok=True)

    suffix1 = infile.suffix.strip().lstrip('.')
    suffix2 = outfiles.suffix.strip().lstrip('.')
    suffix = suffix1 if suffix2 in blank else suffix2

    stem1 = infile.stem.strip()
    stem2 = outfiles.stem.strip()
    stem = stem1 if any(x and x in stem2 for x in blank) else stem2

    outfile: Path = parent / f"{stem}.{suffix}"
    assert infile != outfile, f"infile({infile}) == outfile({outfile})"

    return outfile
