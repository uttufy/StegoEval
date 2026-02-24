from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Any, Optional

class StegoEvalConfig(BaseModel):
    model_config = ConfigDict(extra='ignore')

    # Dataset configuration
    dataset_path: str = "./data"
    dataset_limit: Union[int, None] = None
    
    # Payload configuration
    payload: str = "STEGOEVAL_SECRET"
    payload_sizes: List[int] = [10, 100, 1000, 5000]
    
    # Run configuration
    run_name: str = "benchmark"
    combo_attacks: bool = False
    
    # Capacity test configuration
    capacity: Dict[str, Any] = {}
    
    # Dictionary of Attack Category -> Dict[Attack Name -> List/Dict of Params]
    attacks: Dict[str, Dict[str, Union[List[Any], Dict[str, Any]]]] = {}
