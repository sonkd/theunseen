---
title: Base rate fallacy
front: "Vì sao một xét nghiệm 'chính xác 99%' vẫn có thể sai gần như luôn khi bạn nhận kết quả dương tính?"
back: "Base rate fallacy là xu hướng bỏ qua tỷ lệ nền (tần suất thật của một hiện tượng trong toàn bộ dân số) và chỉ dựa vào thông tin cụ thể trước mắt, khiến ta ước lượng sai xác suất thực sự."
level: 2
categories: [fallacy]
links: [conjunction-fallacy, availability-heuristic, insensitivity-to-sample-size]
refs: ['https://en.wikipedia.org/wiki/Base_rate_fallacy']
strategy: "Trước khi tin vào một kết quả cụ thể (xét nghiệm, cảnh báo gian lận, điểm tín dụng), luôn hỏi: tỷ lệ nền của hiện tượng này trong toàn bộ dân số là bao nhiêu, trước khi diễn giải con số riêng lẻ đó."
image: /assets/stuff/base-rate-fallacy.png
published: true
---

Base rate fallacy xảy ra khi ta đánh giá xác suất của một sự kiện chỉ dựa trên thông tin cụ thể vừa nhận được, mà quên mất tần suất nền — tỷ lệ hiện tượng đó vốn xảy ra thường xuyên thế nào trong toàn bộ dân số. Não bộ ưu tiên câu chuyện sống động trước mắt hơn con số thống kê trừu tượng, dù con số đó mới là thứ quyết định xác suất thật.

Ví dụ kinh điển nhất là bài toán xét nghiệm y tế: một bệnh hiếm gặp chỉ ảnh hưởng 1/1.000 người, xét nghiệm có độ chính xác 99%. Nếu bạn nhận kết quả dương tính, trực giác nói xác suất mắc bệnh là 99%. Nhưng tính đúng theo định lý Bayes, vì số người khỏe mạnh đông hơn rất nhiều, số ca dương tính giả (false positive) trong nhóm khỏe mạnh thực ra áp đảo số ca dương tính thật — xác suất mắc bệnh thực tế chỉ khoảng 9%. Daniel Kahneman và Amos Tversky đã chứng minh hiện tượng này rõ nhất qua "bài toán luật sư — kỹ sư" (1973): khi biết một nhóm gồm 70 kỹ sư và 30 luật sư, người tham gia vẫn đoán nghề nghiệp của một người dựa gần như hoàn toàn vào mô tả tính cách (ví dụ "thích sửa đồ điện, ít giao tiếp"), bỏ qua hẳn tỷ lệ 70/30 đã được cho biết trước.

Trong fintech, base rate fallacy xuất hiện rõ nhất ở hệ thống cảnh báo gian lận. Nếu tỷ lệ giao dịch gian lận thực tế chỉ là 0,1% trên tổng giao dịch, một mô hình phát hiện gian lận có độ chính xác 95% vẫn sẽ tạo ra rất nhiều cảnh báo sai — vì số giao dịch hợp lệ đông áp đảo. Đội vận hành dễ mất niềm tin vào hệ thống hoặc mệt mỏi vì "báo động giả" (alert fatigue) nếu không hiểu gốc rễ là tỷ lệ nền quá thấp, chứ không phải mô hình kém. Tương tự, khi đánh giá rủi ro tín dụng, nhìn vào một hồ sơ vay có vài dấu hiệu "giống" khách hàng từng vỡ nợ không đủ để kết luận rủi ro cao, nếu tỷ lệ vỡ nợ nền trong nhóm đó vốn đã rất thấp.

Base rate fallacy có quan hệ gần với conjunction-fallacy — cả hai đều là hệ quả của representativeness heuristic, khi ta đánh giá xác suất dựa trên mức độ "giống mẫu hình" thay vì tính toán thật. Nó cũng liên quan tới availability-heuristic, vì thông tin cụ thể, sống động luôn dễ nhớ và dễ chi phối phán đoán hơn con số thống kê khô khan. Một biến thể gần gũi khác là insensitivity-to-sample-size, khi ta phớt lờ luôn cả kích thước mẫu chứ không chỉ tỷ lệ nền.
