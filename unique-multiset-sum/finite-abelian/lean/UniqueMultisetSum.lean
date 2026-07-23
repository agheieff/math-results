import Mathlib

namespace UniqueMultisetSum

open scoped BigOperators

/-- The all-ones vector is the unique size-`n` multiplicity vector preserving the sum. -/
def HasUniqueMultisetSums {n : ℕ} {G : Type*} [AddCommMonoid G]
    (g : Fin n → G) : Prop :=
  ∀ m : Fin n → ℕ,
    (∑ i, m i) = n →
    (∑ i, m i • g i) = ∑ i, g i →
    ∀ i, m i = 1

private lemma multiplicity_sum {n : ℕ} (U V : Finset (Fin n))
    (hdisj : Disjoint U V) (hle : U.card ≤ V.card) :
    (∑ x : Fin n, if x ∈ U then 2 else if x ∈ V then 0 else 1) +
        (1 + V.card - U.card) =
      n + 1 := by
  classical
  rw [Finset.sum_ite]
  simp only [Finset.sum_const, nsmul_eq_mul]
  rw [Finset.sum_ite
    (s := Finset.univ.filter fun x : Fin n => x ∉ U)]
  simp only [Finset.sum_const_zero, zero_add, Finset.sum_const, nsmul_eq_mul,
    mul_one]
  have hfilterU : (Finset.univ.filter fun x : Fin n => x ∈ U) = U := by
    ext x
    simp
  have hcomp :
      (Finset.univ.filter fun x : Fin n => x ∉ U).filter (fun x => x ∉ V) =
        Finset.univ \ (U ∪ V) := by
    ext x
    simp
  have hcard_union : (U ∪ V).card = U.card + V.card :=
    Finset.card_union_of_disjoint hdisj
  have hcard_le : U.card + V.card ≤ n := by
    rw [← hcard_union]
    simpa using Finset.card_le_univ (U ∪ V)
  rw [hfilterU, hcomp, Finset.card_sdiff, Finset.inter_univ, hcard_union,
    Finset.card_univ, Fintype.card_fin]
  change U.card * 2 + (n - (U.card + V.card)) +
      (1 + V.card - U.card) = n + 1
  omega

