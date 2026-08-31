---
title: Certainty Effect
front: Vì sao bạn sẵn sàng trả thêm rất nhiều để đi từ 95% chắc chắn lên 100%, nhưng chẳng buồn trả gì để đi từ 60% lên 65%?
back: Xu hướng đánh giá quá cao những kết quả chắc chắn so với những kết quả chỉ gần như chắc chắn — mức tăng xác suất ở đoạn cuối được cảm nhận lớn hơn hẳn mức tăng tương đương ở đoạn giữa.
level: 2
categories: [bias]
tags: [decision, risk]
links: [prospect-theory, pseudocertainty-effect, zero-risk-bias, framing-effect]
refs: ['https://en.wikipedia.org/wiki/Allais_paradox', 'https://en.wikipedia.org/wiki/Prospect_theory']
strategy: 'Trước khi trả giá cho sự chắc chắn tuyệt đối, quy nó về tiền: bạn đang mua bao nhiêu điểm phần trăm rủi ro, và mỗi điểm đó giá bao nhiêu?'
published: true
---

Certainty effect là hiện tượng con người gán trọng số tâm lý không đều cho các mức xác suất. Một bước nhảy năm điểm phần trăm ở giữa thang — từ 60% lên 65% — hầu như không tạo cảm giác gì. Cũng năm điểm đó nhưng ở đoạn cuối — từ 95% lên 100% — lại được cảm nhận như một khác biệt về chất, không phải về lượng. Sự chắc chắn tuyệt đối có một sức hút riêng, và người ta trả giá cho nó vượt xa giá trị kỳ vọng.

Nghịch lý Allais, do nhà kinh tế Maurice Allais đưa ra năm 1953, là bằng chứng đầu tiên cho thấy điều này phá vỡ lý thuyết chuẩn tắc. Trong một cặp lựa chọn, đa số người chọn phương án thắng chắc chắn thay vì một phương án có kỳ vọng cao hơn nhưng kèm rủi ro nhỏ trắng tay. Trong cặp thứ hai, cùng những khoản tiền đó nhưng mọi xác suất đều bị chia nhỏ đi, đa số lại đảo ngược lựa chọn. Hai câu trả lời này không thể cùng đúng dưới expected-utility-theory, vì phần chung giữa hai bài toán lẽ ra phải triệt tiêu.

Kahneman và Tversky đưa hiện tượng vào prospect-theory qua hàm trọng số xác suất: xác suất khách quan được biến đổi thành trọng số quyết định theo một đường cong chữ S ngược. Xác suất nhỏ bị thổi phồng, giải thích vì sao người ta mua vé số và mua bảo hiểm cho những rủi ro rất hiếm. Xác suất lớn nhưng chưa tuyệt đối bị hạ thấp, giải thích chính certainty effect. Điểm 100% nằm ở rìa hàm, nơi độ dốc thay đổi đột ngột.

Trong fintech, hiệu ứng này chi phối cả hai phía bảng cân đối. Người dùng chấp nhận lãi suất tiết kiệm thấp hơn hẳn để đổi lấy cảm giác an toàn tuyệt đối, dù chênh lệch rủi ro thực tế rất nhỏ. Ở chiều ngược lại, các gói bảo hiểm mở rộng bán chạy nhất là những gói hứa hẹn bảo vệ toàn phần, dù phần rủi ro còn lại mà chúng loại bỏ thường không đáng giá bằng phí. Và trong thiết kế luồng thanh toán, câu chữ như bảo đảm hoàn tiền 100% có tác động lên tỷ lệ chuyển đổi lớn hơn nhiều so với một mức 95% được diễn đạt bằng con số.

Certainty effect có quan hệ trực tiếp với pseudocertainty-effect, nơi một cảm giác chắc chắn giả được tạo ra bằng cách chia bài toán thành nhiều giai đoạn. Nó là động cơ nằm dưới zero-risk-bias, xu hướng dồn nguồn lực để xoá sạch một rủi ro nhỏ thay vì giảm mạnh một rủi ro lớn. Và vì mọi thứ ở đây phụ thuộc vào cách bài toán được trình bày, nó gắn chặt với framing-effect.
