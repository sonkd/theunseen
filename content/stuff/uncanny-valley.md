---
title: Uncanny Valley
front: Vì sao một robot hay nhân vật CGI giống con người gần như hoàn hảo lại khiến bạn thấy rợn hơn là một robot rõ ràng là máy móc?
back: Hiện tượng cảm giác khó chịu, rợn người tăng vọt khi một thực thể nhân tạo (robot, hoạt hình 3D, avatar AI) trông gần giống con người thật nhưng chưa hoàn hảo — khác với thực thể rõ ràng phi thực (hoạt hình cách điệu) hoặc giống người gần như tuyệt đối, vốn được cảm nhận dễ chịu hơn hẳn.
level: 1
categories: [perception]
tags: [robotics, face-perception, unease]
links: [anthropomorphism, pareidolia, mere-exposure-effect]
refs: ['https://en.wikipedia.org/wiki/Uncanny_valley']
strategy: 'Khi thiết kế avatar hoặc trợ lý ảo có gương mặt người, hoặc chọn hẳn phong cách cách điệu rõ ràng phi thực, hoặc đầu tư đủ để đạt độ chân thực gần như tuyệt đối — tránh vùng giữa nơi gần giống nhưng chưa đủ, dễ gây khó chịu ngoài ý muốn.'
published: true
---

Uncanny valley (vùng đáy kỳ lạ) mô tả một đường cong cảm xúc kỳ lạ: khi mức độ giống người thật của một thực thể nhân tạo tăng dần, thiện cảm của người nhìn cũng tăng dần theo — cho tới một ngưỡng thực thể trông "gần giống người nhưng vẫn có gì đó sai sai" (như búp bê sáp, xác chết, robot có da giả), thiện cảm sụt giảm đột ngột thành cảm giác rợn người, ghê sợ. Vượt qua ngưỡng đó, nếu độ chân thực tiếp tục tăng tới mức gần như không phân biệt được với người thật, thiện cảm mới hồi phục trở lại.

Khái niệm được kỹ sư robot học người Nhật Masahiro Mori đề xuất năm 1970 dựa trên quan sát thực nghiệm với robot hình người. Có nhiều giả thuyết giải thích cơ chế: một là "báo động bệnh tật" — khuôn mặt gần giống người nhưng có gì bất thường (da tái, cử động cứng, mắt vô hồn) kích hoạt phản xạ né tránh tiến hóa từng giúp tổ tiên tránh xa người bệnh hoặc xác chết; hai là "vi phạm kỳ vọng" — não đã bật chế độ nhận diện khuôn mặt người với các tiêu chuẩn nghiêm ngặt, nên bất kỳ sai lệch nhỏ nào (cử động mắt không tự nhiên, biểu cảm trễ nhịp) đều bị phát hiện và gắn cờ "có gì không ổn" mạnh hơn hẳn so với vật thể rõ ràng phi người.

Hiệu ứng này là bài toán thiết kế thực sự với các ứng dụng dùng avatar AI hoặc trợ lý ảo có gương mặt — nhiều công ty cố tình chọn phong cách hoạt hình cách điệu, tối giản đường nét (như biểu tượng cảm xúc, nhân vật 2D phẳng) thay vì cố tái tạo khuôn mặt người 3D chân thực, chính vì khó đạt đủ độ hoàn hảo để vượt qua vùng đáy kỳ lạ, và một avatar "gần đúng" gây khó chịu còn tệ hơn một avatar rõ ràng là hoạt hình. Trong lĩnh vực ngân hàng số, trợ lý ảo bằng giọng nói với video mặt người tổng hợp (AI face) cần cân nhắc kỹ hiệu ứng này — một khuôn mặt AI tư vấn tài chính trông gần giống người nhưng cử động hơi máy móc có thể vô tình làm giảm lòng tin của khách hàng, phản tác dụng so với mục tiêu ban đầu.

Uncanny valley liên hệ trực tiếp với anthropomorphism — xu hướng gán đặc điểm người cho vật thể phi người — vì chính khả năng gán ghép đó là tiền đề khiến ta nhìn robot như "gần người" rồi đánh giá mức độ giống. Nó cũng gần với pareidolia ở việc não cực kỳ nhạy với các gợi ý khuôn mặt, dù nhạy đến mức nào cũng có giới hạn: khi tín hiệu khuôn mặt vừa đủ rõ để kích hoạt nhận diện nhưng vừa đủ sai để phá vỡ kỳ vọng, cảm giác dễ chịu quen thuộc (liên hệ mere-exposure-effect) bị đảo ngược thành khó chịu.
