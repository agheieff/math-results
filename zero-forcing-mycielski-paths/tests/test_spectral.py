from zero_forcing_mycielski_paths.spectral import verify_spectral_parameters


def test_generic_spectral_parameters() -> None:
    for order in range(4, 80):
        if order != 5:
            verify_spectral_parameters(order)
