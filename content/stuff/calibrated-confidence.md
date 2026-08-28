---
title: Calibrated Confidence
front: Trong số những lần bạn nói chắc chắn 90%, thực tế bạn đúng bao nhiêu phần trăm?
back: Trạng thái mà mức độ tự tin phát biểu khớp với tần suất đúng thực tế — nói chắc 70% thì đúng khoảng 70% số lần.
level: 4
categories: [theory, mental-models]
tags: [probability, forecasting]
links: [overconfidence-effect, hard-easy-effect, illusion-of-validity, bayesian-updating]
refs: ['https://en.wikipedia.org/wiki/Calibration_(statistics)', 'https://en.wikipedia.org/wiki/Brier_score']
strategy: 'Ghi dự đoán kèm xác suất vào một sổ theo dõi, rồi ba tháng một lần chấm điểm theo nhóm xác suất để thấy mình lệch ở đâu.'
published: true
---

Calibrated confidence là sự khớp giữa mức chắc chắn ta phát biểu và tần suất đúng thực tế. Một người hiệu chỉnh tốt không phải người luôn đúng, mà là người mà khi gom tất cả các phán đoán được gán 70%, đúng khoảng bảy trên mười lần; gom các phán đoán 95%, sai chỉ khoảng một trên hai mươi. Đây là tiêu chuẩn khác hẳn với độ chính xác, và quan trọng hơn trong công việc ra quyết định dưới bất định.

Tách bạch hai khái niệm giúp làm rõ vấn đề. Độ nhạy bén là khả năng phân biệt trường hợp đúng và sai. Độ hiệu chỉnh là khả năng gắn con số xác suất trung thực lên phán đoán. Một người có thể rất nhạy nhưng hiệu chỉnh tệ vì luôn nói chắc quá mức, và ngược lại. Công cụ đo phổ biến là Brier score do Glenn Brier đề xuất năm 1950, tính bình phương sai lệch giữa xác suất dự báo và kết quả thực tế; điểm càng thấp càng tốt, và nó phạt cả việc quá tự tin lẫn việc né tránh bằng cách luôn nói năm mươi năm mươi.

Bằng chứng thực nghiệm cho thấy đa số người trưởng thành chưa qua huấn luyện đều quá tự tin, đặc biệt ở khoảng xác suất cao. Khi được yêu cầu đưa khoảng ước lượng chứa giá trị đúng với độ tin cậy 90%, tỷ lệ trúng thường chỉ quanh mức năm mươi tới sáu mươi phần trăm. Tin tốt là hiệu chỉnh cải thiện được: các cộng đồng dự báo, khí tượng viên và những nhóm được chấm điểm phản hồi đều đặn đạt mức hiệu chỉnh tốt hơn hẳn. Yếu tố quyết định là vòng phản hồi khép kín — dự đoán được ghi lại, kết quả được đối chiếu, sai lệch được nhìn thấy.

Cách áp dụng trong công việc sản phẩm khá cụ thể. Trước khi chạy thử nghiệm, mỗi bên liên quan viết ra dự đoán về mức tác động kèm khoảng tin cậy; sau khi có kết quả thì đối chiếu và lưu lại. Sau vài chu kỳ, đội sẽ biết ai lạc quan hệ thống và cần nới khoảng bao nhiêu cho lần sau. Lợi ích lớn nhất là tranh luận chuyển từ ai nói to hơn sang ai có thành tích hiệu chỉnh tốt hơn.

Hiệu chỉnh là liều thuốc trực tiếp cho overconfidence-effect, và bức tranh còn tinh tế hơn qua hard-easy-effect: người ta quá tự tin ở câu hỏi khó nhưng lại thiếu tự tin ở câu hỏi dễ. Nó cũng phơi bày illusion-of-validity, cảm giác chắc chắn sinh ra từ việc dữ liệu trông mạch lạc chứ không từ sức tiên đoán thật. Về cơ chế cập nhật, hiệu chỉnh tốt là điều kiện để bayesian-updating hoạt động đúng, vì niềm tin ban đầu sai lệch sẽ kéo theo mọi cập nhật sau đó.
