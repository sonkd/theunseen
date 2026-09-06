---
title: Connectionism
front: Nếu không có chỗ nào trong não chứa quy tắc, vậy quy tắc mà bạn tuân theo hằng ngày đang nằm ở đâu?
back: Khung lý thuyết cho rằng nhận thức nổi lên từ hoạt động song song của mạng lưới các đơn vị đơn giản, nơi tri thức được mã hóa trong trọng số kết nối chứ không phải trong các ký hiệu và quy tắc tường minh.
level: 5
categories: [theory]
tags: [cognitive-science, neural-networks, learning]
links: [schema-theory, predictive-processing, global-workspace-theory, dual-process-theory]
strategy: 'Khi một hành vi có vẻ tuân theo quy tắc, hãy kiểm tra xem hệ thống có thực sự chứa quy tắc đó không, hay chỉ đang khớp mẫu thống kê — hai trường hợp này hỏng theo hai kiểu rất khác nhau.'
refs: ['https://en.wikipedia.org/wiki/Connectionism', 'https://en.wikipedia.org/wiki/Parallel_distributed_processing']
published: true
---

Connectionism là quan điểm cho rằng năng lực nhận thức không đến từ một bộ quy tắc được lưu trữ và thi hành, mà nổi lên từ tương tác của rất nhiều đơn vị xử lý đơn giản kết nối với nhau. Mỗi đơn vị chỉ làm một việc tầm thường: nhận tín hiệu từ các đơn vị khác, cộng lại theo trọng số, rồi phát ra một mức kích hoạt. Tri thức nằm ở tập trọng số, phân tán trên toàn mạng, không định vị được ở một chỗ nào cụ thể. Học tập là quá trình điều chỉnh dần các trọng số ấy dựa trên sai số.

Khung này trở thành trung tâm của khoa học nhận thức sau bộ sách về xử lý phân tán song song do David Rumelhart, James McClelland và nhóm PDP công bố năm 1986. Cuộc tranh luận nổi tiếng nhất xoay quanh việc học chia động từ tiếng Anh ở trẻ em: trẻ thường dùng đúng dạng bất quy tắc, sau đó chuyển sang dùng sai theo quy tắc chung, rồi mới đúng trở lại. Phe biểu tượng đọc đường cong này là bằng chứng trẻ đã rút ra một quy tắc. Các mô hình liên kết cho thấy cùng mẫu hình ấy có thể xuất hiện ở một mạng không hề chứa quy tắc nào, chỉ do phân bố thống kê của dữ liệu đầu vào thay đổi.

Điều này để lại một hệ quả nhận thức luận quan trọng và vẫn còn nguyên giá trị: hành vi tuân theo quy tắc không chứng minh sự tồn tại của quy tắc bên trong hệ thống. Hai kiến trúc rất khác nhau có thể sinh ra cùng một hành vi trong vùng dữ liệu quen thuộc, và chỉ lộ khác biệt khi gặp trường hợp lạ — hệ thống dựa trên quy tắc thường hỏng dứt khoát, hệ thống liên kết thì suy giảm dần và đưa ra câu trả lời có vẻ hợp lý nhưng sai. Đây cũng chính là hình dáng lỗi mà ta quan sát ở các mô hình học sâu hiện nay, vốn là hậu duệ kỹ thuật trực tiếp của truyền thống này.

Connectionism cung cấp một cách hiểu về cơ chế cho schema-theory: bộ khung tri thức không cần là một cấu trúc được lưu sẵn mà có thể là mẫu kích hoạt ổn định của mạng. Nó ăn khớp tự nhiên với predictive-processing, nơi học tập cũng được dẫn dắt bởi sai số dự đoán. Nó tương phản với global-workspace-theory, vốn nhấn mạnh một không gian chung nơi thông tin được phát rộng, và nó cho một cơ sở khả dĩ cho phần trực giác nhanh trong dual-process-theory — thứ khớp mẫu tức thời mà ta không giải thích nổi bằng lời.
