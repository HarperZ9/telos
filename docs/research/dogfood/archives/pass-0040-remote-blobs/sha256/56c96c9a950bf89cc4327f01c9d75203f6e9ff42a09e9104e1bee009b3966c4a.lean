/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Defs

/-!
# The easy direction: quasi-coherent implies finite-conductor

This file proves the general fact (true for *every* commutative ring, with no
dependence on the construction `B`/`M`/`R`) that a quasi-coherent ring is
finite-conductor. The annihilator clause is shared verbatim between the two
predicates; the pairwise principal-intersection clause of `FiniteConductor` is
the `n = 2` instance of the arbitrary-finite clause of `QuasiCoherent`, obtained
by instantiating the family `f := ![x, y] : Fin 2 → S` and rewriting the finite
`iInf` over `Fin 2` as a binary `⊓`.

The declaration `quasiCoherent_imp_finiteConductor_proof` has *exactly* the type
of the frozen `Prob4b.quasiCoherent_imp_finiteConductor`, so the no-drift gate
`@quasiCoherent_imp_finiteConductor = @quasiCoherent_imp_finiteConductor_proof`
holds by `rfl`.
-/

namespace Prob4b

/-- **The easy direction.** Every quasi-coherent ring is finite-conductor: the
annihilator condition is shared, and the pairwise principal-intersection
condition is the `n = 2` instance of the arbitrary-finite one. -/
theorem quasiCoherent_imp_finiteConductor_proof {S : Type*} [CommRing S]
    (h : QuasiCoherent S) : FiniteConductor S := by
  refine ⟨h.1, fun x y => ?_⟩
  have hpair := h.2 2 ![x, y]
  have heq : (⨅ i, Ideal.span {(![x, y] : Fin 2 → S) i})
      = Ideal.span {x} ⊓ Ideal.span {y} := by
    apply le_antisymm
    · exact le_inf (iInf_le _ 0) (iInf_le _ 1)
    · refine le_iInf fun i => ?_
      fin_cases i
      · exact inf_le_left
      · exact inf_le_right
  rwa [heq] at hpair

end Prob4b
