# 🤖 Chess AI - Game Playing Agent (BTL Nhập môn AI HK2 2024-2025)

## 🎯 Mục tiêu
Phát triển AI chơi cờ vua bằng các thuật toán tìm kiếm cổ điển (Minimax, Alpha-Beta), không sử dụng Machine Learning.

## 🧠 Giải thuật sử dụng
- Minimax search
- Alpha-Beta Pruning
- Static Evaluation Function (Heuristic)
- Agent cấp độ từ 1 → 3 theo độ sâu tìm kiếm

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

## ▶️ Cách chạy 
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
- Agent thắng 10/10 trước agent random bất kể trắng đen
- Hiển thị GUI thân thiện người dùng
- Chia cấp độ từ 1→3 (depth 1,3,5, thêm heuristic)

## 🎥 Video thuyết trình
[Link video YouTube hoặc Google Drive ở đây]

## 👨‍👩‍👧‍👦 Thành viên nhóm
| Họ tên | MSSV | Vai trò |
|--------|------|--------|
| Lê Vũ Thanh Hà | 2320007 | Board & Luật chơi |
| Đào Hữu Gia Huy | 2211158 | AI & Heuristic |
| Nguyễn Trung Hiếu | 2113357 | Kiểm thử & Thống kê |
| Lê Chánh Nguyên | 2111869 | GUI & Báo cáo & Kiểm soát đầu ra |
