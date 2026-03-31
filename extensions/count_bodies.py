"""
count_bodies.py - basic example of a processor that counts the bodies in 
systems.

Four methods need to be implemented:
    GetName(): returns the display name of the processor
    Initialize(): Intializes the processor however it needs
    ProcessSystem(): Processes a system that is passed form the main loop
    Completed(): Run when the main loop is complete to output results
    
See processorBase.py for details.

`system` passed to ProcessSystem is an Elite.SpanshTools.Model.StarSystem
instance. Access any property directly — pythonnet maps .NET properties to
Python attributes.
"""
from pathlib import Path
from processorBase import ProcessorBase

class ExampleCalculator(ProcessorBase):
    def __init__(self):
        self.__body_count = 0

    def GetName(self) -> str:
        return "Example Calculator"

    def Initialize(self) -> None:
        self.__body_count = 0

    def ProcessSystem(self, system) -> None:
        self.__body_count += system.BodyCount

    def Completed(self) -> None:
        print(f"Total bodies found: {self.__body_count}")
