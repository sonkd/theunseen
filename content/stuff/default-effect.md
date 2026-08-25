---
title: Default Effect
front: Vì sao chỉ đổi một ô tick sẵn từ "không" sang "có" lại tăng gấp đôi số người hiến tạng?
back: Xu hướng giữ nguyên phương án đã được thiết lập sẵn thay vì chủ động thay đổi, vì việc "không làm gì" luôn dễ hơn việc hành động.
level: 2
categories: [bias]
tags: [choice-architecture, product]
links: [status-quo-bias, choice-overload, nudge-theory]
refs: ['https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1324774']
strategy: 'Chọn giá trị mặc định phản ánh đúng lợi ích lâu dài của phần lớn người dùng — mặc định không trung lập, nó luôn dẫn dắt hành vi.'
published: true
---

Default effect là xu hướng người dùng giữ nguyên phương án đã được thiết lập sẵn (mặc định) thay vì chủ động đổi sang phương án khác, ngay cả khi việc đổi chỉ tốn một cú click. Cơ chế đứng sau gồm ba lực: chi phí nỗ lực để thay đổi (dù nhỏ vẫn là một rào cản), tín hiệu ngầm rằng mặc định là lựa chọn được khuyến nghị, và hiệu ứng tham chiếu — một khi đã "sở hữu" trạng thái mặc định, từ bỏ nó tạo cảm giác mất mát.

Bằng chứng kinh điển nhất là nghiên cứu về hiến tạng của Eric Johnson và Daniel Goldstein, công bố trên tạp chí Science năm 2003 với câu hỏi tựa đề "Do Defaults Save Lives?". So sánh các nước châu Âu, họ nhận thấy quốc gia dùng chính sách opt-in (phải chủ động đăng ký hiến tạng) có tỷ lệ đồng ý hiệu lực rất thấp, đôi khi dưới 15%; trong khi quốc gia dùng opt-out (mặc định là đồng ý, phải chủ động từ chối nếu không muốn) có tỷ lệ trên 90% — chênh lệch tới vài chục lần, dù người dân về bản chất không hề khác biệt về thái độ với việc hiến tạng. Trong một thí nghiệm online đi kèm, chỉ đổi mặc định từ opt-in sang opt-out đã đẩy tỷ lệ đồng ý từ 42% lên 82%.

Trong fintech, default effect là công cụ thiết kế mạnh nhất mà cũng dễ bị lạm dụng nhất. Đặt mặc định "tự động gia hạn" cho gói bảo hiểm hay "tự động đầu tư định kỳ" cho quỹ hưu trí giúp tăng tỷ lệ duy trì hành vi tốt (tiết kiệm, bảo vệ tài chính) mà không ép buộc ai. Nhưng cùng cơ chế đó, đặt mặc định "đồng ý chia sẻ dữ liệu" hay "đăng ký gói phí cao hơn" lại biến default effect thành dark pattern — về mặt kỹ thuật người dùng vẫn "tự do lựa chọn", nhưng thực tế phần lớn sẽ không bao giờ đổi.

Default effect là một dạng cụ thể của status-quo-bias áp trong bối cảnh có người thiết kế chủ động đặt mặc định, và là công cụ trung tâm trong nudge-theory của Thaler và Sunstein. Nó cũng liên quan tới choice-overload: khi lựa chọn quá nhiều, người dùng càng có xu hướng rơi về mặc định thay vì tự cân nhắc.
