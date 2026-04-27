import numpy as np
import os
import pygame
from sources import greedy_search
from sources import astar_manhattan
from sources import astar_hungarian

# Cài đặt cấu hình thư mục gốc để đọc file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_board = os.path.join(BASE_DIR, 'data', 'maps')
path_checkpoint = os.path.join(BASE_DIR, 'data', 'checkpoints')

# Đọc toàn bộ map từ thư mục maps
def get_boards():
    list_boards = []

    list_file = [file for file in os.listdir(path_board) if file.endswith(".txt")]
    list_file.sort(key=lambda x: int(x.split('.')[0]))

    for file in list_file:
        file_path = os.path.join(path_board, file)
        board = get_board(file_path)
        # print(file)
        list_boards.append(board)

    return list_boards

# Đọc toàn bộ checkpoint từ thư mục checkpoints
def get_check_points():
    list_check_point = []

    list_file = [file for file in os.listdir(path_checkpoint) if file.endswith(".txt")]
    list_file.sort(key=lambda x: int(x.split('.')[0]))
    for file in list_file:
        file_path = os.path.join(path_checkpoint, file)
        check_point = get_pair(file_path)
        
        if check_point.ndim == 1:
            check_point = [check_point.tolist()]
        else:
            check_point = check_point.tolist()
            
        list_check_point.append(check_point)

    return list_check_point

# Chuyển đổi ký tự từ file txt sang các ký tự dùng trong thuật toán
def format_row(row):
	for i in range(len(row)):
		if row[i] == '1':
			row[i] = '#'  # tường
		elif row[i] == 'p':
			row[i] = '@'  # người chơi
		elif row[i] == 'b':
			row[i] = '$'  # thùng
		elif row[i] == 'c':
			row[i] = '%'  # ô đích

# Đọc 1 file map txt và định dạng lại các ký tự và trả về ma trận
def get_board(path):
	result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
	for row in result:
		format_row(row)
	return result

# Đọc file txt chứa checkpoint và trả về mảng số nguyên
def get_pair(path):
	result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
	return result

# Khai báo và nạp dữ liệu map, checkpoint
maps = get_boards()
check_points = get_check_points()


# khởi tạo pygame và tài nguyên cho game
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)

# Nạp hình ảnh cho game
assets_path = os.path.join(BASE_DIR, 'assets')
font_path = os.path.join(assets_path, 'game_font.ttf')
player = pygame.image.load(os.path.join(assets_path, 'player.png'))
player = pygame.transform.scale(player, (32, 32))
wall = pygame.image.load(os.path.join(assets_path, 'wall.png'))
box = pygame.image.load(os.path.join(assets_path, 'box.png'))
point = pygame.image.load(os.path.join(assets_path, 'point.png'))
point = pygame.transform.scale(point, (32, 32))
space = pygame.image.load(os.path.join(assets_path, 'space.png'))
space = pygame.transform.scale(space, (32, 32))
arrow_left = pygame.image.load(os.path.join(assets_path, 'arrow_left.png'))
arrow_right = pygame.image.load(os.path.join(assets_path, 'arrow_right.png'))
init_background = pygame.image.load(os.path.join(assets_path, 'init_background.png'))
init_background = pygame.transform.scale(init_background, screen.get_size())
loading_background = pygame.image.load(os.path.join(assets_path, 'loading_background.png'))
loading_background = pygame.transform.scale(loading_background, screen.get_size())
notfound_background = pygame.image.load(os.path.join(assets_path, 'notfound_background.png'))
notfound_background = pygame.transform.scale(notfound_background, screen.get_size())
found_background = pygame.image.load(os.path.join(assets_path, 'found_background.png'))
found_background = pygame.transform.scale(found_background, screen.get_size())

