import gc
import sys
from trezorutils import halt, memcpy, model, set_mode_unprivileged, symbol  # noqa: F401

if False:
    from typing import Iterable, Iterator, TypeVar, List, Callable


def unimport_begin() -> Iterable[str]:
    return set(sys.modules)


def unimport_end(mods: Iterable[str]) -> None:
    for mod in sys.modules:
        if mod not in mods:
            # remove reference from sys.modules
            del sys.modules[mod]
            # remove reference from the parent module
            i = mod.rfind(".")
            if i < 0:
                continue
            path = mod[:i]
            name = mod[i + 1 :]
            if path in sys.modules:
                delattr(sys.modules[path], name)
    # collect removed modules
    gc.collect()


def ensure(cond: bool, msg: str = None) -> None:
    if not cond:
        if msg is None:
            raise AssertionError()
        else:
            raise AssertionError(msg)


if False:
    Chunked = TypeVar("Chunked")


def chunks(items: List[Chunked], size: int) -> Iterator[List[Chunked]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def split_words(
    sentence: str, width: int, metric: Callable[[str], int] = len
) -> Iterator[str]:
    line = []  # type: List[str]
    for w in sentence.split(" "):
        # empty word  -> skip
        if not w:
            continue
        # new word will not fit -> break the line
        if metric(" ".join(line + [w])) >= width:
            yield " ".join(line)
            line = []
        # word is too wide -> split the word
        while metric(w) >= width:
            for i in range(1, len(w) + 1):
                if metric(w[:-i]) < width:
                    yield w[:-i] + "-"
                    w = w[-i:]
                    break
        line.append(w)
    yield " ".join(line)


def format_amount(amount: int, decimals: int) -> str:
    d = pow(10, decimals)
    s = ("%d.%0*d" % (amount // d, decimals, amount % d)).rstrip("0")
    if s.endswith("."):
        s = s[:-1]
    return s


def format_ordinal(number: int) -> str:
    return str(number) + {1: "st", 2: "nd", 3: "rd"}.get(
        4 if 10 <= number % 100 < 20 else number % 10, "th"
    )


class HashWriter:
    def __init__(self, hashfunc, *hashargs, **hashkwargs):
        self.ctx = hashfunc(*hashargs, **hashkwargs)
        self.buf = bytearray(1)  # used in append()

    def extend(self, buf: bytearray):
        self.ctx.update(buf)

    def append(self, b: int):
        self.buf[0] = b
        self.ctx.update(self.buf)

    def get_digest(self, *args) -> bytes:
        return self.ctx.digest(*args)
