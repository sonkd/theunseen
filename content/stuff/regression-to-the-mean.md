---
title: Regression to the Mean
front: Vì sao "nhân viên xuất sắc nhất quý trước" thường làm việc bình thường hơn ở quý sau?
back: Hiện tượng thống kê khi một kết quả cực đoan có xu hướng được nối tiếp bởi một kết quả gần với mức trung bình hơn ở lần đo tiếp theo, thuần túy do ngẫu nhiên chứ không phải nhân quả.
level: 2
categories: [fallacy, theory]
tags: [statistics, decision]
links: [gamblers-fallacy, hot-hand-fallacy, illusory-correlation]
refs: ['https://en.wikipedia.org/wiki/Regression_toward_the_mean']
strategy: 'Trước khi kết luận một can thiệp (thưởng, phạt, thay đổi chính sách) có hiệu quả, luôn hỏi: nếu không làm gì cả, kết quả có tự "hồi quy" về mức trung bình không?'
published: true
---

Regression to the mean là hiện tượng khi một kết quả cực đoan — cao bất thường hoặc thấp bất thường — được đo lại lần nữa, kết quả lần sau có xu hướng gần với mức trung bình hơn, đơn thuần vì thành phần may rủi trong lần đo đầu khó lặp lại nguyên vẹn. Vấn đề là não bộ con người không nhìn nhận đây là quy luật thống kê thuần túy, mà thường gán cho nó một nguyên nhân — "cậu ấy đã hết duyên", "chính sách mới có tác dụng" — dù thực chất không cần bất kỳ can thiệp nào cũng xảy ra đúng như vậy.

Khái niệm do Francis Galton phát hiện cuối thế kỷ 19 khi nghiên cứu chiều cao cha mẹ và con cái: những người cha rất cao có xu hướng sinh con thấp hơn mình (dù vẫn cao hơn trung bình), và ngược lại, cha thấp sinh con cao hơn mình. Galton gọi đây là "hồi quy về mức tầm thường" (regression towards mediocrity) — thuật ngữ "regression" trong thống kê học ra đời từ đây. Cơ chế đơn giản: một kết quả cực đoan thường là tổng hợp của năng lực thật cộng với một phần may rủi; ở lần đo tiếp theo, may rủi khó lặp lại theo đúng hướng cũ, nên kết quả trôi về gần trung bình hơn. Ví dụ kinh điển là "lời nguyền bìa tạp chí Sports Illustrated": vận động viên xuất hiện trên bìa sau một mùa giải xuất sắc thường thi đấu kém hơn ở mùa sau — không phải vì bị nguyền, mà vì phong độ đỉnh cao vốn khó duy trì.

Nhà tâm lý học Daniel Kahneman kể lại một khoảnh khắc "eureka" khi huấn luyện phi công: giáo viên bay nhận thấy khen ngợi học viên sau một cú xử lý đẹp thường khiến lần sau họ bay tệ hơn, còn quát mắng sau một lần bay tệ lại khiến lần sau tốt hơn — kết luận sai lầm là "phạt hiệu quả hơn khen", trong khi thực chất đó chỉ là regression to the mean: màn trình diễn cực tốt hay cực tệ đều có xu hướng được nối tiếp bởi màn trình diễn trung bình hơn, bất kể phản hồi nào được đưa ra. Trong sản phẩm và tăng trưởng, sai lầm tương tự xảy ra khi một chiến dịch marketing được tung ra ngay sau một tuần có chỉ số bất thường thấp — số liệu tuần sau tự nhiên "cải thiện" khiến đội ngũ nhầm tưởng chiến dịch có tác dụng. Cách phòng vệ chuẩn là dùng nhóm đối chứng (control group) để tách hiệu ứng can thiệp thật ra khỏi hồi quy tự nhiên.

Regression to the mean khác về bản chất với gamblers-fallacy và hot-hand-fallacy — cả hai đều là ngộ nhận về tính độc lập của các sự kiện ngẫu nhiên, trong khi regression to the mean là một hiện tượng thống kê có thật, chỉ bị diễn giải sai thành nhân quả. Nó cũng là nguồn gốc phổ biến của illusory-correlation, khi người quan sát gán một mối liên hệ nhân quả cho hai sự kiện chỉ đơn thuần trùng hợp về mặt thống kê.
