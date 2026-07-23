from hadwiger_alpha2_chi7.criterion import (
    find_clique4_seagull_model,
    find_six_pair_cover_model,
    is_clique_model,
)
from hadwiger_alpha2_chi7.graph import Graph
from hadwiger_alpha2_chi7.verify import verification_record


def test_complement_translation_and_failed_pair_reduction() -> None:
    complement = Graph.complete_bipartite(6, 7)
    graph = complement.complement()

    assert complement.is_triangle_free()
    assert complement.matching_number() == 6
    assert graph.independence_number() == 2
    assert 13 - complement.matching_number() == 7
    assert graph.is_clique(range(6, 13))
    assert find_six_pair_cover_model(graph) is None


def test_seagull_criterion_produces_a_k7_model() -> None:
    complement = Graph.cycle(13)
    graph = complement.complement()

    model = find_clique4_seagull_model(complement)

    assert model is not None
    assert len(model) == 7
    assert sorted(len(branch_set) for branch_set in model) == [1, 1, 1, 1, 3, 3, 3]
    assert is_clique_model(graph, model)


def test_verification_record_is_stable_in_content() -> None:
    record = verification_record()

    assert record["counterexample_complement"] == "K6,7"
    assert record["counterexample_has_six_pair_cover_model"] is False
