# crucible report: Dogfood Pass 0105 Reaction Mass-Conservation Receipt

## Summary

- thesis_id: `483ccbf50e02b9fe`
- thesis_seal: `483ccbf50e02b9fe04aa5df98d62b43f53255b453c162dcf9dfc5a29dfb33e20`
- assessment_seal: `fd386bf90524d14491f6c0ddf67e1f799a9d9190732e608a0af5a523b76320e8`
- counts: MATCH 9 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0105 created a ReactionMassConservationReceipt/v1 artifact with status REACTION_MASS_CONSERVATION_RECEIPT_MATCH, sha256 0d2e36ea03ec3c1685fbaf31c3139cdb709a23c7bbf4167407c637c93d85573a, and seal 44d61ff374c7ac528a4c837c31e8470e5ba539c19164bb098918c436f86ca26d. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 binds AI4Science pass 0104 and reaction A -> B. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 records symbolic derivative total 0 for invariant A+B. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 numerical probe records 97 grid points, max_exact_invariant_drift 0.0, and max_euler_invariant_drift 4.440892098500626e-16. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 negative fixture open_system_degradation breaks invariant with status DRIFT_EXPECTED. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 records law candidate closed_first_order_reaction_total_mass_invariant with status LAW_CANDIDATE. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 flagship receipts for Forum, Index, and Telos all have MATCH status. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 records unsupported_claim_count 0 and current_promoted_natural_laws length 0. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0105 composer sha256 is c390d38e2f2c02bc4fd2312ab4fb12ef5858c3953aa4579dd2379d293c4aaef0, packet sha256 is 2cf9822ab75f7e574d96d60f2fffe5fee48c142efab0f97213a95b20ef965ce3, brief sha256 is b816f77d92418c8acbc5d322556b419c5792a2fa7ff404d38ba25ccc0be1bcb8, steelman sha256 is ff83258e83d58012bada6a21b5abaa4a382480c38724c86cb284face5b11c950, test sha256 is 5a9069a015b8b1a029432cb2bf8c7b2608cffd2b9f8f1f16ba09d35ea4a08d39, and tool_receipts sha256 is 207c5d7bb9c59c1269596c7f9541e4d6fbf19fc27ca954a1d806845db83a5674 with test_receipt status MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0105 created a ReactionMassConservationReceipt/v1 artifact with status REACTION_MASS_CONSERVATION_RECEIPT_MATCH, sha256 0d2e36ea03ec3c1685fbaf31c3139cdb709a23c7bbf4167407c637c93d85573a, and seal 44d61ff374c7ac528a4c837c31e8470e5ba539c19164bb098918c436f86ca26d. | artifact-review | schema=ReactionMassConservationReceipt/v1; status=REACTION_MASS_CONSERVATION_RECEIPT_MATCH; sha256=0d2e36ea03ec3c1685fbaf31c3139cdb709a23c7bbf4167407c637c93d85573a; seal=44d61ff374c7ac528a4c837c31e8470e5ba539c19164bb098918c436f86ca26d |
| Pass 0105 binds AI4Science pass 0104 and reaction A -> B. | artifact-review | source_bindings={'ai4science_pass': '0104', 'source_packet': 'AI4ScienceClaimToExperimentReceipt/v1'}; reaction={'equation': 'A -> B', 'rate_law': 'dA/dt=-kA; dB/dt=kA', 'stoichiometry': {'A': -1, 'B': 1}, 'system_boundary': 'closed'} |
| Pass 0105 records symbolic derivative total 0 for invariant A+B. | artifact-review | proof={'derivation': 'd(A+B)/dt=dA/dt+dB/dt=-kA+kA', 'invariant': 'A+B', 'symbolic_derivative_total': '0'} |
| Pass 0105 numerical probe records 97 grid points, max_exact_invariant_drift 0.0, and max_euler_invariant_drift 4.440892098500626e-16. | artifact-review | grid_points=97; max_exact=0.0; max_euler=4.440892098500626e-16 |
| Pass 0105 negative fixture open_system_degradation breaks invariant with status DRIFT_EXPECTED. | artifact-review | negative_fixture={'breaks_invariant': True, 'fixture_id': 'open_system_degradation', 'max_total_drift': 0.2959392161530001, 'status': 'DRIFT_EXPECTED'} |
| Pass 0105 records law candidate closed_first_order_reaction_total_mass_invariant with status LAW_CANDIDATE. | artifact-review | law_candidate={'name': 'closed_first_order_reaction_total_mass_invariant', 'scope': 'closed two-species first-order conversion A -> B with stoichiometry -1,+1', 'status': 'LAW_CANDIDATE'} |
| Pass 0105 flagship receipts for Forum, Index, and Telos all have MATCH status. | artifact-review | forum=MATCH; index=MATCH; telos=MATCH |
| Pass 0105 records unsupported_claim_count 0 and current_promoted_natural_laws length 0. | artifact-review | unsupported_claim_count=0; natural_law_count=0 |
| Pass 0105 composer sha256 is c390d38e2f2c02bc4fd2312ab4fb12ef5858c3953aa4579dd2379d293c4aaef0, packet sha256 is 2cf9822ab75f7e574d96d60f2fffe5fee48c142efab0f97213a95b20ef965ce3, brief sha256 is b816f77d92418c8acbc5d322556b419c5792a2fa7ff404d38ba25ccc0be1bcb8, steelman sha256 is ff83258e83d58012bada6a21b5abaa4a382480c38724c86cb284face5b11c950, test sha256 is 5a9069a015b8b1a029432cb2bf8c7b2608cffd2b9f8f1f16ba09d35ea4a08d39, and tool_receipts sha256 is 207c5d7bb9c59c1269596c7f9541e4d6fbf19fc27ca954a1d806845db83a5674 with test_receipt status MATCH. | artifact-review | composer_sha256=c390d38e2f2c02bc4fd2312ab4fb12ef5858c3953aa4579dd2379d293c4aaef0; packet_sha256=2cf9822ab75f7e574d96d60f2fffe5fee48c142efab0f97213a95b20ef965ce3; brief_sha256=b816f77d92418c8acbc5d322556b419c5792a2fa7ff404d38ba25ccc0be1bcb8; steelman_sha256=ff83258e83d58012bada6a21b5abaa4a382480c38724c86cb284face5b11c950; test_sha256=5a9069a015b8b1a029432cb2bf8c7b2608cffd2b9f8f1f16ba09d35ea4a08d39; tool_receipts_sha256=207c5d7bb9c59c1269596c7f9541e4d6fbf19fc27ca954a1d806845db83a5674; test_status=MATCH; compose_status=MATCH |
