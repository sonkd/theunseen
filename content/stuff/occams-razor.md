---
title: Occam’s razor
front: '''Occam’s razor'' là gì, và nó tác động thế nào đến cách bạn nghĩ hoặc ra quyết định?'
back: Nguyên tắc cho rằng khi có nhiều giả thuyết cùng giải thích được một hiện tượng, giả thuyết đơn giản nhất — ít giả định nhất — thường đáng được xem xét trước. Còn gọi là "luật tiết kiệm" (law of parsimony).
level: 2
categories: [heuristic, mental-models]
links: [inversion, second-order-thinking, law-of-the-instrument]
refs: ['https://en.wikipedia.org/wiki/Occam%27s_razor']
strategy: 'Trước khi chấp nhận một lời giải thích phức tạp, thử hỏi: có cách giải thích nào đơn giản hơn, ít giả định hơn, mà vẫn khớp với toàn bộ dữ liệu đang có không?'
published: true
---

Occam's razor (dao cạo Occam) là nguyên tắc tư duy cho rằng khi có nhiều giả thuyết cùng giải thích được một hiện tượng, giả thuyết nào đòi hỏi ít giả định nhất thường nên được ưu tiên xem xét trước — không phải vì nó chắc chắn đúng, mà vì nó dễ kiểm chứng và ít điểm có thể sai hơn.

Nguyên tắc mang tên tu sĩ dòng Francis William of Ockham (thế kỷ 14), người phát biểu dưới dạng "không nên nhân số thực thể lên quá mức cần thiết". Đây không phải một định luật khoa học chặt chẽ mà là một heuristic chọn giả thuyết — bản thân nó không chứng minh giả thuyết đơn giản là đúng, chỉ gợi ý nó nên được kiểm định trước vì chi phí xác minh thấp hơn. Trong khoa học hiện đại, nguyên tắc này ẩn sau tiêu chí AIC/BIC dùng để so sánh mô hình thống kê — mô hình phức tạp hơn phải mang lại độ khớp dữ liệu tốt hơn đáng kể mới được chọn thay mô hình đơn giản.

Trong sản phẩm, Occam's razor là nguyên tắc ngầm đứng sau nhiều quyết định thiết kế tốt: khi một luồng người dùng bị lỗi, giả thuyết "nút bấm đặt sai vị trí" thường đáng kiểm tra trước "người dùng không hiểu khái niệm sản phẩm" — vì giả thuyết đầu dễ xác minh và ít rủi ro suy diễn sai hơn. Trong phân tích dữ liệu, khi một chỉ số sụt giảm đột ngột, nên loại trừ các nguyên nhân đơn giản (lỗi tracking, thay đổi định nghĩa metric, ngày lễ) trước khi nhảy tới giả thuyết phức tạp về hành vi người dùng thay đổi — vì kinh nghiệm cho thấy phần lớn các cú sụt bất thường đến từ nguyên nhân kỹ thuật đơn giản, không phải insight sâu sắc.

Occam's razor liên quan chặt với law-of-the-instrument — cả hai đều cảnh báo về việc chọn công cụ hoặc giải thích không phù hợp với vấn đề, dù theo hướng ngược nhau: law-of-the-instrument nói về việc dùng một công cụ quen thuộc cho mọi vấn đề, còn Occam's razor nói về việc chọn giải thích tối giản cho một vấn đề cụ thể. Nó cũng có thể kết hợp với inversion (tư duy ngược — thử loại trừ các khả năng sai trước khi tìm câu trả lời đúng) và second-order-thinking khi cần cân nhắc liệu giải pháp đơn giản có bỏ sót hệ quả bậc hai quan trọng hay không — Occam's razor là điểm khởi đầu tốt, nhưng không phải luôn là điểm kết thúc.
