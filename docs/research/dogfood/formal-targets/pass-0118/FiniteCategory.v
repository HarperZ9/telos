(* Pass 0118 generated target. Source artifact only; not executed here. *)
Inductive A : Type := a0 | a1.
Inductive B : Type := b0 | b1.
Inductive C : Type := c0 | c1.
Inductive D : Type := d0 | d1.

Definition idA (x : A) : A :=
  match x with a0 => a0 | a1 => a1 end.

Definition idB (x : B) : B :=
  match x with b0 => b0 | b1 => b1 end.

Definition f (x : A) : B :=
  match x with a0 => b0 | a1 => b1 end.

Definition g (x : B) : C :=
  match x with b0 => c1 | b1 => c0 end.

Definition h (x : C) : D :=
  match x with c0 => d0 | c1 => d1 end.

Definition comp {X Y Z : Type} (g0 : Y -> Z) (f0 : X -> Y) : X -> Z :=
  fun x => g0 (f0 x).

Theorem idB_comp_f_eq_f : forall x : A, comp idB f x = f x.
Proof. intros x; destruct x; reflexivity. Qed.

Theorem f_comp_idA_eq_f : forall x : A, comp f idA x = f x.
Proof. intros x; destruct x; reflexivity. Qed.

Theorem h_comp_g_comp_f_assoc :
  forall x : A, comp h (comp g f) x = comp (comp h g) f x.
Proof. intros x; destruct x; reflexivity. Qed.
