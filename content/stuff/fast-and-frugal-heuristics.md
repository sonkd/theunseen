---
title: Fast and Frugal Heuristics
front: Nếu quy tắc đơn giản là "lối tắt kém chính xác", vì sao nó lại thường xuyên dự đoán tốt hơn mô hình phức tạp?
back: Các quy tắc quyết định dùng rất ít thông tin và rất ít phép tính, nhưng đạt độ chính xác cao khi cấu trúc của chúng khớp với cấu trúc của môi trường mà chúng hoạt động.
level: 5
categories: [theory]
tags: [foundational, decision, rationality]
links: [heuristics-and-biases-program, bounded-rationality, attribute-substitution, dual-process-theory]
refs: ['https://en.wikipedia.org/wiki/Heuristic_(psychology)', 'https://en.wikipedia.org/wiki/Bounded_rationality']
strategy: 'Trước khi thêm biến vào một mô hình hay thêm bước vào một quy trình, kiểm tra xem một quy tắc ba dòng có đạt kết quả tương đương trên dữ liệu ngoài mẫu hay không.'
published: true
---

Fast and frugal heuristics là hướng nghiên cứu do Gerd Gigerenzer và nhóm ABC tại Viện Max Planck phát triển từ giữa thập niên 1990. Nó nhận cùng một quan sát với chương trình heuristic và thiên lệch — con người dùng quy tắc rút gọn thay vì tính toán đầy đủ — nhưng rút ra kết luận ngược lại. Thay vì coi các quy tắc đó là phiên bản khiếm khuyết của lý trí, hướng này hỏi: trong môi trường nào thì chúng hoạt động tốt, và tốt tới mức nào so với các mô hình nặng hơn.

Một quy tắc được gọi là nhanh và tiết kiệm khi nó dừng tìm kiếm sớm, dùng ít mẩu thông tin, và không cần trọng số phức tạp. Ví dụ điển hình là quy tắc nhận diện: khi phải chọn giữa hai phương án và chỉ nhận ra một cái tên, hãy chọn cái nhận ra. Nghe có vẻ thô thiển, nhưng trong những lĩnh vực mà mức độ nổi tiếng tương quan với đại lượng cần đoán, nó cho kết quả đáng ngạc nhiên — và dẫn tới hiện tượng ít hơn lại tốt hơn, khi người biết ít về một lĩnh vực đôi lúc đoán chính xác hơn người biết nhiều, vì họ còn dùng được quy tắc này còn người kia thì không. Một quy tắc khác là lấy cái tốt nhất: xét các dấu hiệu theo thứ tự độ tin cậy, dừng ngay tại dấu hiệu đầu tiên phân biệt được hai phương án, bỏ qua toàn bộ phần còn lại.

Lời giải thích thống kê cho việc đơn giản mà vẫn tốt nằm ở đánh đổi giữa thiên lệch và phương sai. Mô hình phức tạp với nhiều tham số bám rất sát dữ liệu quá khứ nhưng cũng bám luôn cả nhiễu trong đó, nên hoạt động kém khi gặp dữ liệu mới. Quy tắc đơn giản có thiên lệch cao hơn nhưng phương sai thấp hơn nhiều. Khi mẫu nhỏ, dữ liệu nhiễu, hoặc môi trường thay đổi theo thời gian, tổng sai số của quy tắc đơn giản thường nhỏ hơn. Đây không phải nghịch lý mà là hệ quả toán học quen thuộc trong học máy.

Khái niệm bao trùm là duy lý sinh thái: tính hợp lý của một quy tắc không nằm trong bản thân quy tắc mà nằm ở mức khớp giữa nó và cấu trúc môi trường. Cùng một quy tắc có thể xuất sắc trong môi trường này và tai hại trong môi trường khác. Vì thế câu hỏi đúng không phải "heuristic có hợp lý không" mà "heuristic nào hợp với môi trường nào".

Ứng dụng trong sản phẩm và tài chính rất cụ thể. Nhiều mô hình chấm điểm rủi ro tinh vi bị đánh bại bởi một cây quyết định ba tầng khi đánh giá ngoài mẫu, đặc biệt khi hành vi khách hàng dịch chuyển. Trong y tế cấp cứu, các quy tắc phân loại dạng nhanh và tiết kiệm được dùng chính vì chúng ổn định và giải thích được. Với thiết kế, cùng nguyên tắc gợi ý rằng một tiêu chí quyết định ngắn mà cả đội thực sự áp dụng thường tạo ra kết quả tốt hơn một khung chấm điểm mười trọng số mà không ai dùng đến lần thứ hai.

Hướng này là đối thoại trực tiếp với heuristics-and-biases-program: cùng đối tượng, khác chuẩn đánh giá. Cả hai đều là hậu duệ của bounded-rationality, ý tưởng rằng lý trí phải được đo trong giới hạn thời gian và năng lực xử lý thật. Nó cho một cách đọc khác về attribute-substitution — việc thay câu hỏi khó bằng dấu hiệu dễ có thể là chiến lược hợp lý nếu dấu hiệu đó thực sự tương quan trong môi trường. Và nó bổ sung sắc thái cho dual-process-theory, nhắc rằng hệ thống nhanh không đơn thuần là phiên bản cẩu thả của hệ thống chậm.
