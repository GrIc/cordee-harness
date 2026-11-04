"""One reader per agent tool, each a module here with usage(repo, start, end): each reply of the tool in that repo
between two epoch seconds, as (role, model, tokens). The role is writer, reviewer or agent:<type>; the tokens are input,
output (reasoning included), cache_read and cache_write. A new tool is a new module, nothing else."""
import importlib
import pkgutil
import re

# A sub-agent whose description names a review or a quiz is the reviewer. Above READERS: the readers import it.
REVIEW = re.compile(r"review|quiz", re.I)

READERS = [importlib.import_module(f"{__name__}.{found.name}") for found in pkgutil.iter_modules(__path__)]
