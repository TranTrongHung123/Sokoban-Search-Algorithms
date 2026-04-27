import os
import time
import io
import contextlib
import numpy as np
import matplotlib.pyplot as plt
from sources import greedy_search, astar_manhattan, astar_hungarian

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.path.join(BASE_DIR, "data", "maps")
CP_DIR = os.path.join(BASE_DIR, "data", "checkpoints")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def format_row(row):
    for i, cell in enumerate(row):
        if cell == "1":
            row[i] = "#"
        elif cell == "p":
            row[i] = "@"
        elif cell == "b":
            row[i] = "$"
        elif cell == "c":
            row[i] = "%"


def load_board(level):
    board = np.loadtxt(os.path.join(MAP_DIR, f"{level}.txt"), dtype=str, delimiter=",")
    for row in board:
        format_row(row)
    return board.tolist()


def load_checkpoints(level):
    cp = np.loadtxt(os.path.join(CP_DIR, f"{level}.txt"), dtype=int, delimiter=",")
    if cp.ndim == 1:
        return [cp.tolist()]
    return cp.tolist()


levels = list(range(1, 31))
greedy_steps = []
greedy_states = []
greedy_times = []

manhattan_steps = []
manhattan_states = []
manhattan_times = []

hungarian_steps = []
hungarian_states = []
hungarian_times = []

print("Đang chạy 3 thuật toán trên 30 level...")
for level in levels:
    print("-" * 60)
    print(f"Level {level}/30")
    board = load_board(level)
    cp = load_checkpoints(level)

    silent_buffer = io.StringIO()
    suppress_logs = contextlib.redirect_stdout(silent_buffer)

    # Greedy Search
    t0 = time.time()
    with suppress_logs:
        g_path, g_states = greedy_search.greedy_search(board, cp)
    g_time = time.time() - t0
    greedy_steps.append(len(g_path) if g_path else 0)
    greedy_states.append(g_states)
    greedy_times.append(g_time)

    # A* Manhattan
    t0 = time.time()
    with suppress_logs:
        m_path, m_states = astar_manhattan.astar_search_manhattan(board, cp)
    m_time = time.time() - t0
    manhattan_steps.append(len(m_path) if m_path else 0)
    manhattan_states.append(m_states)
    manhattan_times.append(m_time)

    # A* Hungarian
    t0 = time.time()
    with suppress_logs:
        h_path, h_states = astar_hungarian.astar_search_hungarian(board, cp)
    h_time = time.time() - t0
    hungarian_steps.append(len(h_path) if h_path else 0)
    hungarian_states.append(h_states)
    hungarian_times.append(h_time)
    print(f"Greedy Search  -> steps: {greedy_steps[-1]}, states: {g_states}, time: {g_time:.3f}s")
    print(f"A* Manhattan   -> steps: {manhattan_steps[-1]}, states: {m_states}, time: {m_time:.3f}s")
    print(f"A* Hungarian   -> steps: {hungarian_steps[-1]}, states: {h_states}, time: {h_time:.3f}s")


# Figure 1: Số bước để giải
plt.figure(figsize=(12, 6))
plt.plot(
    levels,
    greedy_steps,
    marker='^',
    label='Greedy Search',
    linewidth=2.8,
    linestyle='-',
    alpha=0.9,
    markersize=8,
    markeredgecolor='black',
    markeredgewidth=0.8,
    zorder=3,
)
plt.plot(
    levels,
    manhattan_steps,
    marker='s',
    label='A* Manhattan',
    linewidth=5.0,
    linestyle='-',
    alpha=0.75,
    markersize=9,
    markerfacecolor='none',
    markeredgecolor='black',
    markeredgewidth=1.2,
    zorder=1,
)
plt.plot(
    levels,
    hungarian_steps,
    marker='D',
    label='A* Hungarian',
    linewidth=3.0,
    linestyle='-',
    alpha=0.95,
    markersize=8,
    markeredgecolor='black',
    markeredgewidth=0.8,
    zorder=4,
)
plt.xlabel('Level', fontsize=12)
plt.ylabel('Số bước cần để giải', fontsize=12)
plt.title('So sánh số bước cần để giải (càng thấp càng tốt)', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(levels)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "chart_steps.png"), dpi=150)

# Figure 2: Số lượng trạng thái
plt.figure(figsize=(12, 6))
plt.plot(
    levels,
    greedy_states,
    marker='^',
    label='Greedy Search',
    linewidth=2.8,
    linestyle='-',
    alpha=0.9,
    markersize=8,
    markeredgecolor='black',
    markeredgewidth=0.8,
    zorder=3,
)
plt.plot(
    levels,
    manhattan_states,
    marker='s',
    label='A* Manhattan',
    linewidth=5.0,
    linestyle='-',
    alpha=0.75,
    markersize=9,
    markerfacecolor='none',
    markeredgecolor='black',
    markeredgewidth=1.2,
    zorder=1,
)
plt.plot(
    levels,
    hungarian_states,
    marker='D',
    label='A* Hungarian',
    linewidth=3.0,
    linestyle='-',
    alpha=0.95,
    markersize=8,
    markeredgecolor='black',
    markeredgewidth=0.8,
    zorder=4,
)
plt.xlabel('Level', fontsize=12)
plt.ylabel('Số lượng trạng thái đã duyệt', fontsize=12)
plt.title('So sánh số lượng trạng thái đã duyệt (càng thấp càng tốt)', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(levels)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "chart_states.png"), dpi=150)

# Figure 3: Thời gian chạy
plt.figure(figsize=(12, 6))
plt.plot(
    levels,
    greedy_times,
    marker='^',
    label='Greedy Search',
    linewidth=2.8,
    linestyle='-',
    alpha=0.9,
    markersize=8,
    markeredgecolor='black',
    markeredgewidth=0.8,
    zorder=3,
)
plt.plot(
    levels,
    manhattan_times,
    marker='s',
    label='A* Manhattan',
    linewidth=5.0,
    linestyle='-',
    alpha=0.75,
    markersize=9,
    markerfacecolor='none',
    markeredgecolor='black',
    markeredgewidth=1.2,
    zorder=1,
)
plt.plot(
    levels,
    hungarian_times,
    marker='D',
    label='A* Hungarian',
    linewidth=3.0,
    linestyle='-',
    alpha=0.95,
    markersize=8,
    markeredgecolor='black',
    markeredgewidth=0.8,
    zorder=4,
)
plt.xlabel('Level', fontsize=12)
plt.ylabel('Thời gian chạy (giây)', fontsize=12)
plt.title('So sánh thời gian chạy (càng thấp càng tốt)', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(levels)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "chart_time.png"), dpi=150)

# Hiển thị tất cả biểu đồ
plt.show()

print("\nĐã hiển thị 3 biểu đồ")