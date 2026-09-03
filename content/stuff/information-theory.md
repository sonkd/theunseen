---
title: Information Theory
front: Nếu một tin nhắn báo đúng thứ bạn đã đoán chắc, nó có mang thông tin nào không?
back: Lý thuyết thông tin định nghĩa lượng tin của một thông điệp bằng mức bất định mà nó xoá bỏ — thông điệp càng bất ngờ thì càng chứa nhiều thông tin.
level: 5
categories: [theory]
tags: [entropy, communication, uncertainty]
links: [signal-detection-theory, bounded-rationality, magic-number-7-2, cognitive-load-theory]
refs: ['https://en.wikipedia.org/wiki/Information_theory', 'https://en.wikipedia.org/wiki/Entropy_(information_theory)']
strategy: 'Đo giá trị của một báo cáo bằng mức nó thay đổi quyết định của bạn, không bằng số liệu nó chứa — dữ liệu xác nhận điều đã biết có lượng tin gần bằng không.'
published: true
---

Information theory là khung toán học do Claude Shannon xây dựng trong bài báo *A Mathematical Theory of Communication* (1948). Đóng góp nền tảng của nó là tách khái niệm thông tin khỏi khái niệm ý nghĩa. Với Shannon, lượng tin của một thông điệp không phụ thuộc vào nó nói gì mà phụ thuộc vào việc nó khó đoán tới đâu. Một thông điệp chắc chắn xảy ra mang lượng tin bằng không; một thông điệp hiếm mang lượng tin lớn.

Đại lượng trung tâm là entropy: mức bất định trung bình của một nguồn phát. Nguồn phát ra các ký hiệu với xác suất đồng đều có entropy cao nhất, vì không thể đoán trước gì. Nguồn thiên lệch mạnh có entropy thấp, và chính độ thấp ấy cho phép nén. Toàn bộ công nghệ nén dữ liệu, mã sửa lỗi và ước lượng dung lượng kênh truyền đều mọc ra từ khung này, cùng với định lý mã hoá kênh chỉ ra rằng mỗi kênh nhiễu có một tốc độ truyền tối đa mà dưới đó sai số có thể đưa về gần không.

Điều làm cho lý thuyết này thuộc tầng nền tảng của nhận thức là nó cung cấp một cách phát biểu chính xác cho một trực giác cũ: tri giác và tư duy là các quá trình giảm bất định dưới ràng buộc dung lượng. Hệ thần kinh có băng thông hữu hạn, nên nó không thể — và không nên — truyền tải mọi thứ chạm vào giác quan. Nó ưu tiên mã hoá cái bất ngờ và bỏ qua cái dự đoán được, vì cái dự đoán được không làm giảm bất định thêm chút nào. Đây là lý do các mô hình hiện đại về vỏ não thị giác được xây quanh ý tưởng mã hoá sai số dự đoán chứ không phải truyền tải tín hiệu thô.

Cùng logic ấy đặt trần cho khả năng ra quyết định của con người và tổ chức. Một hệ thống chỉ có thể xử lý một lượng bất định nhất định trong một đơn vị thời gian; vượt quá đó, thêm dữ liệu không cải thiện quyết định mà làm nhiễu nó. Điều này cho một tiêu chí thực dụng để đánh giá báo cáo và bảng theo dõi: giá trị của một chỉ số bằng mức nó dịch chuyển phân phối niềm tin của người đọc. Một chỉ số luôn xanh, một biểu đồ chỉ xác nhận điều ai cũng biết, một cột số liệu suy ra được từ cột bên cạnh — tất cả đều chiếm băng thông mà không mang lượng tin.

Card này cung cấp nền lượng hoá cho signal-detection-theory, vốn xử lý bài toán tách tín hiệu khỏi nhiễu ở mức quyết định. Nó là một cách phát biểu ràng buộc mà bounded-rationality mô tả ở tầng hành vi. Và nó giải thích vì sao các giới hạn dung lượng trong magic-number-7-2 và cognitive-load-theory không phải khiếm khuyết ngẫu nhiên mà là hệ quả của việc mọi kênh đều hữu hạn.
