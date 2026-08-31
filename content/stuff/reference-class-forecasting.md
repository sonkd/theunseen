---
title: Reference Class Forecasting
front: Muốn biết dự án của bạn mất bao lâu, hỏi đội ngũ hay hỏi thống kê của một trăm dự án tương tự?
back: Phương pháp dự báo bằng cách xác định một lớp các trường hợp tương tự đã hoàn tất, lấy phân bố kết quả thực tế của lớp đó làm điểm xuất phát, rồi mới điều chỉnh theo đặc thù của trường hợp hiện tại.
level: 4
categories: [theory, mental-models]
tags: [forecasting, probability]
links: [outside-view, planning-fallacy, base-rate-fallacy, calibrated-confidence]
refs: ['https://en.wikipedia.org/wiki/Reference_class_forecasting', 'https://en.wikipedia.org/wiki/Planning_fallacy']
strategy: 'Trước khi ước lượng, định nghĩa lớp tham chiếu và lấy phân bố thực tế của nó; chỉ điều chỉnh khỏi phân bố đó khi nêu được lý do cụ thể và có bằng chứng.'
published: true
---

Reference class forecasting là quy trình biến một trực giác thành một con số có thể kiểm chứng. Thay vì mô tả kế hoạch rồi ước lượng thời gian và chi phí từ bên trong, người dự báo đi tìm một lớp các trường hợp đã hoàn tất đủ giống trường hợp hiện tại, lấy phân bố kết quả thật của lớp đó, và dùng nó làm điểm neo. Đặc điểm quan trọng: điểm xuất phát không phải một con số duy nhất mà là một phân bố, gồm cả phần đuôi.

Nền tảng khái niệm đến từ phân biệt của Kahneman và Tversky giữa góc nhìn bên trong và outside-view. Góc nhìn bên trong dựng dự báo từ chi tiết của kế hoạch, và vì kế hoạch không bao giờ liệt kê được những thứ chưa nghĩ ra, nó có thiên lệch lạc quan hệ thống — chính là planning-fallacy. Góc nhìn bên ngoài bỏ qua chi tiết và hỏi các trường hợp giống thế này thường kết thúc ra sao. Bent Flyvbjerg biến ý tưởng này thành quy trình thực hành cho hạ tầng công, và phương pháp được cơ quan giao thông Anh đưa vào hướng dẫn thẩm định dự án từ giữa thập niên 2000, dưới dạng các hệ số điều chỉnh lạc quan theo loại dự án.

Quy trình gồm ba bước. Một, chọn lớp tham chiếu: đủ rộng để có mẫu ý nghĩa, đủ hẹp để còn tương đồng — đây là bước khó nhất và là chỗ phương pháp dễ bị bẻ cong nhất, vì lớp chọn theo ý muốn sẽ cho kết quả theo ý muốn. Hai, lấy phân bố thực tế của lớp, không phải kế hoạch ban đầu của các trường hợp trong lớp. Ba, điều chỉnh có kỷ luật: chỉ dịch khỏi phân bố khi nêu được đặc thù cụ thể kèm bằng chứng, và ghi lại lý do để sau này kiểm tra.

Trong sản phẩm số, cách dùng rất trực tiếp. Khi ước lượng tác động của một thử nghiệm cải thiện luồng eKYC, lớp tham chiếu là toàn bộ thử nghiệm luồng onboarding đội đã chạy trong hai năm qua. Nếu phân bố thực tế cho thấy trung vị tăng 1,5 điểm phần trăm và phần tư trên là 3 điểm, thì một dự báo tăng 12 điểm cần lý do rất mạnh chứ không chỉ cần nhiệt huyết. Cùng logic áp cho ước lượng lịch phát hành: lấy tỷ lệ trượt hạn thực tế của các phát hành trước thay vì tin vào bản kế hoạch mới nhất.

Phương pháp này là liều thuốc trực tiếp cho base-rate-fallacy, vì nó buộc tỷ lệ nền phải xuất hiện trước khi thông tin cá biệt được nghe. Nó cần calibrated-confidence đi kèm để phần khoảng tin cậy có ý nghĩa, chứ không chỉ dịch điểm ước lượng. Và nó chỉ đáng tin khi lớp tham chiếu được chốt trước, vì đó là lằn ranh giữa dự báo và biện minh.
