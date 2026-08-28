---
title: Signal Detection Theory
front: Khi hệ thống chống gian lận báo động sai quá nhiều, đó là do nó kém nhạy hay do ngưỡng đặt sai chỗ?
back: Khung lý thuyết tách khả năng phân biệt tín hiệu khỏi nhiễu ra khỏi ngưỡng quyết định — hai đại lượng độc lập thường bị gộp làm một khi đánh giá hiệu quả.
level: 5
categories: [theory]
tags: [perception, probability, risk]
links: [weber-fechner-law, base-rate-fallacy, zero-risk-bias, illusory-correlation]
refs: ['https://en.wikipedia.org/wiki/Detection_theory', 'https://en.wikipedia.org/wiki/Receiver_operating_characteristic']
strategy: 'Trước khi kết luận mô hình yếu, hãy vẽ đường ROC: nếu độ nhạy đủ tốt, vấn đề nằm ở ngưỡng và chi phí hai loại lỗi, không nằm ở mô hình.'
published: true
---

Signal detection theory là khung lý thuyết mô tả cách một người quan sát ra quyết định khi tín hiệu cần phát hiện luôn lẫn trong nhiễu. Nó được phát triển vào thập niên 1950 và 1960, xuất phát từ bài toán radar thời chiến rồi được David Green và John Swets đưa vào tâm lý học tri giác một cách hệ thống trong cuốn sách xuất bản năm 1966.

Đóng góp lớn nhất của nó là tách một thứ vốn bị gộp làm một. Trước đó, người ta đo khả năng phát hiện bằng một con số duy nhất là ngưỡng cảm giác. Lý thuyết này chỉ ra rằng mọi phán đoán có-không đều là tổ hợp của hai đại lượng độc lập. Thứ nhất là độ nhạy, ký hiệu quen thuộc là d prime, đo mức tách biệt giữa phân bố khi có tín hiệu và phân bố khi chỉ có nhiễu — đây là năng lực phân biệt thật. Thứ hai là tiêu chí quyết định, tức người quan sát đặt ngưỡng ở đâu để nói có — đây là lựa chọn chiến lược, phụ thuộc vào cái giá của từng loại sai.

Từ đó sinh ra bảng bốn ô đã trở thành ngôn ngữ chung của nhiều ngành: trúng, báo động giả, bỏ sót, và bác bỏ đúng. Điểm quan trọng là hai loại lỗi đánh đổi lẫn nhau. Hạ ngưỡng để bớt bỏ sót thì báo động giả tăng, và ngược lại; không có cách nào giảm cả hai nếu độ nhạy không đổi. Đường ROC vẽ toàn bộ đánh đổi này thành một đồ thị, và diện tích dưới đường cong trở thành thước đo độ nhạy không phụ thuộc ngưỡng.

Sức sống của lý thuyết nằm ở phạm vi áp dụng. Bác sĩ đọc phim chụp, hội đồng tuyển dụng sàng hồ sơ, hệ thống chấm điểm tín dụng và mô hình phát hiện giao dịch gian lận đều là bài toán phát hiện tín hiệu. Trong fintech, hệ quả rất cụ thể: một mô hình chặn gian lận bị phàn nàn vì khoá nhầm giao dịch của khách hàng tốt thường không phải mô hình kém, mà là mô hình chạy ở ngưỡng phản ánh việc tổ chức coi bỏ sót gian lận đắt hơn làm phiền khách. Đó là một quyết định kinh doanh và cần được nói ra thành lời thay vì nằm ẩn trong một tham số.

Lý thuyết này kế thừa truyền thống đo lường tri giác mà weber-fechner-law đại diện, nhưng thay khái niệm ngưỡng cứng bằng mô hình xác suất. Nó là công cụ tốt để thấy base-rate-fallacy: khi tỷ lệ nền của tín hiệu rất thấp, ngay cả một máy dò rất nhạy cũng cho ra phần lớn cảnh báo là báo động giả. Nó cũng làm rõ vì sao zero-risk-bias tốn kém — đòi đưa một loại lỗi về không luôn phải trả giá bằng loại lỗi kia. Và nó giải thích cơ chế của illusory-correlation, khi nhiễu ngẫu nhiên vượt ngưỡng đủ thường xuyên để trông như một quy luật.
