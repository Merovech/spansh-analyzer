"""
count_population.py - basic example of a processor that counts the population 
in systems, then provides an average (removing systems with 0 population).

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
from processor_base import ProcessorBase

class CountPopulation(ProcessorBase):
    def __init__(self):
        self.__total_population = 0
        self.__total_populated_systems = 0

    def GetName(self) -> str:
        return "Population Counter Example"

    def Initialize(self) -> None:
        self.__total_populated_systems = 0

    def ProcessSystem(self, system) -> None:
        if system.Population > 0:
            self.__total_population += system.Population
            self.__total_populated_systems += 1

    def Completed(self) -> None:
        print(f"Total population found: {self.__total_population}")
        print(f"Average per populated system: {self.__total_population // self.__total_populated_systems}")

