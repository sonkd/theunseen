---
title: Epistemic vs Aleatory Uncertainty
front: Bạn không chắc vì chưa biết đủ, hay vì bản thân sự việc vốn ngẫu nhiên — và hai trường hợp đó có cần cách xử lý giống nhau không?
back: Phân biệt giữa bất định do thiếu hiểu biết (giảm được bằng cách thu thập thêm dữ liệu) và bất định do bản chất ngẫu nhiên của quá trình (không giảm được, chỉ mô tả được bằng phân bố).
level: 4
categories: [theory, mental-models]
tags: [uncertainty, probability]
links: [calibrated-confidence, bayesian-updating, unknown-unknowns, metacognition]
refs: ['https://en.wikipedia.org/wiki/Uncertainty_quantification', 'https://en.wikipedia.org/wiki/Knightian_uncertainty']
strategy: 'Với mỗi con số bất định, hỏi thu thập thêm dữ liệu có làm nó hẹp lại không — nếu có thì đi lấy dữ liệu, nếu không thì thiết kế để chịu được phân bố.'
published: true
---

Hai loại bất định trông giống nhau từ bên trong nhưng đòi hỏi hành động trái ngược. Bất định nhận thức, hay epistemic, đến từ chỗ ta chưa biết đủ về hệ thống: tham số chưa đo, cơ chế chưa hiểu, mô hình chưa đúng. Nó co lại khi có thêm thông tin. Bất định ngẫu nhiên, hay aleatory, đến từ chính sự biến thiên của quá trình: kết quả tung xúc xắc, thời điểm một khách hàng cụ thể quyết định rời đi. Thu thập thêm dữ liệu không làm nó nhỏ đi — dữ liệu chỉ giúp mô tả phân bố chính xác hơn.

Phép phân biệt này có gốc từ thống kê và kỹ thuật, nơi nó là nền của lĩnh vực định lượng bất định trong mô phỏng và mô hình rủi ro. Trong kinh tế học, Frank Knight đưa ra một phân biệt gần gũi năm 1921 giữa risk và uncertainty: rủi ro là thứ có phân bố xác suất biết được, còn bất định Knight là thứ ngay cả phân bố cũng không biết. Ba khái niệm này không trùng khít nhưng cùng chỉ về một điểm: gộp mọi thứ không chắc chắn vào một con số duy nhất sẽ che mất câu hỏi quan trọng nhất — có đáng bỏ tiền đi tìm hiểu thêm không.

Hệ quả thực hành nằm ở chỗ đó. Nếu phần lớn bất định là epistemic, khoản đầu tư đúng là nghiên cứu: chạy thử nghiệm, phỏng vấn, đo thêm, xây mô hình tốt hơn. Nếu phần lớn là aleatory, tiền bỏ vào nghiên cứu gần như lãng phí, và khoản đầu tư đúng là thiết kế chịu đựng: đệm dự phòng, giới hạn thiệt hại, đa dạng hoá, kế hoạch dự phòng cho phần đuôi phân bố. Nhầm loại là một trong những cách đốt ngân sách phân tích phổ biến nhất — nghiên cứu mãi một thứ vốn không thể biết trước, hoặc chấp nhận số phận với một thứ chỉ cần một tuần đo đạc là sáng tỏ.

Trong sản phẩm số, ranh giới thường khá rõ nếu chịu hỏi. Tỷ lệ chuyển đổi thật của một luồng thanh toán mới là bất định epistemic: chạy thử nghiệm với cỡ mẫu đủ lớn thì khoảng tin cậy hẹp lại. Việc một khách hàng cụ thể nào trong nhóm rủi ro cao sẽ vỡ nợ trong quý tới phần lớn là aleatory: mô hình tốt hơn cải thiện xếp hạng, nhưng không xoá được tính ngẫu nhiên ở cấp cá nhân, nên chính sách đúng là định giá theo danh mục và dự phòng, không phải cố dự đoán từng người.

Phân biệt này là điều kiện để calibrated-confidence có ý nghĩa, vì một khoảng tin cậy trộn lẫn hai nguồn sai số sẽ không được diễn giải đúng. Nó cũng làm rõ giới hạn của bayesian-updating: cập nhật thu hẹp phần epistemic, còn phần aleatory vẫn nguyên vẹn dù có bao nhiêu dữ liệu. Và cả hai loại vẫn nằm bên trong mô hình hiện tại — phần nằm ngoài mô hình là unknown-unknowns, thứ mà không phép tính nào bắt được. Nhận ra mình đang đứng ở loại nào là một bài tập metacognition điển hình.
