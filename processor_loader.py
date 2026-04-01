# System imports
import importlib.util
import inspect
import sys
from pathlib import Path

# Project imports
import log
from processor_base import ProcessorBase

# Processor loader
def load_processors(extensions_dir: Path) -> list[ProcessorBase]:
    """
    Discover every *.py file in extensions_dir that contains a ProcessorBase
    subclass and return a list of instantiated processors.
    """
    processors: list[ProcessorBase] = []

    if not extensions_dir.is_dir():
        return processors

    for path in sorted(extensions_dir.glob("*.py")):
        # Python files beginning with an underscore are considered disabled and 
        # ignored.
        if path.name.startswith("_"):
            continue

        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            log.writeln(f"  [WARN] Could not load extension: {path.name}.  This will be skipped.")
            continue

        module = importlib.util.module_from_spec(spec)
        sys_path = sys.path
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            log.writeln(f"  [WARN] Error importing extension {path.name}: {exc}.  This will be skipped.")
            continue
        finally:
            # Reset sys.path to avoid extensions that attempt to play shenanigans
            # with the path.
            sys.path = sys_path

        processor = find_processor(module, path)
        if processor is None:
            continue

        processors.append(processor)
        log.writeln(f"  [OK]   {path.name} ({processor.GetName()})")

    return processors

# Processor candidate validation
def find_processor(module, path: Path) -> ProcessorBase | None:
    """Return an instance of the first ProcessorBase subclass found in module."""
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, ProcessorBase) and obj is not ProcessorBase:
            return obj()

    log.writeln(f"  [SKIP] {path.name} — no ProcessorBase subclass found")
    return None
