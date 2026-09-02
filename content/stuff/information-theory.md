---
title: Information Theory
front: Làm sao đo được "lượng tin" trong một câu nói, khi hai câu dài bằng nhau có thể cho bạn biết nhiều ít khác hẳn?
back: Lý thuyết của Claude Shannon đo lượng thông tin bằng mức độ bất định được giảm đi — thông tin không nằm ở nội dung, mà ở việc nó loại bỏ được bao nhiêu khả năng.
level: 5
categories: [theory]
tags: [information, entropy, communication]
links: [signal-detection-theory, bounded-rationality, map-is-not-the-territory]
refs: ['https://en.wikipedia.org/wiki/Information_theory', 'https://en.wikipedia.org/wiki/Entropy_(information_theory)']
strategy: 'Đánh giá một báo cáo hay một chỉ số bằng câu hỏi: nó loại bỏ được bao nhiêu khả năng? Thứ mà bạn đã đoán trước được thì không mang thông tin, dù dài đến đâu.'
published: true
---

Information Theory bắt đầu từ một bài báo duy nhất: "A Mathematical Theory of Communication" của Claude Shannon, công bố năm 1948 tại Bell Labs. Đóng góp cốt lõi của nó là tách khái niệm "thông tin" khỏi khái niệm "ý nghĩa", và định nghĩa thông tin theo một đại lượng đo được: **mức giảm bất định**.

Trực giác nền: một tin nhắn mang nhiều thông tin khi nó khiến bạn ngạc nhiên. Nếu bạn đã biết chắc trời sẽ nắng, câu "hôm nay trời nắng" không mang thông tin nào cả. Nếu xác suất nắng và mưa là 50–50, cùng câu đó loại bỏ đúng một nửa số khả năng — Shannon gọi lượng đó là **một bit**. Tổng quát hơn, entropy của một nguồn là kỳ vọng của mức ngạc nhiên trên tất cả các thông điệp nó có thể phát ra: nguồn càng khó đoán thì entropy càng cao.

Từ định nghĩa đó, Shannon rút ra hai định lý nền tảng. Định lý mã hoá nguồn đặt giới hạn dưới tuyệt đối cho việc nén: không thể nén một nguồn xuống dưới entropy của nó mà không mất mát — đó là lý do mọi phần mềm nén đều đụng trần ở đâu đó. Định lý mã hoá kênh cho một kết quả gần như phản trực giác: mọi kênh truyền, dù nhiễu đến đâu, đều có một **dung lượng** hữu hạn, và ở dưới mức đó ta có thể truyền tin với xác suất lỗi nhỏ tuỳ ý — bằng cách thêm dư thừa (redundancy) một cách thông minh. Toàn bộ hạ tầng viễn thông, lưu trữ số và mã sửa lỗi hiện đại đứng trên hai định lý này.

Với khoa học nhận thức, ảnh hưởng đến theo đường gián tiếp nhưng sâu. Nó cung cấp ngôn ngữ để nói về giới hạn xử lý của con người bằng con số thay vì bằng ẩn dụ — dòng nghiên cứu về dung lượng kênh của trí nhớ ngắn hạn thập niên 1950 mang dấu ấn trực tiếp của Shannon. Nó cũng đặt nền cho cách nghĩ hiện đại về tri giác: hệ thần kinh không truyền lại toàn bộ tín hiệu mà mã hoá phần bất ngờ, bỏ đi phần dư thừa đã dự đoán được.

Trong công việc dữ liệu, khung này rất thực dụng. Một dashboard mười biểu đồ mà chín cái luôn xanh thì mang gần như không có thông tin, dù chiếm chín phần mười diện tích màn hình. Một chỉ số đáng theo dõi là chỉ số mà bạn không đoán trước được giá trị của nó. Cùng logic ấy giải thích vì sao thêm biến vào mô hình không phải lúc nào cũng cải thiện dự báo: biến chỉ có giá trị khi nó mang thông tin chưa có trong các biến còn lại.

Information Theory là nền toán học của signal-detection-theory — cả hai đều xử lý bài toán tách tín hiệu khỏi nhiễu, chỉ khác là một bên đo lượng tin, bên kia đo ngưỡng quyết định. Nó cho bounded-rationality một cơ sở định lượng: nếu kênh xử lý có dung lượng hữu hạn thì việc đơn giản hoá không phải khiếm khuyết mà là điều bắt buộc. Và nó là phát biểu chính xác nhất của map-is-not-the-territory — mọi biểu diễn đều là một phép nén, và phép nén nào cũng phải quyết định bỏ đi cái gì.
