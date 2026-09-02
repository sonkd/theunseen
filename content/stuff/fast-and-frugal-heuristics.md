---
title: Fast-and-Frugal Heuristics
front: Vì sao một quy tắc chỉ dùng đúng một manh mối lại có thể dự báo chính xác hơn mô hình cân nhắc đủ mọi biến?
back: Các quy tắc quyết định đơn giản, ít thông tin, ít tính toán, do Gerd Gigerenzer và nhóm ABC nghiên cứu — chúng hoạt động tốt khi cấu trúc của quy tắc khớp với cấu trúc của môi trường.
level: 5
categories: [theory]
tags: [heuristic, rationality, decision]
links: [heuristics-and-biases-program, bounded-rationality, availability-heuristic, less-is-better-effect]
refs: ['https://en.wikipedia.org/wiki/Gerd_Gigerenzer', 'https://en.wikipedia.org/wiki/Recognition_heuristic']
strategy: 'Trước khi xây một mô hình phức tạp, thử một quy tắc một-manh-mối làm chuẩn so sánh — nếu mô hình không thắng được nó ngoài mẫu, sự phức tạp đó không đáng giá.'
published: true
---

Fast-and-Frugal Heuristics là dòng nghiên cứu do Gerd Gigerenzer, Peter Todd và nhóm ABC tại Viện Max Planck phát triển, tổng kết trong *Simple Heuristics That Make Us Smart* (1999). Luận điểm của nó là một sự đảo chiều: heuristic không phải phiên bản lỗi của lý tính, mà là công cụ được tiến hoá và học tập trang bị cho những môi trường mà thông tin thì thiếu, thời gian thì ít, và tương lai thì không giống hệt quá khứ.

"Nhanh" nghĩa là ít bước tính; "tiết kiệm" nghĩa là dùng ít manh mối. Một ví dụ được nghiên cứu kỹ là **recognition heuristic**: khi so hai lựa chọn mà bạn chỉ nhận ra một, hãy chọn cái bạn nhận ra. Nghe thô sơ, nhưng nếu việc bạn nhận ra một thành phố có tương quan với quy mô của nó, quy tắc này dự đoán thành phố nào đông dân hơn khá tốt — và đôi khi người ít hiểu biết hơn lại đoán đúng hơn người biết cả hai, vì họ còn dùng được quy tắc. Một ví dụ khác là **take-the-best**: xếp các manh mối theo độ tin cậy, đọc lần lượt, dừng ngay ở manh mối đầu tiên phân biệt được hai phương án, bỏ qua tất cả phần còn lại. Trong nhiều bộ dữ liệu thực, take-the-best dự báo ngoài mẫu ngang hoặc tốt hơn hồi quy đa biến.

Lời giải thích cho nghịch lý "ít mà tốt hơn" là bài toán đánh đổi thiên lệch–phương sai. Mô hình phức tạp ước lượng nhiều tham số, nên bám sát dữ liệu huấn luyện và khuếch đại nhiễu của mẫu; quy tắc đơn giản có thiên lệch cao hơn nhưng phương sai thấp hơn nhiều, và với mẫu nhỏ hoặc môi trường biến động, tổng sai số của nó lại nhỏ hơn. Đây là lập luận thống kê, không phải lời khen ngợi sự đơn giản.

Khái niệm khoá của cả chương trình là **ecological rationality**: không có heuristic nào tốt hay tệ một cách tuyệt đối; chỉ có sự khớp hoặc không khớp giữa cấu trúc quy tắc và cấu trúc môi trường. Recognition heuristic sụp đổ trong môi trường mà mức độ nổi tiếng không tương quan với đại lượng cần đoán. Câu hỏi đúng vì thế không phải "quy tắc này có hợp lý không" mà "quy tắc này hợp lý trong môi trường nào".

Trong thực hành sản phẩm và dữ liệu, hệ quả rất cụ thể: luôn dựng một baseline đơn giản — một quy tắc một biến, hoặc một cây quyết định ba tầng — trước khi tin vào một mô hình phức tạp; và với các quyết định vận hành cần con người thực thi dưới áp lực, một checklist ngắn thường tạo ra kết quả tốt hơn một điểm số mà không ai hiểu.

Dòng này là đối trọng có chủ đích với heuristics-and-biases-program: cùng nghiên cứu một đối tượng, nhưng lấy chuẩn so sánh là hiệu quả trong môi trường thực thay vì tiên đề của lý thuyết xác suất. Cả hai đều là hậu duệ của bounded-rationality của Herbert Simon, chỉ khác ở chỗ nhấn vào giới hạn hay vào sự thích nghi. Nó buộc ta đọc lại availability-heuristic theo hướng ôn hoà hơn — độ dễ nhớ là một manh mối thật, chỉ sai khi môi trường bóp méo cái được nhớ. Và nó là nền lý thuyết cho less-is-better-effect: thêm thông tin không phải lúc nào cũng cải thiện phán đoán.
