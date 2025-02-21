from typing import Any, Callable
import time

from graboidrfc.core.modules.utils.logger import logger as logging

def safecast(value, to_type, default=None):
    """Funzione per castare in modo sicuro"""
    try: return to_type(value)
    except (ValueError, TypeError):
        return default

def howMuchTimeDoesItTake(func: Callable) -> Callable:
    """ Decoratore che misura il tempo di esecuzione di una funzione"""
    
    def wrapped(*args, **kwargs) -> Any:
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        
        tot = str(end-start).split(".")   
        
        logging.debug(
            f"L'esecuzione della funzione \'{func.__name__}\' ha impiegato:", tot[0] + "." + tot[1][:4], "secondi."
        )
        
        return value
    
    return wrapped