from zero_forcing_mycielski_paths.forts import exceptional_forts, verify_exceptional_forts
from zero_forcing_mycielski_paths.model import MycielskiPath


def test_exceptional_fort_certificates() -> None:
    for order in (3, 5):
        graph = MycielskiPath.build(order)
        verify_exceptional_forts(graph)
        assert tuple(map(len, exceptional_forts(graph))) == ((2, 2, 3) if order == 3 else (3, 3, 5))
