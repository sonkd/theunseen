---
title: Feedback Loops
front: Vì sao có những vấn đề càng can thiệp càng phình to, còn có những vấn đề tự lặng đi dù bạn không làm gì?
back: Cấu trúc trong đó đầu ra của một quá trình quay lại làm đầu vào cho chính nó — vòng khuếch đại đẩy hệ đi xa khỏi trạng thái cũ, vòng cân bằng kéo hệ về mức mục tiêu.
level: 3
categories: [mental-models, theory]
tags: [systems, causality, growth]
links: [systems-thinking, goodharts-law, self-fulfilling-prophecy, hedonic-treadmill]
refs: ['https://en.wikipedia.org/wiki/Feedback', 'https://en.wikipedia.org/wiki/Causal_loop_diagram']
strategy: 'Với mỗi chỉ số đang theo dõi, xác định nó nằm trong vòng khuếch đại hay vòng cân bằng và độ trễ là bao lâu — vì hai loại vòng đòi hỏi hai kiểu can thiệp hoàn toàn khác nhau.'
published: true
---

Feedback loop là cấu trúc trong đó kết quả của một quá trình quay ngược lại tác động lên chính đầu vào của quá trình đó. Chỉ có hai loại cơ bản, và phân biệt được chúng là phần lớn giá trị của khái niệm.

Vòng khuếch đại đẩy hệ đi xa hơn theo hướng nó đang đi. Càng nhiều người dùng thì mạng lưới càng giá trị, càng giá trị thì càng kéo thêm người dùng. Càng nhiều nợ kỹ thuật thì mỗi thay đổi càng chậm, càng chậm thì đội càng phải đi tắt, càng đi tắt thì nợ càng dày. Vòng khuếch đại tạo ra tăng trưởng theo cấp số nhân hoặc sụp đổ theo cấp số nhân — cùng một cấu trúc, chỉ khác dấu.

Vòng cân bằng kéo hệ về một mức mục tiêu. Điều hoà nhiệt độ trong phòng, đói và no, giá cả với cung cầu, hay hàng chờ hỗ trợ khi thời gian chờ tăng khiến một phần người dùng bỏ cuộc. Vòng cân bằng tạo ra sự ổn định, và cũng tạo ra sự bướng bỉnh: nó chính là lý do nhiều can thiệp bị hệ thống nuốt chửng mà không để lại dấu vết.

Yếu tố thứ ba là độ trễ, và nó là nguồn gốc của hầu hết hành vi khó hiểu. Khi hệ quả đến chậm hơn nhiều so với hành động, người vận hành có xu hướng can thiệp thêm vì tưởng lần trước chưa đủ, rồi khi tất cả các can thiệp cùng phát tác thì hệ vọt quá đà, rồi bị sửa quá tay theo chiều ngược lại. Đây là cơ chế sinh ra dao động — không cần ai làm sai, chỉ cần độ trễ đủ dài và tay lái đủ nôn nóng. Khái niệm này là trung tâm của điều khiển học từ giữa thế kỷ 20 và của system dynamics sau đó.

Cách áp dụng vào công việc sản phẩm khá cụ thể. Với mỗi chỉ số quan trọng, viết ra một câu: chỉ số này tăng thì điều gì xảy ra tiếp, và điều đó có làm chỉ số tăng thêm hay giảm lại. Nếu tăng thêm, ta đang ở vòng khuếch đại và cần chú ý tới điểm bão hoà cùng rủi ro chạy quá đà. Nếu giảm lại, ta đang ở vòng cân bằng và cần tìm ra thứ đang giữ mức mục tiêu, vì đó mới là chỗ đáng can thiệp. Sau đó ghi độ trễ ước tính, rồi ấn định trước bao lâu mới được đánh giá kết quả — cam kết này chống lại phản xạ can thiệp liên tục.

Ví dụ trong fintech: chương trình giới thiệu bạn bè là vòng khuếch đại rõ ràng, nhưng nó thường bị một vòng cân bằng ẩn chặn lại — chất lượng người dùng mới giảm dần khi vòng lan tới nhóm ngoài phân khúc, kéo tỉ lệ gian lận và chi phí hỗ trợ lên, buộc đội siết điều kiện. Nhìn thấy vòng cân bằng ẩn này trước sẽ tránh được kết luận vội rằng chương trình "hết hiệu quả".

Feedback loops là đơn vị phân tích cơ bản của systems-thinking. Chúng là cơ chế đằng sau self-fulfilling-prophecy, nơi kỳ vọng tạo ra hành vi xác nhận chính kỳ vọng đó, và đằng sau hedonic-treadmill, một vòng cân bằng đưa mức hài lòng trở về đường cơ sở. Chúng cũng giải thích goodharts-law: khi một chỉ số thành mục tiêu, con người tạo ra một vòng phản hồi mới nối thẳng từ chỉ số về hành vi, và vòng đó ăn mòn ý nghĩa ban đầu của phép đo.
