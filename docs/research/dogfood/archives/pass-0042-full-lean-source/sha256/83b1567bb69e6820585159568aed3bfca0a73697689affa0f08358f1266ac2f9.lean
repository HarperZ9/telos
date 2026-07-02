-- Frozen interface for the Problem 4(b) counterexample: the definitions
-- (`Defs`) and the immutable theorem statements (`Theorems`), plus the
-- `Proofs/` modules that discharge them. `Discharge`/`Solution` are added once
-- all frozen statements are proved. See `PROGRESS.md` and `BLUEPRINT.md`.
import Prob4b.Defs
import Prob4b.Theorems
import Prob4b.Proofs.RingModel.Basic
import Prob4b.Proofs.RingModel.Normal
import Prob4b.Proofs.EasyDirection.Basic
import Prob4b.Proofs.Triple.Membership
import Prob4b.Proofs.Triple.Basic
import Prob4b.Proofs.Idealization.Basic
import Prob4b.Proofs.Module.Basic
import Prob4b.Proofs.Amplify.Carrier
import Prob4b.Proofs.Amplify.NotQuasiCoherent
import Prob4b.Proofs.Amplify.FiniteConductor
import Prob4b.Proofs.Amplify.Basic
import Prob4b.Discharge
import Prob4b.Solution
