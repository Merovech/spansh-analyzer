# spansh-analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

(Build automation coming soon)

Tool for analyzing galaxy data from spansh data dumps.  Extensible to allow for custom scripts.

## What is this?
spansh-analyzer is an application that analyzes systems as they are parsed from [Spansh Data Dumps].  It runs a relatively simple loop over the data:

1. Grab the next line in the file and parse it into an object model.
2. Pass the object model to any processors found in the system.
3. When everything is complete, allow each to report the results of their work.

By way of example, there are two example processors provided in source and downloads.  One counts the number of bodies that have been encountered and reports the final count at the end of the process, and the other counts the total population the bodies have along with the average across all populated systems.

Here's the output from a sample run without the verbose logging flag (the warning has been removed to keep the output shorter; see below for information on that):

```txt
> ./spanshan.exe -i /d/data/galaxy_1day.json
[OK] Input file found at 'D:/data/galaxy_1day.json'
[OK] Input file is a JSON file.
Loading processors...
  [OK]   count_bodies.py (Body Counter Example)
  [OK]   count_population.py (Population Counter Example)

Initializing all processors...
Done.

Process statistics:
-------------------
  Processed: 146891
  Errors   : 0
  Elapsed  : 00:00:24

Results:
--------
Total bodies found: 715453
Total population found: 4616871739026
Average per populated system: 303501954
```

Galaxy parsing to an object model is done using the [Elite.SpanshTools](https://github.com/Merovech/Elite.SpanshTools) library that I built.  The first time the application is run it will download the latest version of the library from NuGet, so you don't need to install it yourself.  (If you need to update it, juust delete the `lib` directory and the next time you run the tool it will re-download.)

Everything is also logged to a file (timestamp as the name) in the same directory as the application entry point.

## Prerequisites
Python 3.xx

.NET 8.0 (the requirements are the same as [pythonnet](https://github.com/pythonnet/pythonnet))

## Usage
### From source
See below for using information
```txt
python main.py [-h] [-v] -i FILE [-n N]
```

Usage information can be found using the `--help` flag:

### From exe
```txt 
spanshan.exe [-h] [-v] -i FILE [-n N]
```

### Usage details
```txt
Parse a Spansh galaxy JSON dump and run all extension processors.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose logging.
  -i FILE, --input-file FILE
                        Path to the Spansh galaxy JSON file to process.
  -n N, --console-interval N
                        How often (in systems) to update the processing status. Default: 10000.
```

## Creating new processors
Before the file is parsed, the application looks at the `./extensions` directory next to the application's entry point. From there, it will try to scan any python file it sees unless that file is prefixed with an underscore, in which case it will be ignored.

Each processor must be a Python class that inherits from `ProcessorBase` and implements the following four methods:

| Name | Description | Run Frequency |
| - | - | - |
| `GetName()` | Returns the display name of the processor | As needed |
| `Initialize()` | Intialize the processor however it needs | Once |
| `ProcessSystem()` | Processes each system in the dump file | Once per file entry |
| `Completed()` | Runs when the main loop is complete to output results | Once |

Two sample processors -- `count_bodies.py` and `count_population.py` are provided in the source tree and binary package.

The object model isn't completely documented yet -- that's my next project -- but the objects are all simple POCOs (Plain Old C# Objects) and thus the source itself is somewhat self-documenting: https://github.com/Merovech/Elite.SpanshTools/tree/main/src/Model

## A Note on Security
Because you (or anyone else) can write your own processors, and because those processors are written in Python, there are *no guardrails* to what this tool can do.  So please be careful and **run only scripts you have created yourself or ones you trust**.

I do not sandbox the processors in any way and take no responsibility for malicious third-party processors.  Though if there are persistent problems that can be worked around I will happily work with the community to overcome them.

A warning is provided at the beginning of every run.  If you do not wish to see it, you can suppress it by creating an empty file called `.warnignore` next to either `main.py` or the exe you used.

## Contributing
I'm more than happy to take any assistance people wish to improve on this.  To that end a script has been provided called `build.py` does the following:

* Clear out the `./dist` folder
* Build the .exe using PyInstaller
* Copies over required files for NuGet restoration
* Copies over the example scripts into an `./extensions folder`.

Usage is dirt simple:
```txt
python build.py
```

Results will be in the `./dist` folder.

## Future Plans
:arrow_forward:= In Progress
:white_check_mark:= Complete
:black_square_button:= Not started
:grey_question:= Idea (needs investigation)

* :black_square_button: Set up a GitHub project for bug/feature progress tracking
* :black_square_button: Set up GitHub actions for checkins and releases
* :black_square_button: Turn this readme into a wiki
* :black_square_button: Feature: add NuGet version checking to replace the .NET package when its outdated

## Changelist
### 1.0.0
* Initial release

## Thanks and Final Notes
Hopefully the community will find this useful.  I wrote it primarily because I started thinking things like, "How can I get statistics on a one-off basis without having to maintain my own copy of a database?"  Then it turned into "Can I use Python to make an extensible tool that reuses my .NET package?".  And here we are.

Thanks to Spansh for all the work he does both in providing these dumps to the Elite community and creating phenomenally useful [tools](https://www.spansh.co.uk/plotter) for CMDRs.  I've used them for most of my exploration missions, among other things, and they're invaluable.

If you have any questions, comments, or whatever, feel free to contact [Merovech](https://github.com/Merovech) on GitHub.  If you find any bugs, feel free to open an issue here!