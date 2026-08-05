---
title: Law of triviality
front: Vì sao một dự án hạt nhân trăm triệu đô được duyệt trong 5 phút, còn màu sơn nhà để xe lại tranh cãi cả buổi họp?
back: Trong nhóm ra quyết định, thời gian tranh luận cho một vấn đề thường tỷ lệ nghịch với tầm quan trọng thực sự của nó — việc càng nhỏ, càng dễ hiểu, càng nhiều người nhảy vào bàn.
level: 2
categories: [mental-models, social]
links: [attribute-substitution, dunning-kruger-effect, law-of-the-instrument]
refs: ['https://en.wikipedia.org/wiki/Law_of_triviality', 'https://fs.blog/bikeshed-effect/']
strategy: 'Trước cuộc họp quan trọng, timebox thời gian cho từng mục nhỏ và giao hẳn quyền quyết định việc vụn vặt cho một người, để năng lượng cả nhóm dồn vào vấn đề thật sự đáng bàn.'
published: true
---

Law of triviality mô tả một nghịch lý quen thuộc trong các nhóm ra quyết định: thời gian và năng lượng tranh luận dành cho một vấn đề thường tỷ lệ nghịch với tầm quan trọng thực sự của nó. Vấn đề càng lớn, càng phức tạp, càng ít người đủ tự tin để chất vấn — nên nó hay được thông qua nhanh, gần như không bàn cãi. Ngược lại, vấn đề càng nhỏ, càng dễ hình dung, càng nhiều người sẵn sàng nhảy vào tranh luận, vì ai cũng cảm thấy mình đủ tư cách để có ý kiến.

C. Northcote Parkinson đưa ra khái niệm này năm 1957, trong cuốn "Parkinson's Law: The Pursuit of Progress", qua câu chuyện giả tưởng về một ủy ban tài chính họp xét ba khoản mục cùng lúc: một nhà máy điện hạt nhân trị giá hàng chục triệu bảng, một nhà để xe đạp cho nhân viên, và ngân sách cà phê hàng năm. Đề án nhà máy điện được duyệt chỉ sau vài phút — gần như không ai trong phòng đủ hiểu vật lý hạt nhân để phản biện. Nhưng khi bàn tới nhà để xe đạp, cuộc họp kéo dài hàng giờ, vì ai cũng biết mái tôn khác mái ngói ra sao và ai cũng muốn góp ý tiết kiệm vài đồng. Từ ví dụ này, thuật ngữ "bikeshedding" ra đời, được kỹ sư phần mềm Poul-Henning Kamp phổ biến trong cộng đồng mã nguồn mở FreeBSD năm 1999, rồi lan rộng khắp giới công nghệ.

Trong công việc hàng ngày, hiệu ứng này lộ rõ nhất ở các buổi review: một quyết định kiến trúc hệ thống ảnh hưởng tới hiệu năng và chi phí vận hành nhiều năm sau được duyệt chỉ sau vài câu hỏi qua loa, trong khi màu sắc nút "Đăng ký" hay câu chữ trong một dòng cảnh báo lỗi có thể khiến cả team tranh luận qua nhiều buổi họp liên tiếp. Vấn đề không phải nút bấm quan trọng hơn kiến trúc, mà vì ai cũng nhìn thấy nút bấm và có gu thẩm mỹ riêng để bàn, còn kiến trúc hệ thống đòi hỏi chuyên môn mà phần lớn người trong phòng không có.

Law of triviality có quan hệ gần với attribute-substitution — cơ chế não bộ âm thầm thay một câu hỏi khó ("kiến trúc này có ổn không?") bằng một câu hỏi dễ hơn mà ai cũng trả lời được ("màu này có đẹp không?"). Nó cũng gần với dunning-kruger-effect, khi người thiếu chuyên môn về vấn đề lớn lại tự tin bàn sâu về những chi tiết nhỏ nằm gọn trong hiểu biết của mình. Còn law-of-the-instrument nhắc một khía cạnh khác của cùng câu chuyện: khi không có công cụ tư duy để giải quyết cái khó, người ta quay sang xử lý cái dễ — dù nó chẳng phải trọng tâm cuộc họp. Cách phòng vệ thực tế nhất là timebox từng mục trong agenda và giao hẳn quyền quyết định những việc vụn vặt cho một người, thay vì để cả nhóm cùng sa vào bàn luận.
