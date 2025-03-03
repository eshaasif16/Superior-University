from collections import deque

def waterJugProblem(capacity1, capacity2, goal):
    queue =deque()
    visited=set()

    queue.append((0, 0))
    visited.add((0, 0))

    actions = []
    while queue:
        jug1, jug2 = queue.popleft()
        actions.append((jug1, jug2))
        
        if jug1 == goal or jug2 == goal:
            print("solulu found")
            for action in actions:
                print(action)
            
            print("1 fill Jug1")
            print("2 dill Jug2")
            print("3 empty Jug1")
            print("4 empty Jug2")
            print("5 pour Jug1 into Jug2 until its full")
            print("6 pour Jug2 into Jug1 until Jug1 its full")
            print("7 pour all water from Jug1 into Jug2")
            print("8 pour all water from Jug2 into Jug1")
            return True

        rules = [
            (capacity1, jug2),  
            (jug1, capacity2),  
            (0, jug2),          
            (jug1, 0),         
            (jug1 - min(jug1, capacity2 - jug2), jug2 + min(jug1, capacity2 - jug2)),  
            (jug1 + min(jug2, capacity1 - jug1), jug2 - min(jug2, capacity1 - jug1)),  
            (jug1 + jug2 if jug1 + jug2 <= capacity2 else jug1 - (capacity2 - jug2),
             jug2 + jug1 if jug2 + jug1 <= capacity2 else capacity2),  
            (jug1 + jug2 if jug1 + jug2 <= capacity1 else capacity1,
             jug2 - (capacity1 - jug1) if jug2 + jug1 > capacity1 else 0),  
        ]
        for state in rules:
            if state not in visited:
                visited.add(state)
                queue.append(state)

    print("solulu notfound")
    return False

jug1Capacity = 4
jug2Capacity = 3
target = 2

waterJugProblem(jug1Capacity,jug2Capacity,target)