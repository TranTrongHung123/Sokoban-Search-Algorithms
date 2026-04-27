# ===== Kiểm tra hộp có nằm trên checkpoint không =====

def is_box_on_check_point(box, list_check_point):
	return any(box[0] == check_point[0] and box[1] == check_point[1] for check_point in list_check_point)

# ===== Kiểm tra tường và góc =====

# Kiểm tra xem ô có phải là tường không
def is_wall_cell(board, x, y):
	if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
		return True
	return board[x][y] == '#'

# Deadlock ở góc khi hộp bị kẹt ở góc tạo bởi 2 tường vuông góc nhau
def check_in_corner(board, x, y, list_check_point):
	if is_box_on_check_point((x, y), list_check_point):
		return False

	top_wall = is_wall_cell(board, x - 1, y)
	bottom_wall = is_wall_cell(board, x + 1, y)
	left_wall = is_wall_cell(board, x, y - 1)
	right_wall = is_wall_cell(board, x, y + 1)

	if (top_wall or bottom_wall) and (left_wall or right_wall):
		return True

	return False

# ===== Vị trí các hộp và khả năng di chuyển của hộp =====

# Tìm vị trí của tất cả hộp trên bản đồ
def find_boxes_position(board):
	return [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == '$']

# Kiểm tra xem hộp có thể được đẩy đi hay không
def is_box_can_be_moved(board, box_position):
	x, y = box_position

	# Hàm phụ kiểm tra xem ô có khoảng trống cho người chơi đứng đẩy không
	def is_clear(px, py):
		if is_wall_cell(board, px, py):
			return False
		return board[px][py] in (' ', '%', '@')

	# Hàm phụ kiểm tra xem ô đích có cho phép hộp trượt vào không
	def is_pushable(tx, ty):
		if is_wall_cell(board, tx, ty):
			return False
		return board[tx][ty] != '$'

	# Trục ngang: Người có thể đứng bên trái đẩy sang phải hoặc đứng bên phải đẩy sang trái
	if (is_clear(x, y - 1) and is_pushable(x, y + 1)) or \
	   (is_clear(x, y + 1) and is_pushable(x, y - 1)):
		return True

	# Trục dọc: Người có thể đứng bên trên đẩy xuống dưới hoặc đứng bên dưới đẩy lên trên
	if (is_clear(x - 1, y) and is_pushable(x + 1, y)) or \
	   (is_clear(x + 1, y) and is_pushable(x - 1, y)):
		return True

	return False

# ===== Deadlock tổng hợp =====

# Deadlock khi mọi hộp đều không thể đẩy đi và không có hộp nào đã ở đích
def is_all_boxes_stuck(board, list_check_point):
	for box in find_boxes_position(board):
		if is_box_on_check_point(box, list_check_point):
			return False
		if is_box_can_be_moved(board, box):
			return False
	return True

# Quét qua các hộp, nếu có hộp nào vào góc chết mà không phải đích thì cắt nhánh
def is_board_can_not_win(board, list_check_point):
	for x, y in find_boxes_position(board):
		if check_in_corner(board, x, y, list_check_point):
			return True
	return False