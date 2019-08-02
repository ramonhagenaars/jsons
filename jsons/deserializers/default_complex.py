from typing import Dict


def default_complex_deserializer(obj: Dict[str, float], cls: type = complex, **kwargs) -> complex:
    print("Complex deserializer was called")
    print(f"Object is {type(obj)}: {obj}")
    print(f"Class is {type(cls)}: {cls}")
    real = obj.get('real')
    imag = obj.get('imag')
    return complex(real, imag)
