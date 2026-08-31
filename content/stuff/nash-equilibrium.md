---
title: Nash Equilibrium
front: Nếu không ai có lợi khi đơn phương đổi ý, tình thế đó có nghĩa là mọi người đang ở phương án tốt nhất không?
back: Trạng thái của một trò chơi trong đó không người chơi nào cải thiện được kết quả bằng cách một mình đổi chiến lược, khi các bên còn lại giữ nguyên — không nhất thiết là trạng thái tốt nhất cho tập thể.
level: 3
categories: [mental-models, theory]
tags: [game-theory, strategy]
links: [prisoners-dilemma, second-order-thinking, moral-hazard, goodharts-law]
refs: ['https://en.wikipedia.org/wiki/Nash_equilibrium', 'https://en.wikipedia.org/wiki/Game_theory']
strategy: 'Khi một hành vi tệ vẫn kéo dài, đừng hỏi ai sai — hãy hỏi mỗi bên đang phản ứng tối ưu với cái gì, rồi đổi khoản chi trả chứ đừng đổi lời kêu gọi.'
published: true
---

Nash equilibrium là một tổ hợp chiến lược trong đó mỗi người chơi đang chọn phương án tốt nhất có thể, xét theo những gì các bên còn lại đang làm. Định nghĩa gọn: không ai có động cơ đơn phương đổi ý. Điều quan trọng — và thường bị bỏ qua — là điều kiện này chỉ nói về sự ổn định, không nói gì về chất lượng. Một trạng thái tồi tệ cho tất cả vẫn có thể là cân bằng, và chính vì thế nó không tự tan.

John Nash chứng minh năm 1950 rằng mọi trò chơi hữu hạn với số người chơi hữu hạn đều tồn tại ít nhất một cân bằng, nếu cho phép chiến lược hỗn hợp — tức là chọn ngẫu nhiên theo một phân bố xác suất. Kết quả này mở rộng lý thuyết trò chơi từ các trò tổng bằng không của von Neumann và Morgenstern sang phạm vi tổng quát hơn nhiều, và mang lại cho Nash giải Nobel Kinh tế năm 1994.

Ví dụ chuẩn mực là prisoners-dilemma: cả hai cùng khai là cân bằng duy nhất, dù cả hai cùng im lặng sẽ tốt hơn cho cả hai. Đây là minh hoạ sắc nét nhất cho khoảng cách giữa ổn định và tối ưu. Một họ ví dụ khác là các trò chơi có nhiều cân bằng, nơi vấn đề không phải động cơ mà là phối hợp: hai bên đều muốn cùng chọn một chuẩn, nhưng không biết bên kia sẽ chọn chuẩn nào.

Cách dùng mô hình này trong công việc gồm ba bước rõ ràng. Một, liệt kê các bên thật sự có quyền hành động — thường nhiều hơn ta tưởng, gồm cả đội nội bộ, đối tác và người dùng. Hai, viết ra khoản chi trả thực tế của mỗi bên, tức là thứ họ được thưởng và bị phạt, chứ không phải thứ họ được yêu cầu làm. Ba, tìm xem tổ hợp hành vi hiện tại có phải cân bằng không; nếu có, mọi lời kêu gọi thay đổi sẽ vô hiệu cho tới khi bảng chi trả đổi.

Trong fintech, khung này giải thích nhiều bế tắc quen thuộc. Khi đội bán hàng được thưởng theo số hồ sơ giải ngân còn đội rủi ro bị phạt theo nợ xấu, hành vi giằng co giữa hai đội chính là một cân bằng; họp thêm không giải quyết được, phải sửa cơ chế thưởng. Tương tự, một thị trường mà mọi ví điện tử đều đốt tiền khuyến mãi là cân bằng tồi mà không bên nào dừng trước được, vì bên dừng đầu tiên mất thị phần ngay lập tức.

Mô hình này đòi hỏi second-order-thinking, vì phải tính tới phản ứng của phản ứng. Nó là nền để hiểu moral-hazard, nơi một bên tối ưu hoá dựa trên rủi ro mà bên khác gánh. Và nó soi rõ goodharts-law: khi chỉ số thành mục tiêu, cân bằng mới hình thành quanh chính chỉ số đó chứ không quanh kết quả mà chỉ số vốn định đo.
