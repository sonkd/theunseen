---
title: Optionality
front: Vì sao quyền được chọn — mà không bắt buộc phải chọn — lại có giá trị ngay cả khi bạn không dùng đến nó?
back: Giá trị của việc giữ quyền hành động mà không có nghĩa vụ hành động: khi kết quả bất định, quyền chọn tạo ra một hồ sơ lời lỗ bất đối xứng, giới hạn thiệt hại và bỏ ngỏ phần lợi.
level: 3
categories: [mental-models, theory]
tags: [decision, risk]
links: [antifragility, margin-of-safety, black-swan-theory, barbell-strategy]
refs: ['https://en.wikipedia.org/wiki/Real_options_valuation', 'https://en.wikipedia.org/wiki/Antifragility']
strategy: 'Với mỗi cam kết lớn, hỏi chi phí để giữ quyền rút lui hoặc mở rộng là bao nhiêu — và trả chi phí đó nếu độ bất định còn cao.'
published: true
---

Optionality là giá trị nằm trong quyền được làm một việc mà không bị buộc phải làm. Khác biệt then chốt so với một cam kết là hình dạng của hồ sơ kết quả: người giữ quyền chọn chỉ mất phần phí đã bỏ ra để có quyền đó, trong khi phần lợi khi tình hình thuận lợi không bị chặn trên. Sự bất đối xứng này khiến quyền chọn có giá trị dương ngay cả khi kết quả trung bình bằng không — và giá trị đó tăng theo mức bất định, chứ không giảm.

Ý tưởng được hình thức hoá trong tài chính qua định giá quyền chọn của Fischer Black, Myron Scholes và Robert Merton đầu thập niên 1970, nơi biến động của tài sản cơ sở là một tham số làm tăng giá quyền chọn. Ngành quản trị mượn lại dưới tên real options: quyền trì hoãn, mở rộng, thu hẹp hay từ bỏ một dự án đều là những quyền chọn thực có thể định giá. Nassim Taleb đẩy khái niệm sang triết lý ra quyết định, lập luận rằng người ta có thể hưởng lợi từ bất định mà không cần dự báo đúng, miễn là cấu trúc phơi nhiễm đúng dạng.

Điểm dễ hiểu sai là optionality không đồng nghĩa với việc trì hoãn mọi quyết định. Quyền chọn luôn có phí — thời gian, tiền, chi phí cơ hội, chi phí giữ nhiều lựa chọn mở trong đầu. Giữ quá nhiều quyền mà không bao giờ thực hiện là cách đốt vốn chậm. Câu hỏi đúng là so sánh phí quyền chọn với mức độ bất định còn lại: bất định cao thì trả phí là hợp lý, bất định đã giảm thì nên cam kết.

Trong sản phẩm, cách áp dụng khá cụ thể. Ba bước: một, xác định các quyết định một chiều khó đảo ngược — chọn nhà cung cấp lõi, đổi mô hình dữ liệu khách hàng, ký hợp đồng độc quyền. Hai, tìm cách chuyển chúng thành quyết định hai chiều: hợp đồng ngắn có gia hạn, kiến trúc có lớp trừu tượng, thử nghiệm giới hạn ở một phân khúc. Ba, định giá quyền đó — tốn thêm bao nhiêu công, và mức bất định hiện tại có xứng đáng không. Một đội fintech chạy thử tính năng cho vay trên 5% người dùng trước khi mở rộng đang trả một khoản phí nhỏ để giữ quyền dừng, và khoản phí đó rẻ hơn nhiều so với việc gỡ một sản phẩm đã triển khai toàn hệ thống.

Optionality là cơ chế cụ thể tạo ra antifragility: một hệ thống có nhiều quyền chọn rẻ sẽ hưởng lợi khi biến động tăng. Nó là mặt tấn công của margin-of-safety, vốn lo phần phòng thủ, và cả hai cùng nhắm tới việc sống sót qua những cú sốc mà black-swan-theory cảnh báo là không thể dự báo. Cách triển khai gọn gàng nhất của nguyên tắc này chính là barbell-strategy.
