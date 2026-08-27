---
title: Size Constancy
front: Vì sao một người bạn đi xa dần không hề "co lại" trong mắt bạn, dù ảnh của họ trên võng mạc đang nhỏ đi rất nhanh?
back: Khả năng của não giữ nguyên cảm nhận kích thước thật của một vật thể quen thuộc dù khoảng cách tới nó thay đổi, bằng cách kết hợp kích thước hình chiếu trên võng mạc với thông tin về khoảng cách ước lượng được.
level: 1
categories: [perception]
tags: [vision, depth, adaptation]
links: [ponzo-illusion, color-constancy, weber-fechner-law]
refs: ['https://en.wikipedia.org/wiki/Size_constancy']
strategy: 'Khi thiết kế trải nghiệm AR hiển thị vật thể ảo ở nhiều khoảng cách, đảm bảo các gợi ý chiều sâu (bóng đổ, tỷ lệ với vật xung quanh) đủ rõ ràng — thiếu gợi ý phối cảnh khiến não khó áp dụng size constancy, dễ đánh giá sai kích thước và khoảng cách thật của vật ảo.'
published: true
---

Khi một người đi xa dần khỏi bạn, hình chiếu của họ trên võng mạc mắt co nhỏ lại theo đúng quy luật hình học — xa gấp đôi thì ảnh nhỏ đi một nửa — nhưng bạn không hề cảm thấy người đó đang "co lại" như một hình nộm cao su, mà vẫn cảm nhận đúng chiều cao thật của họ suốt quá trình. Đây chính là size constancy: não không chỉ dựa vào kích thước hình chiếu thô trên võng mạc mà còn nhân bù với ước lượng khoảng cách, để suy ra kích thước thật tương đối ổn định của vật thể.

Cơ chế này được nghiên cứu hệ thống từ đầu thế kỷ 20, gắn liền với các công trình về tri giác không gian của trường phái Gestalt và sau này là lý thuyết "tri giác sinh thái" của James Gibson. Não sử dụng nhiều gợi ý (depth cues) để ước lượng khoảng cách — độ mờ do khí quyển, độ chồng lấp giữa các vật thể, kích thước tương đối so với vật quen thuộc xung quanh, và cả trải nghiệm quá khứ về kích thước "bình thường" của loại vật thể đó (một người trưởng thành hiếm khi cao dưới 1 mét). Khi các gợi ý này bị loại bỏ hoặc đánh lừa — như trong "căn phòng Ames" nổi tiếng, nơi hình dạng phòng bị bóp méo để đánh lừa não về khoảng cách — size constancy sụp đổ hoàn toàn và hai người đứng ở hai góc phòng trông chênh lệch kích thước khổng lồ dù thực tế cao bằng nhau.

Nguyên lý này là nền tảng bắt buộc phải hiểu khi thiết kế trải nghiệm thực tế tăng cường (AR) — ví dụ ứng dụng ngân hàng cho phép "đặt" mô hình 3D minh họa sản phẩm tài chính vào không gian thực qua camera điện thoại. Nếu vật thể ảo thiếu các gợi ý chiều sâu phù hợp (bóng đổ đúng hướng sáng, tỷ lệ đúng với đồ vật thật xung quanh), não người dùng khó áp dụng size constancy như với vật thể thật, dẫn tới cảm giác vật ảo "trôi nổi" sai kích thước hoặc sai khoảng cách, phá vỡ cảm giác chân thực mà AR hướng tới.

Size constancy có quan hệ trực tiếp với ponzo-illusion: chính ảo giác Ponzo là ví dụ về việc lợi dụng gợi ý phối cảnh giả để "đánh lừa" cơ chế size constancy vốn đang cố gắng bù trừ khoảng cách một cách hợp lý. Nó cũng vận hành theo cùng logic bù trừ ngữ cảnh như color-constancy, và cả hai đều minh họa cho weber-fechner-law: cảm nhận của con người về các thuộc tính vật lý luôn được xử lý tương đối, có điều chỉnh theo ngữ cảnh, chứ không bao giờ là một phép đo tuyệt đối thuần túy.
