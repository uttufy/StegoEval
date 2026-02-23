from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Any

class StegoEvalConfig(BaseModel):
    model_config = ConfigDict(extra='ignore')

    dataset_path: str = "./data"
    dataset_limit: Union[int, None] = None
    payload: str = "STEGOEVAL_SECRET"
    
    # Dictionary of Attack Category -> Dict[Attack Name -> List/Dict of Params]
    attacks: Dict[str, Dict[str, Union[List[Any], Dict[str, Any]]]] = {}
