# Sokoban - Search Algorithms

## Mô tả
Dự án mô phỏng trò chơi Sokoban và so sánh 3 thuật toán tìm kiếm:
- Greedy Search  
- A* Manhattan  
- A* Hungarian  

Có 2 chế độ chạy:
- `main.py`: giao diện Pygame chơi và xem AI giải  
- `benchmark.py`: chạy 30 level và vẽ biểu đồ so sánh  

---

## Yêu cầu
- Python 3.9+
- Thư viện:
  - numpy
  - pygame
  - matplotlib
  - scipy

---

## Cài đặt

> Chạy từng lệnh một

```bash
py -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
pip install numpy pygame matplotlib scipy
```

---

## Chạy giao diện game

```bash
python main.py
```

### Phím tắt trong game
- ← / → : đổi level  
- Space : đổi thuật toán  
- Enter : bắt đầu / chạy lại  

---

## Chạy benchmark

```bash
python benchmark.py
```

### Kết quả
- In thông tin từng level ra terminal  
- Lưu biểu đồ vào thư mục `figures/`:
  - `chart_steps.png`
  - `chart_states.png`
  - `chart_time.png`

---

## Lưu ý
Dữ liệu để mẫu dùng để test:
- Level: `data/maps/`  
- Checkpoint: `data/checkpoints/`  