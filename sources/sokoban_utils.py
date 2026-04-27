from sources import deadlock_utils as deadlock
from scipy.optimize import linear_sum_assignment

TIME_OUT = 1800

class state:
    def __init__(self, board, state_parent, list_check_point,mode):
        self.board = board
        self.state_parent = state_parent
        self.cost = 0 if state_parent is None else state_parent.cost + 1
        self.heuristic = None
        self.check_points = list_check_point
        self.mode = mode

    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.board)
            current = current.state_parent
        path.reverse()
        return path

    ''' Tính giá trị heuristic cho trạng thái hiện tại '''
    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic is None:
            # Hungarian matching cho tổng khoảng cách Manhattan
            if self.mode == 2:
                h = compute_hungarian_heuristic(list_boxes, self.check_points)
            else:
                h = 0
                for box in list_boxes:
                    # Manhattan gần nhất theo từng hộp (nhanh, nhưng không tối ưu ghép toàn cục).
                    min_dist = min(
                        abs(box[0] - cp[0]) + abs(box[1] - cp[1])
                        for cp in self.check_points
                    )
                    h += min_dist

            if self.mode == 1 or self.mode == 2:
                self.heuristic = self.cost + h  # A*: f(n) = g(n) + h(n)
            else:
                self.heuristic = h  # Greedy: f(n) = h(n)
        return self.heuristic
    
    def __gt__(self, other):
        if self.compute_heuristic() > other.compute_heuristic():
            return True
        else:
            return False
        
    def __lt__(self, other):
        if self.compute_heuristic() < other.compute_heuristic():
            return True
        else :
            return False


def check_win(board, list_check_point):
    for p in list_check_point:
        if board[p[0]][p[1]] != '$':
            return False
    return True

# ===== Tiện ích chung =====

def assign_matrix(board):
    return [list(row) for row in board]

def find_position_player(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '@':
                return (x,y)
    return (-1,-1)  # Không tìm thấy người chơi

# ===== Xử lí deadlock =====

def is_box_on_check_point(box, list_check_point):
    return deadlock.is_box_on_check_point(box, list_check_point)

def is_wall_cell(board, x, y):
    return deadlock.is_wall_cell(board, x, y)

def check_in_corner(board, x, y, list_check_point):
    return deadlock.check_in_corner(board, x, y, list_check_point)

def find_boxes_position(board):
    return deadlock.find_boxes_position(board)

def is_box_can_be_moved(board, box_position):
    return deadlock.is_box_can_be_moved(board, box_position)

def is_all_boxes_stuck(board, list_check_point):
    return deadlock.is_all_boxes_stuck(board, list_check_point)

def is_board_can_not_win(board, list_check_point):
    return deadlock.is_board_can_not_win(board, list_check_point)

# ===== Di chuyển trạng thái =====

def get_next_pos(board, cur_pos):
    x, y = cur_pos
    rows, cols = len(board), len(board[0])
    list_can_move = []

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < rows and 0 <= ny < cols):
            continue

        value = board[nx][ny]
        if value == ' ' or value == '%':
            list_can_move.append((nx, ny))
            continue

        if value == '$':
            bx, by = nx + dx, ny + dy
            if 0 <= bx < rows and 0 <= by < cols:
                next_pos_box = board[bx][by]
                if next_pos_box != '#' and next_pos_box != '$':
                    list_can_move.append((nx, ny))

    return list_can_move

def move(board, next_pos, cur_pos, list_check_point):
    new_board = assign_matrix(board)
    nx, ny = next_pos
    cx, cy = cur_pos

    # Nếu đẩy hộp thì cập nhật vị trí hộp
    if new_board[nx][ny] == '$':
        dx, dy = nx - cx, ny - cy
        new_board[nx + dx][ny + dy] = '$'

    # Cập nhật vị trí người chơi
    new_board[nx][ny] = '@'
    new_board[cx][cy] = ' '

    # Không để mất điểm đích nếu ô checkpoint rỗng thì đặt lại '%'
    for px, py in list_check_point:
        if new_board[px][py] == ' ':
            new_board[px][py] = '%'
    return new_board

# ===== Checkpoint =====

def find_list_check_point(board):
    list_check_point = []
    num_of_box = 0
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                num_of_box += 1
            elif board[x][y] == '%':
                list_check_point.append((x,y))
    if num_of_box < len(list_check_point):
        return [(-1,-1)]
    return list_check_point

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)


def compute_hungarian_heuristic(list_boxes, list_check_point):
    if len(list_boxes) == 0 or len(list_check_point) == 0:
        return 0

    # Cost matrix Manhattan: hàng là box, cột là checkpoint
    cost_matrix = [
        [abs(box[0] - cp[0]) + abs(box[1] - cp[1]) for cp in list_check_point]
        for box in list_boxes
    ]

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return sum(cost_matrix[r][c] for r, c in zip(row_ind, col_ind))