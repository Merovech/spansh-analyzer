from abc import ABC, abstractmethod

class ProcessorBase(ABC):
    """
    Base class for all processors.

    """
    def __init__(self):
        self.log_verbose = False

    def Initialize(self, log_verbose: bool = False) -> None: 
        """Initializes the processor.
        
        This is a good place to initialize any collections, state, etc. that
        needs to be done at runtime.

        Parameters
        ----------
        log_verbose : `bool`
            If true, verbose logging was requested.  Defaults to false.
        """ 
        self.log_verbose = log_verbose

    @abstractmethod
    def GetName(self) -> str:
        """Returns the display name of the processor.""" 
        pass
    
    @abstractmethod
    def ProcessSystem(self, system) -> None: 
        """Process a `StarSystem`

        Each `StarSystem` provided by the main loop is sent through the discovered
        processors, one at a time.

        Parameters
        ----------
        system : `Elite.SpanshTools.Model.StarSystem`
            A star system from a Spansh dump, with a fully defined model.
        """
        pass

    @abstractmethod
    def Completed(self) -> None: 
        """Called when the main loop finishes the last item in the file.
        
        This is the place for any final calculations and output.  The processor is
        responsible for printing the output to the console when this method is called.
        """
        pass
