from __future__ import print_function
from turtle import back

from numpy import empty
from game import sd_peers, sd_spots, sd_domain_num, sd_domain, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy
from collections import deque

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem)

        # Implementation of backtracking search.

        # Propagate initial decisions, i.e. assign values to all cells initially in the problem
        conflict = self.propagate_initial_decisions(domains)

        if conflict:
            return {}

        # Initialize data structures
        empty_cells = [(i, j) for (i, j), domain in domains.items() if len(domain) > 1]
        decisions_stack = deque()

        # while the list of empty cells has elements to be assigned
        while len(empty_cells) > 0:

            # take a decision
            decision = self.take_decision(domains, empty_cells, decisions_stack)

            # propagate it
            conflict = self.propagate(domains, decision, empty_cells)

            # if it caused a conflict, backtrack
            if conflict:
                backtracked, domains, empty_cells = self.backtrack(decisions_stack)
                if not backtracked:
                    return {}

        return domains

    def propagate_initial_decisions(self, domains):
        decisions = []
        for (i, j), domain in domains.items():
            if len(domain) == 1:
                decisions.append((i, j, domain[0]))

        for decision in decisions:
            conflict = self.propagate(domains, decision)
            if conflict:
                return True

        return False

    def propagate(self, domains, decision, empty_cells=None):
        to_propagate = deque()
        to_propagate.append(decision)

        while len(to_propagate) > 0:
            i, j, value = to_propagate.popleft()
            related_cells = self.related_cells(i, j)

            for (x, y) in related_cells:
                if value in domains[(x, y)]:
                    domains[(x, y)].remove(value)

                    domain_size = len(domains[(x, y)])

                    if domain_size == 1:
                        if empty_cells is not None:
                            empty_cells.remove((x, y))
                        propagated_val = domains[(x, y)][0]
                        to_propagate.append((x, y, propagated_val))

                    elif domain_size == 0:
                        return True

        return False

    def related_cells(self, i, j):
        result = []

        sd_domain = list(range(0, SD_SIZE))

        # same row
        for jprime in sd_domain:
            if jprime == j:
                continue
            result.append((i, jprime))

        # same column
        for iprime in sd_domain:
            if iprime == i:
                continue
            result.append((iprime, j))

        # same grid quadrant
        (i_quadrant, j_quadrant) = (i // SD_DIM, j // SD_DIM)
        for di in range(SD_DIM):
            for dj in range(SD_DIM):
                if (SD_DIM * i_quadrant + di, SD_DIM * j_quadrant + dj) == (i, j):
                    continue
                result.append((SD_DIM * i_quadrant + di, SD_DIM * j_quadrant + dj))

        return result

    def take_decision(self, domains, empty_cells, decisions_stack):
        # select cell with minimum length of domain
        min_domain_cell = empty_cells[0]
        min_domain_len = len(domains[min_domain_cell])
        for cell in empty_cells:
            if len(domains[cell]) < min_domain_len:
                min_domain_cell = cell
                min_domain_len = len(domains[min_domain_cell])

        # print('Before taking decision:', domains[min_domain_cell])

        # assign it the first value in its domain
        value = domains[min_domain_cell][0]
        remaining_domain = domains[min_domain_cell][1:]
        domains[min_domain_cell] = [value]

        ## push the decision into the stack
        # copy the current state of the domains
        domains_state = copy.deepcopy(domains)
        # update the copied domains to be ready for an eventual backtracking
        domains_state[min_domain_cell] = remaining_domain
        # copy the current empty_cells
        empty_cells_state = copy.deepcopy(empty_cells)
        # and push the assigned cell and relative backtracking domains in the stack
        decisions_stack.append((min_domain_cell, domains_state, empty_cells_state))

        # print('I just took decision: ', min_domain_cell, ' ', domains[min_domain_cell], ' ', remaining_domain)

        # remove it from the list of empty cells
        empty_cells.remove(min_domain_cell)

        return (*min_domain_cell, value)

    def backtrack(self, decisions_stack):
        backtracked = False
        while len(decisions_stack) > 0 and not backtracked:
            cell, last_decision_domains, last_decision_empty_cells = decisions_stack.popleft()
            if len(last_decision_domains[cell]) == 0:
                # the last decision doesn't have other options anymore, it's a conflict itself, backtrack higher up the tree
                continue
            else:
                new_domains = last_decision_domains
                new_empty_cells = last_decision_empty_cells
                backtracked = True

        return backtracked, new_domains, new_empty_cells

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains

        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
