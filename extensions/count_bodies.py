"""
count_bodies.py - basic example of a processor that counts the bodies in 
systems.

Four methods need to be implemented:
    GetName(): returns the display name of the processor
    Initialize(): Intializes the processor however it needs
    ProcessSystem(): Processes a system that is passed form the main loop
    Completed(): Run when the main loop is complete to output results
    
See processor_base.py for details.

`system` passed to ProcessSystem is an Elite.SpanshTools.Model.StarSystem
instance. Access any property directly — pythonnet maps .NET properties to
Python attributes.
"""
from processor_base import ProcessorBase
import log

class BodyCounter(ProcessorBase):
    def __init__(self):
        super().__init__()
        self.__body_count = 0

    def GetName(self) -> str:
        return "Body Counter Example"

    def Initialize(self, log_verbose: bool = False) -> None:
        super().Initialize(log_verbose)
        self.__body_count = 0

    def ProcessSystem(self, system) -> None:
        self.__body_count += system.BodyCount

    def Completed(self) -> None:
        log.writeln(f"Total bodies found: {self.__body_count}")
