from lang import lang

if lang == 'Dafny':
    proof_marker = 'ensures'
elif lang == 'Coq':
    proof_marker = 'Qed'
else:
    proof_marker = None

if proof_marker:
    check_proof = lambda v: proof_marker in v
else:
    check_proof = lambda v: True

problem_fact = (f"""### Spec: In {lang}, write a factorial function and prove that the factorial is always strictly positive.
{'''### Hint: Use a plain function, NOT a function method.
''' if lang=='Dafny' else ''
}{'''### Hint: Don't forget to import the Arith module.
### Hint: use `Nat.lt_0_1` in the base case of the proof.
### Hint: use `Nat.lt_lt_add_r` in the inductive case of the proof.
''' if lang=='Coq' else ''
}### {lang}:""",
                500, None, 5, check_proof)
problem_opt0 = (f"""### Spec: In {lang}, write an ADT for arithmetic expressions comprising constants, variables and binary addition. Then write an evaluator taking an expression and an environment (a function that takes a variable name and returns a number) and returns the number resulting from evaluation. Then write an optimizer tha takes an expression and returns an expression with all additions by 0 removed. Then prove that the optimizer preserves the semantics as defined by the evaluation function.
{'''### Hint: Recall that in Dafny, pattern match takes the form
match e
case Foo(x, y) => 1
case Bar(x) => 2
case _ => 3
''' if lang=='Dafny' else ''
}### Hint: In the optimizer, recursively optimize the sub-expressions.
{'''### Hint: For the proof, just do a simple pattern match (match not if) and call the lemma recursively without adding asserts.
''' if lang=='Dafny' else ''
}{'''### Hint: You can import the `string` datatype with the line `Require Import Coq.Strings.String.`
### Hint: Use Fixpoint instead of Definition for recursive functions.
### Hint: If you do induction on `e` with sub-expressions `e1` and `e2`, the two inductive hypotheses are called `IHe1` and `IHe2`.
### Hint: For the inductive case of the proof, `eauto using PeanoNat.Nat.add_0_r` might be useful (`Require Arith` in the imports).
### Hint: You can also rewrite backwards: `rewrite <- H`.
''' if lang=='Coq' else ''
}### {lang}:""",
                1000, None, 22, check_proof)

# HumanEvalX, Problem 3
relates_to = "==>" # can do <==> for harder problem
problem_below0_dafny = ("""
### Hint: In Dafny, the result is assigned `result := true` and `return` takes no arguments.
### Hint: Remember to have an invariant related running balance and the sum.
### Hint: Call the lemma sum_plus after you add one ops element to maintain the invariant.
```Dafny
function sum(s: seq<int>, n: nat): int
    requires n <= |s|
{
    if |s| == 0 || n == 0 then
        0
    else
        s[0] + sum(s[1..], n-1)
}

lemma sum_plus(s: seq<int>, i: nat)
    requires i < |s|
    ensures sum(s, i) + s[i] == sum(s, i+1)
{
}

method below_zero(ops: seq<int>) returns (result: bool)
/*
You're given a list of deposit and withdrawal operations on a bank account that starts with
zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
at that point function should return true. Otherwise it should return false.
- assert !below_zero([1, 2, 3])
- assert below_zero([1, 2, -4, 5])
*/
    ensures result """+relates_to+""" exists n: nat :: n <= |ops| && sum(ops, n) < 0
{
""", 1000, None, 5, check_proof)


# Set the right-hand side to the selected problem.
(prompt, max_new_tokens, expansion_count, min_lines, check_fun) = problem_below0_dafny
