import os
import random


def init_seed(seed: int | None = None) -> int:
    """Initialize the global random seed for deterministic obfuscation."""
    if seed is not None and not isinstance(seed, int):
        msg = f"seed must be an integer, got {type(seed).__name__}"
        raise TypeError(msg)
    if seed is None:
        env_seed = os.environ.get("POF_SEED")
        if env_seed is not None:
            try:
                seed = int(env_seed)
            except ValueError:
                msg = f"POF_SEED environment variable must be an integer, got: {env_seed!r}"  # noqa: E501
                raise ValueError(msg) from None
            random.seed(seed)
        else:
            seed = random.randrange(2**32)
            random.seed(seed)
    else:
        random.seed(seed)
    return seed
