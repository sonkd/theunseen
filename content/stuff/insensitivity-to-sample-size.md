---
title: Insensitivity to sample size
front: '''Insensitivity to sample size'' là gì, và nó tác động thế nào đến cách bạn nghĩ hoặc ra quyết định?'
back: We will assume that likelihood of things doesn't change as the sample size changes, even though there's more variability in a small sample size than a large sample.
level: 2
categories: [mental-models]
links: [gamblers-fallacy, hot-hand-fallacy, clustering-illusion, base-rate-fallacy]
refs: ['https://en.wikipedia.org/wiki/Insensitivity_to_sample_size', 'http://stats.org.uk/statistical-inference/TverskyKahneman1971.pdf', 'https://fs.blog/mental-model-bias-from-insensitivity-to-sample-size/']
strategy: "Trước khi kết luận điều gì đó từ một mẫu nhỏ (vài chục người dùng test A/B, vài ngày dữ liệu, vài tháng hiệu suất), tự hỏi: nếu mẫu lớn gấp 10 lần, kết luận này có còn đứng vững không?"
published: true
---

Insensitivity to sample size là xu hướng đánh giá xác suất hoặc rút ra kết luận từ một mẫu quan sát mà không cân nhắc mẫu đó lớn hay nhỏ. Về mặt thống kê, mẫu càng nhỏ thì càng dễ dao động xa khỏi tỷ lệ trung bình thực sự của tổng thể — biến thiên lấy mẫu (sampling variability) luôn lớn hơn ở mẫu nhỏ. Nhưng trực giác con người lại đối xử với một mẫu 10 quan sát y hệt một mẫu 10.000 quan sát, miễn là tỷ lệ phần trăm nhìn có vẻ giống nhau, bỏ qua hoàn toàn việc kích thước mẫu quyết định độ tin cậy của con số đó.

Thuật ngữ này gắn liền với nghiên cứu năm 1971 của Amos Tversky và Daniel Kahneman, "Belief in the Law of Small Numbers" — họ chỉ ra rằng ngay cả các nhà nghiên cứu tâm lý học chuyên nghiệp cũng tin sai rằng một mẫu nhỏ đủ đại diện cho tổng thể. Thí nghiệm minh hoạ nổi tiếng nhất là bài toán "hai bệnh viện": một thị trấn có bệnh viện lớn với khoảng 45 ca sinh mỗi ngày và bệnh viện nhỏ với khoảng 15 ca sinh mỗi ngày. Trong một năm, bệnh viện nào ghi nhận nhiều ngày có hơn 60% số bé sinh ra là trai hơn? Đáp án đúng — bệnh viện nhỏ, vì mẫu nhỏ dao động mạnh hơn — chỉ được 22% người tham gia chọn; đa số nghĩ hai bệnh viện có xác suất như nhau, bỏ qua hẳn vai trò của kích thước mẫu. Tversky và Kahneman gọi cơ chế đứng sau là representativeness heuristic: não bộ phán đoán một mẫu "trông giống" tổng thể là đủ, không cần tính tới việc mẫu đó đáng tin đến đâu.

Trong sản phẩm số, đây là cái bẫy kinh điển của A/B testing: một tính năng mới chạy thử trên 50 người dùng, 60% "thích" — con số nghe rất thuyết phục, nhưng với mẫu chỉ 50 người, kết quả gần như vô nghĩa nếu lặp lại với 5.000 người. Dashboard cũng dễ tạo ảo giác tương tự: tỷ lệ chuyển đổi tăng vọt trong một ngày ít giao dịch khiến đội ngũ tưởng chiến dịch marketing "hiệu quả đột phá", trong khi đó chỉ là biến động tự nhiên của một mẫu quá nhỏ. Cùng logic, một nhà quản lý quỹ có 3 tháng lợi nhuận vượt trội dễ bị gắn mác "thiên tài", dù 3 tháng là mẫu quá nhỏ để phân biệt kỹ năng thực sự với may mắn thuần túy.

Insensitivity to sample size là gốc rễ thống kê chung của nhiều lỗi suy luận khác: gamblers-fallacy và hot-hand-fallacy đều xuất phát từ việc coi một chuỗi ngắn — tức một mẫu nhỏ — là đủ để suy ra quy luật, chỉ khác nhau ở hướng đảo chiều hay tiếp diễn; clustering-illusion là hệ quả trực tiếp khi ta "thấy" cụm hay khuôn mẫu trong đúng loại dữ liệu ngẫu nhiên mà mẫu nhỏ hay tạo ra; còn base-rate-fallacy là biến thể liên quan, khi ta bỏ qua tỷ lệ nền của tổng thể chứ không chỉ kích thước mẫu. Cách phòng vệ đơn giản nhất là luôn hỏi mẫu quan sát có đủ lớn để kết luận đáng tin hay chưa, trước khi biến một con số ngẫu nhiên thành một câu chuyện.