private lemma weighted_nonbase {n : ℕ} {G : Type*} [AddCommGroup G]
    (g : Fin n → G) (U V : Finset (Fin n)) (hdisj : Disjoint U V) :
    (∑ x : Fin n, (if x ∈ U then 2 else if x ∈ V then 0 else 1) • g x) =
      (∑ x, g x) + (∑ x ∈ U, g x) - ∑ x ∈ V, g x := by
  classical
  have hU : (∑ x ∈ U, g x) = ∑ x, if x ∈ U then g x else 0 := by
    simp
  have hV : (∑ x ∈ V, g x) = ∑ x, if x ∈ V then g x else 0 := by
    simp
  rw [hU, hV, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun x _ => ?_
  by_cases hxU : x ∈ U
  · have hxV : x ∉ V := fun hxV => Finset.disjoint_left.mp hdisj hxU hxV
    simp [hxU, hxV, two_nsmul]
  · by_cases hxV : x ∈ V
    · simp [hxU, hxV]
    · simp [hxU, hxV]

private lemma sum_sdiff_eq_sum_sdiff {α G : Type*} [DecidableEq α]
    [AddCommGroup G] (f : α → G) (A B : Finset α)
    (h : (∑ x ∈ A, f x) = ∑ x ∈ B, f x) :
    (∑ x ∈ A \ B, f x) = ∑ x ∈ B \ A, f x := by
  have hA := Finset.sum_sdiff
    (f := f) (Finset.inter_subset_left : A ∩ B ⊆ A)
  have hB := Finset.sum_sdiff
    (f := f) (Finset.inter_subset_right : A ∩ B ⊆ B)
  have hdiffA : A \ (A ∩ B) = A \ B := by
    ext x
    simp
  have hdiffB : B \ (A ∩ B) = B \ A := by
    ext x
    simp [and_comm]
  rw [hdiffA] at hA
  rw [hdiffB] at hB
  rw [← hA, ← hB] at h
  exact add_right_cancel h

/-- Every basepoint-difference family has injective subset sums. -/
theorem basepoint_subsetSum_injective {n : ℕ} {G : Type*} [AddCommGroup G]
    (g : Fin (n + 1) → G) (huniq : HasUniqueMultisetSums g) :
    Function.Injective fun A : Finset (Fin n) =>
      ∑ i ∈ A, (g i.castSucc - g (Fin.last n)) := by
  classical
  have forward :
      ∀ A B : Finset (Fin n),
        (∑ i ∈ A, (g i.castSucc - g (Fin.last n))) =
          ∑ i ∈ B, (g i.castSucc - g (Fin.last n)) →
        (A \ B).card ≤ (B \ A).card →
        A = B := by
    intro A B hAB hle
    let U := A \ B
    let V := B \ A
    change U.card ≤ V.card at hle
    have hdisj : Disjoint U V := by
      rw [Finset.disjoint_left]
      intro x hxU hxV
      simp only [U, V, Finset.mem_sdiff] at hxU hxV
      exact hxU.2 hxV.1
    have hUV :
        (∑ i ∈ U, (g i.castSucc - g (Fin.last n))) =
          ∑ i ∈ V, (g i.castSucc - g (Fin.last n)) :=
      sum_sdiff_eq_sum_sdiff
        (fun i : Fin n => g i.castSucc - g (Fin.last n)) A B hAB
    let m : Fin (n + 1) → ℕ := fun i =>
      match finSuccEquivLast i with
      | none => 1 + V.card - U.card
      | some x => if x ∈ U then 2 else if x ∈ V then 0 else 1
    have hm_sum : (∑ i, m i) = n + 1 := by
      rw [Fin.sum_univ_castSucc]
      simpa only [m, finSuccEquivLast_castSucc, finSuccEquivLast_last] using
        multiplicity_sum U V hdisj hle
    have hbalance :
        (∑ i ∈ U, g i.castSucc) - (∑ i ∈ V, g i.castSucc) +
            (V.card - U.card) • g (Fin.last n) =
          0 := by
      simp only [Finset.sum_sub_distrib, Finset.sum_const] at hUV
      have hcard : V.card = U.card + (V.card - U.card) := by omega
      rw [hcard, add_nsmul] at hUV
      have hx :
          (∑ i ∈ U, g i.castSucc) =
            (∑ i ∈ V, g i.castSucc) -
              (V.card - U.card) • g (Fin.last n) := calc
        (∑ i ∈ U, g i.castSucc) =
            ((∑ i ∈ U, g i.castSucc) - U.card • g (Fin.last n)) +
              U.card • g (Fin.last n) :=
          (sub_add_cancel _ _).symm
        _ = ((∑ i ∈ V, g i.castSucc) -
              (U.card • g (Fin.last n) +
                (V.card - U.card) • g (Fin.last n))) +
              U.card • g (Fin.last n) := by rw [hUV]
        _ = (∑ i ∈ V, g i.castSucc) -
              (V.card - U.card) • g (Fin.last n) := by abel
      rw [hx]
      abel
    have hm_weight : (∑ i, m i • g i) = ∑ i, g i := by
      rw [Fin.sum_univ_castSucc, Fin.sum_univ_castSucc]
      simp only [m, finSuccEquivLast_castSucc, finSuccEquivLast_last]
      rw [weighted_nonbase (fun i : Fin n => g i.castSucc) U V hdisj]
      have hcoeff :
          1 + V.card - U.card = 1 + (V.card - U.card) := by omega
      rw [hcoeff, add_nsmul]
      simp only [one_nsmul]
      calc
        (∑ x : Fin n, g x.castSucc) + (∑ i ∈ U, g i.castSucc) -
              (∑ i ∈ V, g i.castSucc) +
              (g (Fin.last n) +
                (V.card - U.card) • g (Fin.last n)) =
            (∑ x : Fin n, g x.castSucc) + g (Fin.last n) +
              ((∑ i ∈ U, g i.castSucc) - (∑ i ∈ V, g i.castSucc) +
                (V.card - U.card) • g (Fin.last n)) := by abel
        _ = (∑ x : Fin n, g x.castSucc) + g (Fin.last n) := by
          rw [hbalance, add_zero]
    have hm_one := huniq m hm_sum hm_weight
    have hUempty : U = ∅ := by
      rw [← Finset.not_nonempty_iff_eq_empty]
      rintro ⟨x, hxU⟩
      have hx := hm_one x.castSucc
      simp only [m, finSuccEquivLast_castSucc] at hx
      simp [hxU] at hx
    have hVempty : V = ∅ := by
      rw [← Finset.not_nonempty_iff_eq_empty]
      rintro ⟨x, hxV⟩
      have hxU : x ∉ U := Finset.disjoint_right.mp hdisj hxV
      have hx := hm_one x.castSucc
      simp only [m, finSuccEquivLast_castSucc] at hx
      simp [hxU, hxV] at hx
    apply Finset.Subset.antisymm
    · exact Finset.sdiff_eq_empty_iff_subset.mp hUempty
    · exact Finset.sdiff_eq_empty_iff_subset.mp hVempty
  intro A B hAB
  rcases le_total (A \ B).card (B \ A).card with hle | hle
  · exact forward A B hAB hle
  · exact (forward B A hAB.symm hle).symm

/-- A size-`n + 1` unique-multiset-sum family forces `|G| ≥ 2^n`. -/
theorem group_card_lower_bound {n : ℕ} {G : Type*}
    [AddCommGroup G] [Fintype G] (g : Fin (n + 1) → G)
    (huniq : HasUniqueMultisetSums g) :
    2 ^ n ≤ Fintype.card G := by
  have hinj := basepoint_subsetSum_injective g huniq
  simpa using Fintype.card_le_of_injective
    (fun A : Finset (Fin n) =>
      ∑ i ∈ A, (g i.castSucc - g (Fin.last n))) hinj

end UniqueMultisetSum
