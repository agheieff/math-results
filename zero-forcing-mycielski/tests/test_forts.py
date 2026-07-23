from zero_forcing_mycielski.forts import q6_fort_certificate


def test_q6_fort_certificate() -> None:
    result = q6_fort_certificate()
    assert result.fort_count == 16
    assert result.candidate_count == 81
    assert len(result.survivors_after_first_two_families) == 6
    assert not result.final_survivors
