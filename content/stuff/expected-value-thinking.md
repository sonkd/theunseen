---
title: Expected Value Thinking
front: Một lựa chọn thắng chín lần trên mười vẫn có thể là lựa chọn tồi — điều gì ở lần thứ mười quyết định chuyện đó?
back: Cách đánh giá lựa chọn bằng tổng của từng kết quả nhân với xác suất của nó, thay vì bằng kết quả dễ hình dung nhất hay bằng tần suất thắng thua.
level: 3
categories: [mental-models, heuristic]
tags: [decision, probability, risk]
links: [probabilistic-thinking, expected-utility-theory, outcome-bias, margin-of-safety]
strategy: 'Trước khi chốt, viết ra ba kết quả có thể kèm xác suất và độ lớn của mỗi kết quả — nếu không viết được xác suất, bạn đang quyết định bằng cảm giác chứ không bằng giá trị kỳ vọng.'
refs: ['https://en.wikipedia.org/wiki/Expected_value', 'https://en.wikipedia.org/wiki/Decision_theory']
published: true
---

Expected value thinking thay câu hỏi "phương án này có khả năng thành công không" bằng câu hỏi "nếu lặp lại lựa chọn này rất nhiều lần, trung bình mỗi lần tôi được gì". Cách tính đơn giản: liệt kê các kết quả có thể, gán cho mỗi kết quả một xác suất và một giá trị, rồi cộng tất cả các tích lại. Điều làm nó khác biệt so với trực giác là nó buộc ta nhân xác suất với độ lớn, thay vì để một trong hai đại lượng lấn át đại lượng kia.

Đây chính là chỗ trực giác hay hỏng. Một canh bạc thắng 95% các lần nhưng lần thua mất gấp năm mươi lần tiền thắng là canh bạc lỗ, dù cảm giác về nó rất tốt vì phần lớn thời gian ta thấy mình đúng. Ngược lại, một khoản đầu tư thất bại tám trên mười lần vẫn có thể xuất sắc nếu hai lần thành công trả lại gấp trăm. Hai ví dụ này giải thích vì sao "tỷ lệ thắng" là chỉ số gây hiểu lầm bậc nhất trong mọi cuộc thảo luận về rủi ro.

Áp dụng vào công việc sản phẩm, khung này thay đổi cách xếp thứ tự việc cần làm. Một thử nghiệm có 20% khả năng nâng tỷ lệ hoàn tất đăng ký thêm ba điểm phần trăm thường đáng làm hơn một cải tiến chắc chắn nâng được 0,2 điểm, nếu chi phí hai bên tương đương. Trong tín dụng, quyết định phê duyệt một hồ sơ không phải là dự đoán khách hàng này có trả nợ hay không, mà là so sánh biên lãi kỳ vọng với xác suất vỡ nợ nhân mức tổn thất khi vỡ nợ. Nhưng khung này có một giới hạn quan trọng: nó chỉ hợp lệ khi ta thực sự được lặp lại nhiều lần. Với những quyết định một lần mà kết quả xấu là không thể phục hồi — mất giấy phép, mất niềm tin của khách hàng — giá trị kỳ vọng dương vẫn không đủ để biện minh.

Cách tư duy này là dạng định lượng của probabilistic-thinking, và là phiên bản trung tính về tiền của expected-utility-theory — vốn thừa nhận rằng mỗi đồng tăng thêm không có giá trị như nhau với mọi người. Nó cũng là liều thuốc trực tiếp cho outcome-bias, thói quen đánh giá chất lượng quyết định qua kết quả thực tế thay vì qua thông tin có tại thời điểm quyết định. Còn ràng buộc về những mất mát không thể phục hồi chính là lý do margin-of-safety tồn tại như một điều kiện đi kèm, chứ không phải một tùy chọn.
