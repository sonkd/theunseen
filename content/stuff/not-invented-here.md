---
title: Not invented here
front: '''Not invented here'' là gì, và nó tác động thế nào đến cách bạn nghĩ hoặc ra quyết định?'
back: Xu hướng ưu tiên tự xây dựng giải pháp thay vì dùng công cụ/quy trình đã có sẵn từ người khác, ngay cả khi giải pháp có sẵn tốt hơn hoặc rẻ hơn.
level: 2
categories: [bias]
links: [ikea-effect, status-quo-bias, endowment-effect]
refs: ['https://en.wikipedia.org/wiki/Not_invented_here']
strategy: 'Trước khi quyết định "build" thay vì "buy/reuse", buộc trả lời câu hỏi: nếu công cụ này do chính đội mình tạo ra, mình có đánh giá nó khác đi không?'
published: true
---

Not invented here (NIH) là xu hướng tổ chức hoặc cá nhân ưu tiên tự xây dựng một giải pháp thay vì áp dụng giải pháp đã có sẵn từ bên ngoài, ngay cả khi lựa chọn có sẵn tốt hơn về chi phí, thời gian hoặc chất lượng.

Thuật ngữ xuất hiện từ nghiên cứu quản trị công nghệ những năm 1980, khi các nhà nghiên cứu như Ralph Katz và Thomas Allen quan sát các phòng R&D lớn có xu hướng hệ thống hóa việc coi thường công nghệ do đội khác — kể cả trong cùng công ty — phát triển. Nguyên nhân không đơn thuần là kiêu ngạo: nó bắt nguồn từ sự pha trộn giữa hiệu ứng sở hữu tâm lý (ta đánh giá cao hơn thứ mình tạo ra, gần giống ikea-effect), nỗi lo mất kiểm soát khi phụ thuộc vào bên ngoài, và động lực nghề nghiệp — kỹ sư muốn giải quyết bài toán khó thay vì tích hợp công cụ có sẵn.

Trong ngành công nghệ, NIH là lý do nhiều đội kỹ thuật tự viết lại thư viện mã nguồn mở đã ổn định thay vì dùng nguyên bản, tốn hàng tháng công sức để tái tạo thứ đã tồn tại, thường kèm nhiều lỗi hơn bản gốc do thiếu thời gian kiểm thử tương đương. Ở cấp sản phẩm, NIH thể hiện khi một đội thiết kế từ chối áp dụng design pattern đã được kiểm chứng ở sản phẩm khác trong ngành (ví dụ luồng OTP chuẩn ngành ngân hàng) chỉ vì "chúng ta làm khác". Hệ quả với fintech đặc biệt tốn kém: xây lại một hệ thống KYC hoặc chấm điểm tín dụng từ đầu thay vì dùng nhà cung cấp đã qua kiểm định thường kéo dài time-to-market và tăng rủi ro tuân thủ — chi phí cơ hội mà NIH bias khiến người ra quyết định đánh giá thấp.

NIH có quan hệ gần với ikea-effect — cùng cơ chế "công sức bỏ ra khiến ta đánh giá cao sản phẩm của chính mình" — nhưng ikea-effect là về cảm nhận giá trị sau khi tạo ra, còn NIH là về quyết định trước khi bắt tay vào làm. Nó cũng liên quan tới status-quo-bias khi tổ chức đã đầu tư vào hệ thống nội bộ và ngại thay đổi, cũng như endowment-effect — thứ ta sở hữu, kể cả code do chính mình viết, luôn có vẻ giá trị hơn thứ tương đương của người khác.
