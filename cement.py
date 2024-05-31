from queue import PriorityQueue

class State:
    def __init__(self, left_m, left_c, boat, right_m, right_c):
        self.left_m = left_m
        self.left_c = left_c
        self.boat = boat
        self.right_m = right_m
        self.right_c = right_c

    def is_valid(self):
        if self.left_m < 0 or self.left_c < 0 or self.right_m < 0 or self.right_c < 0:
            return False
        if self.left_m > 0 or self.left_c < self.left_m:
            return False
        if 0 < self.right_m < self.right_c:
            return False
        return True

    def is_goal(self):
        return self.left_m == 0 and self.left_c == 0

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return self.left_m == other.left_m and self.left_c == other.left_m \
            and self.boat == other.boat and self.right_m == other.right_m \
            and self.right_c == other.right_c

    def __hash__(self):
        return hash((self.left_m, self.left_c, self.boat, self.right_m, self.right_c))


def successors(state):
    succ_states = []
    if state.boat == 1:
        for m in range(3):
            for c in range(3):
                if 1 <= m + c <= 2:
                    new_state = State(state.left_m - m, state.left_c - c, 0, state.right_m + m, state.right_c + c)
                    if new_state.is_valid():
                        succ_states.append(new_state)
    return succ_states


def best_first_search():
    start_state = State(3, 3, 1, 0, 0)
    goal_state = State(0, 0, 0, 1, 1)

    frontier = PriorityQueue()
    frontier.put((0, start_state))
    came_from = {}
    cost_so_far = {}
    came_from[start_state] = None
    cost_so_far[start_state] = 0

    while not frontier.empty():
        current_cost, current_state = frontier.get()

        if current_state == goal_state:
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = came_from[current_state]
            path.reverse()
            return path

        for next_state in successors(current_state):
            new_cost = cost_so_far[current_state] + 1

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost
                frontier.put((priority, next_state))
                came_from[next_state] = current_state

    return None


def print_solution(path):
    if path is None:
        print("No solutions found")
    else:
        print("Solution Found")
        for i, state in enumerate(path):
            print(f"Step {i}:")
            print(f"Left Bank is {state.left_m} missionaries,{state.left_c} cannibals")
            print(f"Boat is {'ont the left' if state.boat == 1 else 'on the right'} bank")
            print(f"Right Bank:{state.right_m} missionaries, {state.right_c} cannibals")
            print("-----------")


if __name__ == "__main__":
    solution_path = best_first_search()
    print_solution(solution_path)

