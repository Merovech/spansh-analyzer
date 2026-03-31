from abc import ABC, abstractmethod

"""
Base class for all processors.

"""
class ProcessorBase(ABC):

    
    @abstractmethod
    def GetName(self) -> str:
        """Returns the display name of the processor.""" 
        pass
    

    @abstractmethod
    def Initialize(self, log_verbose: bool = False) -> None: 
        """Returns the display name of the processor.
        
        This is a good place to initialize any collections, state, etc. that
        needs to be done at runtime.

        Parameters
        ----------
        system : `Elite.SpanshTools.Model.StarSystem`
            A star system from a Spansh dump, with a fully defined model.
        
        log_verbose : `bool`
            If true, verbose logging was requested.  Defaults to false.
        """ 
        pass

    @abstractmethod
    def ProcessSystem(self, system, log_verbose: bool = False) -> None: 
        """Process a `StarSystem`

        Each `StarSystem` provided by the main loop is sent through the discovered
        processors, one at a time.

        Parameters
        ----------
        system : `Elite.SpanshTools.Model.StarSystem`
            A star system from a Spansh dump, with a fully defined model.

        log_verbose : `bool`
            If true, verbose logging was requested.  Defaults to false.
        """
        pass

    @abstractmethod
    def Completed(self, log_verbose: bool = False) -> None: 
        """Called when the main loop finishes the last item in the file.
        
        This is the place for any final calculations and output.  The processor is
        responsible for printing the output to the console when this method is called.

        Parameters
        ----------
        log_verbose : `bool`
            If true, verbose logging was requested.  Defaults to false.
        """
        pass
