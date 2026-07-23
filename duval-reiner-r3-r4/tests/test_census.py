from duval_reiner_r3_r4.census import run_census


def test_exact_six_vertex_census() -> None:
    result = run_census()
    assert result["isomorphism_classes"] == 2136
    indices = result["indices"]
    assert isinstance(indices, dict)
    assert indices["3"]["exact_status_counts"] == {  # type: ignore[index]
        "equality": 510,
        "strict": 1626,
    }
    assert indices["4"]["exact_status_counts"] == {  # type: ignore[index]
        "equality": 315,
        "strict": 1821,
    }
    assert indices["3"]["numerical_screen_candidates"] == 0  # type: ignore[index]
    assert indices["4"]["numerical_screen_candidates"] == 0  # type: ignore[index]
