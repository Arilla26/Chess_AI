# 🤖 Chess AI - Game Playing Agent (BTL Nhập môn AI HK2 2024-2025)

## 🎯 Mục tiêu
Phát triển AI chơi cờ vua bằng các thuật toán tìm kiếm cổ điển (Minimax, Alpha-Beta), không sử dụng Machine Learning.

## 🧠 Giải thuật sử dụng
- Minimax search
- Alpha-Beta Pruning
- Static Evaluation Function (Heuristic)
- Agent cấp độ từ 1 → 5 theo độ sâu tìm kiếm

## 🗂️ Cấu trúc thư mục
```
chess_ai_project/
├── board.py            # Luật chơi, bàn cờ, nước đi
├── agent.py            # Minimax & Alpha-Beta Agent
├── heuristic.py        # Hàm đánh giá trạng thái bàn cờ
├── random_agent.py     # Đối thủ random
├── test_agent.py       # Test AI vs Random
├── main.py             # Chơi console đơn giản
├── gui.py              # Giao diện pygame
├── assets/             # Ảnh quân cờ PNG
└── README.md
```

## ▶️ Cách chạy (Python 3.8+)
### 1. Cài đặt
```bash
pip install pygame
```

### 2. Chạy GUI để chơi với AI
```bash
python gui.py
```

### 3. Chạy test AI vs Random
```bash
python test_agent.py
```

## 📊 Kết quả
- Agent thắng 10/10 trước agent random
- Hiển thị GUI thân thiện người dùng
- Chia cấp độ từ 1→5 (depth từ 1→3, thêm heuristic)

## 🎥 Video thuyết trình
[Link video YouTube hoặc Google Drive ở đây]

## 👨‍👩‍👧‍👦 Thành viên nhóm
| Họ tên | MSSV | Vai trò |
|--------|------|--------|
| Nguyễn Văn A | 2012xxxxx | Board & Luật chơi |
| Trần Thị B | 2012xxxxx | AI & Heuristic |
| Lê Văn C | 2012xxxxx | Kiểm thử & Thống kê |
| Phạm Thị D | 2012xxxxx | GUI & Báo cáo |
