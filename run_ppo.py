import ppo
import torch

from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo

from lang import score_func, can_be_solution

from prompts import prompt, expansion_count, min_lines, check_fun

class GenNode:
    def __init__(self, text, gens):
        self.text = text
        self.gens = gens

montecarlo = MonteCarlo(Node(GenNode(prompt, [])))

def reinforce(gens, reward):
    rewards = [torch.tensor(reward)]
    for (query_tensors, response_tensors) in gens:
        ppo.trainer_step(query_tensors, response_tensors, rewards)

def generate_complete(text, montecarlo, gens):
    (text, gen) = ppo.generate(text)
    gens.append(gen)
    score = score_func(text)
    if score is not None:
        reinforce(gens, score)
        if score < 0:
            return None
        else:
            node = Node(GenNode(text, gens))
            if can_be_solution(text, min_lines, check_fun):
                montecarlo.solution = node
            return node
    else:
        return generate_complete(text, montecarlo, gens)

def child_finder(node, montecarlo):
    child = generate_complete(node.state.text, montecarlo, [])
    if child is None:
        node.update_win_value(-1)
    else:
        node.add_child(child)
        child.update_win_value(1)
        child.update_policy_value(1)

        retry_child = Node(GenNode(node.state.text, []))
        node.add_child(retry_child)
        retry_child.update_policy_value(0.2)

montecarlo.child_finder = child_finder

montecarlo.simulate(expansion_count)

if montecarlo.solution:
    print('CHOSEN SOLUTION')
    print(montecarlo.solution.state.text)

    node = montecarlo.solution
    while node:
        reinforce(node.state.gens, 10.0)
        node = node.parent

ppo.save()
