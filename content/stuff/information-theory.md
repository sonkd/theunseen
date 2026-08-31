---
title: Information Theory
front: Làm sao đo được lượng thông tin trong một câu nói, khi thứ ta đo không phải chữ mà là điều ta chưa biết?
back: Lý thuyết của Claude Shannon định lượng thông tin bằng mức độ bất định được giảm đi — một thông điệp càng khó đoán trước thì càng mang nhiều thông tin.
level: 5
categories: [theory]
tags: [foundational, communication, uncertainty]
links: [signal-detection-theory, magic-number-7-2, bounded-rationality, cognitive-load-theory]
refs: ['https://en.wikipedia.org/wiki/Information_theory', 'https://en.wikipedia.org/wiki/Entropy_(information_theory)']
strategy: 'Khi thiết kế một thông báo hay một chỉ số, hãy hỏi nó giảm bất định của người nhận được bao nhiêu — thứ ai cũng đoán được trước khi đọc thì không mang thông tin, chỉ chiếm chỗ.'
published: true
---

Information theory là khung toán học do Claude Shannon công bố năm 1948 tại Bell Labs, trong công trình về lý thuyết truyền tin. Đóng góp then chốt của nó là tách khái niệm thông tin ra khỏi khái niệm ý nghĩa và biến nó thành một đại lượng đo được. Trong khung này, thông tin của một thông điệp không nằm ở nội dung nó nói gì, mà ở chỗ nó loại bỏ được bao nhiêu khả năng mà người nhận trước đó còn để ngỏ.

Từ đó sinh ra khái niệm trung tâm: entropy. Entropy của một nguồn là mức bất định trung bình trên mỗi thông điệp nó phát ra, đo bằng bit. Một đồng xu cân bằng có entropy một bit mỗi lần tung, vì kết quả hoàn toàn không đoán được. Một đồng xu hai mặt giống nhau có entropy bằng không — biết trước kết quả nên không có thông tin nào được truyền. Hệ quả trực giác: sự kiện càng hiếm thì khi xảy ra càng mang nhiều thông tin, còn thứ luôn luôn xảy ra thì không nói gì.

Ba khái niệm phái sinh định hình gần như toàn bộ hạ tầng số hiện đại. Dư thừa là phần có thể đoán được trong một thông điệp; nén dữ liệu chính là việc loại bỏ dư thừa, và entropy đặt ra giới hạn cứng cho mức nén tối đa không mất mát. Nhiễu là thứ làm sai lệch tín hiệu trên đường truyền. Dung lượng kênh là tốc độ truyền tối đa mà vẫn giữ được sai số nhỏ tuỳ ý — kết quả nổi tiếng nhất của Shannon là chứng minh rằng dung lượng này tồn tại và có thể đạt gần tới bằng mã sửa lỗi, điều mà giới kỹ sư thời đó cho là bất khả thi. Nghịch lý thú vị là để chống nhiễu, ta phải cố tình thêm dư thừa trở lại.

Ảnh hưởng của khung này lan ra ngoài kỹ thuật truyền tin. Tâm lý học nhận thức thập niên 1950 mượn từ vựng của nó để coi con người như một kênh truyền có dung lượng giới hạn, và cách đặt vấn đề đó vẫn còn nguyên trong cách ta nói về tải nhận thức. Thống kê Bayes dùng entropy để đo lượng thông tin kỳ vọng thu được từ một quan sát, tức để trả lời câu hỏi thí nghiệm nào đáng chạy nhất. Học máy hiện đại dùng cross-entropy làm hàm mất mát mặc định cho bài toán phân loại.

Với người làm sản phẩm, giá trị thực dụng nằm ở một câu hỏi: thông điệp này giảm bất định của người nhận được bao nhiêu. Một màn hình xác nhận nhắc lại đúng những gì người dùng vừa nhập không mang thông tin mới; một dòng cảnh báo chỉ hiện khi có bất thường thì mang rất nhiều. Một báo cáo tuần mà ai cũng đoán được nội dung trước khi mở là entropy gần bằng không. Ngược lại, nguyên tắc dư thừa nhắc rằng ở nơi có nhiễu cao — người dùng đang vội, môi trường ồn, thao tác không đảo ngược được — lặp lại thông tin quan trọng qua nhiều kênh là thiết kế đúng chứ không phải thừa.

Information theory là nền toán học cho signal-detection-theory, khung mô tả cách một hệ tách tín hiệu khỏi nhiễu khi phải quyết định dưới bất định. Nó là gốc lịch sử của cách đặt vấn đề trong magic-number-7-2 và cognitive-load-theory, cả hai đều coi năng lực xử lý là một kênh có dung lượng hữu hạn. Và nó cho ngôn ngữ chính xác để nói về bounded-rationality: giới hạn không nằm ở ý chí, mà ở lượng bit mà hệ thống có thể xử lý trong thời gian có sẵn.
