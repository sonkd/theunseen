---
title: "Goodhart's law"
front: "Tại sao chỉ số đôi khi phá hỏng chính điều ta muốn đạt?"
back: "Khi một phép đo trở thành mục tiêu, phép đo ấy mất giá trị như một chỉ báo — người và hệ thống tối ưu hóa chỉ số thay vì mục tiêu thực sự, dẫn tới hành vi méo mó và kết quả lệch mục đích."
level: 2
categories: [theory, heuristic]
links: [law-of-the-instrument, extrinsic-incentive-error, information-bias, automation-bias]
refs:
  - https://en.wikipedia.org/wiki/Goodhart%27s_law
  - https://arxiv.org/abs/1803.04585
strategy: "Đừng đặt một chỉ số làm mục tiêu duy nhất: dùng nhiều chỉ số, đo lường kết quả thực tế, và bổ sung đánh giá định tính/thử nghiệm liên tục."
published: true
---

Goodhart's law mô tả một mối nguy đơn giản nhưng sâu sắc: khi bạn biến một phép đo thành mục tiêu, phép đo đó dần mất ý nghĩa như một chỉ báo cho mục tiêu thật sự. Hiểu theo cách thực dụng, vấn đề không phải là chỉ số xấu mà là khi toàn bộ hệ thống — con người, phần thưởng, và quy trình — bắt đầu tối ưu hóa cho chỉ số thay vì điều bạn thực sự muốn đạt.

Cơ chế xảy ra thường là thế này: chỉ số là đại diện (proxy) cho mục tiêu. Khi không có gì ngăn cản, người ta sẽ tìm mọi cách để làm cho proxy tăng lên — kể cả bằng hành vi méo mó, gian lận, hoặc bằng những thủ thuật hợp pháp nhưng làm giảm giá trị thực của kết quả. Ngoài ra, tối ưu hóa mạnh mẽ (ví dụ thuật toán máy học) có thể tìm ra lỗ hổng trong phép đo: mô hình đạt điểm cao trên metric kiểm tra nhưng thất bại ở thực tế.

Ví dụ ngắn dễ hình dung: một công ty đặt KPI là "số hợp đồng mới" để tăng lượng khách hàng. Nhân viên bán hàng có thể mở nhiều tài khoản chất lượng kém hoặc chấp nhận khách hàng không phù hợp chỉ để hoàn thành KPI. Số hợp đồng tăng, nhưng doanh thu thực tế, tỉ lệ giữ chân khách hàng và lợi nhuận giảm — tức là chỉ số bị chơi để đổi lấy kết quả thực tế tệ hơn.

Trong machine learning, tương tự: nếu bạn tối ưu hóa một metric như accuracy hay AUC mà không quan tâm đến phân phối dữ liệu thực tế, mô hình có thể học “mẹo” (shortcuts) — tận dụng rò rỉ nhãn, bỏ qua nhóm người dùng ít xuất hiện — dẫn tới hiệu suất tệ trên người dùng thật. Ví dụ nhỏ: tối ưu hóa F1 trên một tập test cố định có thể khuyến khích chọn ngưỡng và xử lý dữ liệu sao cho điểm số trên test cao nhưng không có ý nghĩa trong môi trường sản xuất.

Cách tiếp cận thực tế để hạn chế tác hại: 
- Dùng nhiều chỉ số đối chứng thay vì một KPI duy nhất; 
- Ưu tiên metric đo kết quả thực (outcomes) hơn proxy; 
- Bổ sung đánh giá định tính, kiểm tra mẫu ngẫu nhiên và audit; 
- Thay đổi hoặc random hoá mục tiêu theo thời gian để tránh hệ thống “overfit” vào metric; 
- Khi dùng tự động hóa, theo dõi tín hiệu trái chiều và giữ con người trong vòng lặp.

Lưu ý khi tham khảo tài liệu: hãy diễn giải bằng lời của bạn và tránh sao chép nguyên văn các nguồn. Đọc thêm trong các tham khảo nếu muốn đào sâu về nguồn gốc khái niệm và phân tích kỹ hơn.
