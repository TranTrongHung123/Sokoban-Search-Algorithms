from sources import sokoban_utils as utils
import time
from queue import PriorityQueue


def greedy_search(board, list_check_point):
    start_time = time.time()

    if utils.check_win(board, list_check_point):
        print("Found win")
        return ([board], 1)
    
    start_state = utils.state(board, None, list_check_point, 0)
    visited = {utils.board_to_tuple(start_state.board)}

    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)

    while not heuristic_queue.empty():
        if time.time() - start_time > utils.TIME_OUT:
            return ([], len(visited))

        now_state = heuristic_queue.get()

        if utils.check_win(now_state.board, list_check_point):
            print("Found win")
            timesolve = time.time() - start_time
            print(f"Time solve = {timesolve}" )
            return (now_state.get_path(), len(visited))

        cur_pos = utils.find_position_player(now_state.board)
        list_can_move = utils.get_next_pos(now_state.board, cur_pos)
        for next_pos in list_can_move:
            new_board = utils.move(now_state.board, next_pos, cur_pos, list_check_point)
            board_key = utils.board_to_tuple(new_board)
            if board_key in visited:
                continue
            
            # Xử lí deadlock
            if utils.is_board_can_not_win(new_board, list_check_point):
                continue
            
            if utils.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = utils.state(new_board, now_state, list_check_point, 0)
            visited.add(board_key)
            heuristic_queue.put(new_state)

    print("Not Found")
    return ([], len(visited))