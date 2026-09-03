---
title: Fast and Frugal Heuristics
front: Một quy tắc chỉ dùng một manh mối duy nhất lại dự báo chính xác hơn mô hình hồi quy đầy đủ — chuyện đó xảy ra khi nào?
back: Heuristic nhanh và tiết kiệm là các quy tắc quyết định đơn giản, dùng ít thông tin và ít phép tính, nhưng đạt độ chính xác cao khi cấu trúc của chúng khớp với cấu trúc của môi trường.
level: 5
categories: [theory]
tags: [gigerenzer, decision-rules, robustness]
links: [heuristics-and-biases-program, bounded-rationality, dual-process-theory, attribute-substitution]
refs: ['https://en.wikipedia.org/wiki/Fast-and-frugal_trees', 'https://en.wikipedia.org/wiki/Gerd_Gigerenzer']
strategy: 'Khi dữ liệu ít và nhiễu cao, hãy so sánh mô hình phức tạp với một quy tắc một manh mối trên dữ liệu ngoài mẫu — nếu quy tắc đơn giản không thua, nó là lựa chọn tốt hơn vì nó bền hơn.'
published: true
---

Fast and frugal heuristics là chương trình nghiên cứu do Gerd Gigerenzer và nhóm ABC tại Viện Max Planck phát triển từ giữa thập niên 1990. Nó chia sẻ tiền đề với dòng nghiên cứu heuristic trước đó — con người dùng quy tắc rút gọn — nhưng rút ra kết luận ngược lại về giá trị của chúng. Thay vì coi quy tắc rút gọn là nguồn sai lệch cần chữa, chương trình này hỏi: trong môi trường nào thì quy tắc rút gọn cho kết quả tốt hơn phép tính đầy đủ, và vì sao.

Ví dụ kinh điển là heuristic nhận biết. Khi phải chọn thành phố nào đông dân hơn giữa hai cái tên, một quy tắc chỉ dựa vào việc "tôi có nghe tên thành phố này không" đạt độ chính xác cao đáng ngạc nhiên — trong một số bối cảnh còn cao hơn ở người biết ít hơn, vì người biết cả hai tên mất đi manh mối phân biệt. Một ví dụ khác là take-the-best: xét các manh mối theo thứ tự độ tin cậy giảm dần, dừng ngay ở manh mối đầu tiên phân biệt được hai phương án, bỏ qua toàn bộ phần còn lại. Trong các so sánh trên dữ liệu thực, quy tắc này nhiều lần ngang bằng hoặc vượt hồi quy tuyến tính dùng đủ biến khi dự báo ngoài mẫu.

Lý do nằm ở đánh đổi giữa độ chệch và phương sai. Mô hình phức tạp có độ chệch thấp nhưng phương sai cao: nó bám sát mẫu huấn luyện, kể cả phần nhiễu, nên kém ổn định khi gặp dữ liệu mới. Quy tắc đơn giản chấp nhận độ chệch cao hơn để đổi lấy phương sai rất thấp. Khi mẫu nhỏ, nhiễu lớn hoặc môi trường thay đổi, đánh đổi này nghiêng về phía đơn giản. Đây là lập luận thống kê chứ không phải lời ca ngợi trực giác.

Khái niệm gắn kèm là duy lý sinh thái: một heuristic không tốt hay xấu tự thân, nó tốt hay xấu tuỳ mức khớp giữa cấu trúc của nó và cấu trúc thống kê của môi trường. Heuristic nhận biết chỉ hiệu quả khi mức độ nổi tiếng tương quan với đại lượng cần đoán. Đưa nó sang môi trường không có tương quan ấy thì nó thành vô dụng.

Ứng dụng rõ nhất là các cây quyết định nhanh và tiết kiệm trong y tế cấp cứu và sàng lọc rủi ro: ba tới bốn câu hỏi có thứ tự, mỗi câu có thể dẫn thẳng tới quyết định. Trong tài chính, cùng nguyên tắc áp dụng cho quy tắc sàng lọc tín dụng ở phân khúc thiếu dữ liệu lịch sử — nơi mô hình nhiều biến dễ học phải nhiễu. Điều kiện đi kèm luôn là kiểm định ngoài mẫu, vì tính đơn giản không tự bảo đảm tính chính xác.

Card này là đối trọng học thuật trực tiếp của heuristics-and-biases-program: cùng đối tượng, khác chuẩn đánh giá. Nó là cách đọc tích cực đối với bounded-rationality của Simon, vận hành trong kiến trúc mà dual-process-theory mô tả, và cho thấy attribute-substitution không nhất thiết là lỗi khi thuộc tính thay thế có tương quan tốt với thuộc tính đích.