# Vẽ bản đồ cho màn hình chơi
def renderMap(board):
	width = len(board[0])
	height = len(board)
	indent = (640 - width * 32) / 2.0
	for i in range(height):
		for j in range(width):
			screen.blit(space, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '#':
				screen.blit(wall, (j * 32 + indent, i * 32 + 250))  # tường
			if board[i][j] == '$':
				screen.blit(box, (j * 32 + indent, i * 32 + 250))  # thùng
			if board[i][j] == '%':
				screen.blit(point, (j * 32 + indent, i * 32 + 250))  # ô đích
			if board[i][j] == '@':
				screen.blit(player, (j * 32 + indent, i * 32 + 250))  # người chơi


''' Biến trạng thái chính của game '''
# Level hiện tại
mapNumber = 0
# Thuật toán đang được chọn
algorithm = "Greedy Search"
ALGORITHMS = ["Greedy Search", "A* Manhattan", "A* Hungarian"]
# Các scene: init, loading, executing, playing, end
sceneState = "init"
loading = False


''' Màn hình menu chính '''
# Vẽ scene khởi đầu
def initGame(map):
	titleSize = pygame.font.Font(font_path, 60)
	titleText = titleSize.render('Sokoban', True, WHITE)
	titleRect = titleText.get_rect(center=(320, 80))
	screen.blit(titleText, titleRect)

	desSize = pygame.font.Font(font_path, 20)
	desText = desSize.render('Select map', True, WHITE)
	desRect = desText.get_rect(center=(320, 140))
	screen.blit(desText, desRect)

	mapSize = pygame.font.Font(font_path, 30)
	mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
	mapRect = mapText.get_rect(center=(320, 200))
	screen.blit(mapText, mapRect)

	screen.blit(arrow_left, (246, 188))
	screen.blit(arrow_right, (370, 188))

	algorithmSize = pygame.font.Font(font_path, 30)
	algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
	algorithmRect = algorithmText.get_rect(center=(320, 600))
	screen.blit(algorithmText, algorithmRect)
	renderMap(map)


''' Màn hình đang tính toán '''
# Vẽ màn hình hiển thị trong lúc chờ AI giải bài
def loadingGame():
	screen.blit(loading_background, (0, 0))

# Vẽ màn hình chiến thắng khi AI đã hoàn thành việc biểu diễn đường đi
def foundGame(map):
	screen.blit(found_background, (0, 0))

	font = pygame.font.Font(font_path, 20)
	text = font.render('Press Enter to continue.', True, WHITE)
	text_rect = text.get_rect(center=(320, 600))
	screen.blit(text, text_rect)

	renderMap(map)

# Vẽ màn hình thất bại khi AI báo 'Not Found' hoặc 'Timeout'
def notfoundGame():
	screen.blit(notfound_background, (0, 0))

	font = pygame.font.Font(font_path, 20)
	text = font.render('Press Enter to continue.', True, WHITE)
	text_rect = text.get_rect(center=(320, 600))
	screen.blit(text, text_rect)


''' Vòng lặp chính của game '''
def sokoban():
	running = True
	global sceneState
	global loading
	global algorithm
	global list_board
	global mapNumber
	stateLength = 0
	currentState = 0
	found = True

	while running:
		screen.blit(init_background, (0, 0))
		if sceneState == "init":
			# Hiển thị map đang chọn
			initGame(maps[mapNumber])

		if sceneState == "executing":
			# Lấy checkpoint theo map hiện tại
			list_check_point = check_points[mapNumber]
			print("Lv " + str(mapNumber + 1) + ":")
			# Chạy thuật toán đã chọn
			if algorithm == "Greedy Search":
				print("Greedy Search")
				list_board = greedy_search.greedy_search(maps[mapNumber], list_check_point)
			elif algorithm == "A* Manhattan":
				print("A* Manhattan")
				list_board = astar_manhattan.astar_search_manhattan(maps[mapNumber], list_check_point)
			else:
				print("A* Hungarian")
				list_board = astar_hungarian.astar_search_hungarian(maps[mapNumber], list_check_point)
			if list_board[0]:
				sceneState = "playing"
				stateLength = len(list_board[0])
				currentState = 0
			else:
				sceneState = "end"
				found = False

		if sceneState == "loading":
			loadingGame()
			sceneState = "executing"

		if sceneState == "end":
			if found:
				foundGame(list_board[0][stateLength - 1])
			else:
				notfoundGame()

		if sceneState == "playing":
			clock.tick(2)
			renderMap(list_board[0][currentState])
			currentState = currentState + 1
			if currentState == stateLength:
				sceneState = "end"
				print("Step solve = " + str(stateLength))
				print("States Explored = " + str(list_board[1]))
				found = True

		# Xử lý phím bấm
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				# Mũi tên trái/phải để đổi level
				if event.key == pygame.K_RIGHT and sceneState == "init":
					if mapNumber < len(maps) - 1:
						mapNumber = mapNumber + 1
				if event.key == pygame.K_LEFT and sceneState == "init":
					if mapNumber > 0:
						mapNumber = mapNumber - 1

				# Enter để bắt đầu hoặc quay lại menu
				if event.key == pygame.K_RETURN:
					if sceneState == "init":
						sceneState = "loading"
					if sceneState == "end":
						sceneState = "init"
						
				# Space để đổi thuật toán
				if event.key == pygame.K_SPACE and sceneState == "init":
					current_index = ALGORITHMS.index(algorithm)
					algorithm = ALGORITHMS[(current_index + 1) % len(ALGORITHMS)]
		pygame.display.flip()
	pygame.quit()

def main():
	sokoban()

if __name__ == "__main__":
	main()