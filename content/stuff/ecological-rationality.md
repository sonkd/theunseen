---
title: Ecological Rationality
front: Một quy tắc ngón tay cái là hợp lý hay phi lý — hay câu hỏi đó chỉ trả lời được khi biết nó đang chạy trong môi trường nào?
back: Quan điểm cho rằng tính hợp lý của một chiến lược nhận thức không nằm trong bản thân chiến lược, mà nằm ở mức độ khớp giữa cấu trúc của nó và cấu trúc của môi trường nơi nó được dùng.
level: 5
categories: [theory]
tags: [decision, heuristics]
links: [fast-and-frugal-heuristics, bounded-rationality, heuristics-and-biases-program, signal-detection-theory]
refs: ['https://en.wikipedia.org/wiki/Ecological_rationality', 'https://en.wikipedia.org/wiki/Bounded_rationality']
strategy: 'Trước khi gọi một hành vi là phi lý, mô tả môi trường mà nó tiến hoá để phục vụ — rồi hỏi hành vi đó có hợp lý trong chính môi trường ấy không.'
published: true
---

Ecological rationality là lập trường cho rằng không tồn tại một tiêu chuẩn hợp lý duy nhất, độc lập với bối cảnh. Một quy tắc quyết định chỉ có thể được đánh giá theo cặp: quy tắc và môi trường. Cùng một heuristic có thể vượt trội một mô hình hồi quy phức tạp trong môi trường này và thua đậm trong môi trường kia. Câu hỏi đúng không phải quy tắc này có hợp lý không, mà là nó khớp với cấu trúc thống kê nào.

Ý tưởng nối tiếp trực tiếp hình ảnh chiếc kéo hai lưỡi của Herbert Simon: hành vi được cắt bởi cả năng lực nhận thức lẫn cấu trúc môi trường, và nhìn một lưỡi thôi thì không hiểu được vết cắt. Gerd Gigerenzer cùng nhóm ABC tại Viện Max Planck phát triển nó thành một chương trình nghiên cứu từ thập niên 1990, với công cụ chính là mô phỏng: cho một heuristic đơn giản và một mô hình thống kê đầy đủ cùng chạy trên dữ liệu thực, rồi so kết quả dự báo ngoài mẫu.

Kết quả lặp lại nhiều lần là less-is-more: trong môi trường có mẫu nhỏ, nhiều biến nhiễu và quan hệ không ổn định theo thời gian, quy tắc bỏ qua phần lớn thông tin thường dự báo tốt hơn mô hình dùng hết thông tin. Lý do nằm ở phân rã sai số: mô hình phức tạp giảm được phần chệch nhưng gánh phương sai lớn, còn heuristic chấp nhận chệch để giữ phương sai thấp. Khi dữ liệu ít và thế giới hay đổi, đánh đổi đó có lợi. Đây là một lập luận thống kê, không phải lời ca ngợi trực giác.

Chương trình này đứng ở thế đối thoại căng thẳng với heuristics-and-biases-program. Truyền thống Kahneman và Tversky đo hành vi so với chuẩn mực chuẩn tắc và ghi nhận sai lệch có hệ thống; truyền thống ecological rationality phản biện rằng chuẩn mực ấy thường được lấy từ phòng thí nghiệm chứ không từ môi trường mà cơ chế nhận thức tiến hoá để phục vụ, nên nhiều sai lệch tan biến khi bài toán được trình bày dưới dạng tần suất tự nhiên. Cả hai vẫn cùng tồn tại, và cách đọc cân bằng là chúng trả lời hai câu hỏi khác nhau chứ không phải một câu hỏi với hai đáp án.

Với công việc sản phẩm, hệ quả rất cụ thể. Một mô hình chấm điểm tín dụng dùng năm chục biến có thể thua một quy tắc ba biến khi danh mục còn nhỏ và hành vi khách hàng đang dịch chuyển. Và một luồng giao diện buộc người dùng cân nhắc mọi thuộc tính không nhất thiết cho quyết định tốt hơn — nó chỉ tốt hơn nếu môi trường đủ ổn định để những thuộc tính đó thật sự mang tin.

Khung này là phần mở rộng tự nhiên của bounded-rationality, và fast-and-frugal-heuristics là bộ công cụ cụ thể mà nó nghiên cứu. Về phương pháp, nó chia tinh thần với signal-detection-theory: cả hai đều nhấn rằng chất lượng của một quyết định phải được đo cùng với đặc tính của môi trường tạo ra tín hiệu.
