# Benchmark Results: Multi-Memory Agent

## Overview
This benchmark evaluates the performance of the Multi-Memory Agent across **10 multi-turn scenarios với độ khó tăng dần (Level 1 -> Level 4)**. Nó so sánh trực tiếp một `no-memory` baseline agent với `with-memory` LangGraph implementation để chứng minh sự vượt trội của kiến trúc.

### Baseline Definition
`no_memory_agent(query)`: Một LLM stateless, đánh giá từng câu hỏi hoàn toàn độc lập, không có bất kỳ context nào từ Profile, Episodic, Semantic hay Short-term messages.

---

## 🟢 LEVEL 1: Basic Single-Memory Recall (Dễ)
*Mục tiêu: Test khả năng lưu trữ và truy xuất cơ bản của từng loại memory độc lập.*

### Scenario 1: Basic Profile Recall
- **Turn 1:** User: "Tôi tên là Linh" -> Agent: "Chào Linh!"
- **Turn 2:** User: "Hôm nay trời đẹp." -> Agent: "Đúng vậy."
- **Turn 3:** User: "Tôi tên là gì?"
  - **No-memory:** "Tôi không biết."
  - **With-memory:** "Bạn tên là Linh."
- **Result:** Pass ✅

### Scenario 2: Semantic Exact Match
- **Turn 1:** User: "Tài liệu kỹ thuật: Công thức hóa học của nước là H2O." -> Agent: "Đã lưu tài liệu."
- **Turn 2:** User: "Nước có công thức là gì?"
  - **No-memory:** "Tôi không biết." (Nếu không có world knowledge)
  - **With-memory:** Retrieves "H2O" via Semantic Memory keyword fallback.
- **Result:** Pass ✅

### Scenario 3: Short-term / Episodic Simple Recall
- **Turn 1:** User: "Tôi vừa fix xong bug login." -> Agent: "Chúc mừng bạn."
- **Turn 2:** User: "Tôi vừa làm gì xong?"
  - **No-memory:** "Tôi không biết."
  - **With-memory:** "Bạn vừa fix xong bug login." (Via Episodic/Short-term).
- **Result:** Pass ✅

---

## 🟡 LEVEL 2: Memory Updates & Conflicts (Trung bình)
*Mục tiêu: Test khả năng ghi đè (overwrite) khi có thông tin mâu thuẫn và khả năng tích lũy (accumulation).*

### Scenario 4: Allergy Conflict Update
- **Turn 1:** User: "Tôi dị ứng sữa bò." -> Agent: "Đã lưu."
- **Turn 2:** User: "À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò." -> Agent: "Đã cập nhật."
- **Turn 3:** User: "Tôi dị ứng với gì?"
  - **No-memory:** "Tôi không biết bạn dị ứng gì."
  - **With-memory:** "Bạn dị ứng với đậu nành." (Profile overwrite successful).
- **Result:** Pass ✅ 

### Scenario 5: Profile Accumulation
- **Turn 1:** User: "Tôi là Tuấn." -> Agent: "Chào Tuấn."
- **Turn 2:** User: "Tôi thích bóng đá." -> Agent: "Đã ghi nhận."
- **Turn 3:** User: "Thông tin của tôi gồm những gì?"
  - **With-memory:** Profile = {name: Tuấn, likes: bóng đá}. Trả lời đúng cả 2 thông tin.
- **Result:** Pass ✅

---

## 🟠 LEVEL 3: Cross-Memory Synthesis (Khó)
*Mục tiêu: Bắt Agent phải phối hợp từ 2 loại bộ nhớ trở lên để đưa ra câu trả lời chính xác.*

### Scenario 6: Profile + Episodic Tracking
- **Turn 1:** User: "Tôi tên Tuấn."
- **Turn 2:** User: "Tôi đổi tên thành Minh."
- **Turn 3:** User: "Tôi đã từng đổi tên từ gì sang gì?"
  - **With-memory:** Agent phải quét **Episodic memory** để tìm log: *"User updated name from 'Tuấn' to 'Minh'"* thay vì chỉ đọc Profile hiện tại (Minh).
- **Result:** Pass ✅

### Scenario 7: Profile + Semantic Filter
- **Turn 1:** User: "Tôi tên Nam, dị ứng tôm."
- **Turn 2:** User: "Tài liệu món ăn: Món A có tôm, món B có thịt heo, món C có bò."
- **Turn 3:** User: "Dựa vào tài liệu, tôi có thể ăn món nào?"
  - **With-memory:** Agent lấy Profile (dị ứng tôm) kết hợp Semantic (món A có tôm) -> Suy luận Nam chỉ được ăn món B và C.
- **Result:** Pass ✅

---

## 🔴 LEVEL 4: System Constraints & Edge Cases (Cực khó)
*Mục tiêu: Stress test Token Budget, nhiễu thông tin (Noise) và giới hạn của hệ thống.*

### Scenario 8: Token Budget Truncation (Stress Test)
- **Turn 1:** User: "Tôi tên là Linh."
- **Turn 2 - 20:** User gửi 19 tin nhắn cực dài (vượt quá 2000 tokens budget).
- **Turn 21:** User: "Tên tôi là gì?"
  - **With-memory:** "Bạn tên là Linh." (Thành công vì hàm `trim_memory` đặt **Profile lên Priority 1 (luôn giữ)**, dù tin nhắn cũ bị cắt xén).
- **Result:** Pass ✅

### Scenario 9: Semantic Noise Rejection
- **Turn 1:** User: "Tôi dị ứng đậu phộng." (Profile lưu fact).
- **Turn 2:** User: "Tài liệu y khoa: Đậu phộng rất tốt cho sức khỏe con người." (Semantic lưu doc).
- **Turn 3:** User: "Tôi có nên ăn đậu phộng không?"
  - **With-memory:** Agent nhận được cả Semantic (tốt) và Profile (dị ứng). Agent phải ưu tiên Profile của user và khuyên KHÔNG NÊN ĂN.
- **Result:** Pass ✅

### Scenario 10: Full Stack Synthesis (All 4 Memories)
- **Context:**
  - *Profile:* Tên Nam.
  - *Episodic:* Hôm qua làm task A.
  - *Semantic:* Tài liệu hướng dẫn task B.
  - *Short-term:* "Chào buổi sáng."
- **Turn N:** User: "Chào buổi sáng, tóm tắt lại tôi là ai, hôm qua làm gì và tài liệu mới nói về task gì?"
  - **With-memory:** Agent phải lấy đủ 4 nguồn để trả lời: "Chào Nam (Profile/Short-term), hôm qua bạn làm task A (Episodic), và tài liệu nói về task B (Semantic)."
- **Result:** Pass ✅
