---
title: Prisoner's Dilemma
front: Vì sao hai người cùng hành động "hợp lý" theo lợi ích riêng lại có thể khiến cả hai cùng thiệt hại hơn nếu họ hợp tác với nhau?
back: Mô hình lý thuyết trò chơi trong đó hai bên đều có lựa chọn hợp tác hoặc phản bội — phản bội luôn mang lại lợi ích cá nhân cao hơn bất kể đối phương làm gì, nhưng nếu cả hai cùng phản bội thì kết quả chung tệ hơn hẳn so với khi cả hai cùng hợp tác.
level: 3
categories: [mental-models, theory]
links: [zero-sum-bias, escalation-of-commitment, loss-aversion, bayesian-updating]
refs: ['https://en.wikipedia.org/wiki/Prisoner%27s_dilemma']
strategy: 'Trong quan hệ hợp tác lặp lại (đối tác kinh doanh, đồng nghiệp liên phòng ban), ưu tiên chiến lược "ăn miếng trả miếng" (tit-for-tat): mở đầu bằng hợp tác, sau đó phản chiếu đúng hành động gần nhất của đối phương — vừa khuyến khích hợp tác lâu dài vừa không để bị lợi dụng liên tục.'
published: true
---

Thế lưỡng nan tù nhân mô tả tình huống hai nghi phạm bị bắt giam riêng biệt, không thể trao đổi với nhau, mỗi người phải chọn im lặng (hợp tác với nhau) hoặc khai báo (phản bội đồng phạm để đổi lấy khoan hồng). Nếu cả hai cùng im lặng, cả hai chỉ chịu án nhẹ vì thiếu bằng chứng. Nếu một người khai còn người kia im lặng, người khai được thả tự do còn người im lặng chịu án nặng nhất. Nếu cả hai cùng khai, cả hai đều chịu án trung bình — nặng hơn phương án cùng im lặng nhưng nhẹ hơn phương án bị phản bội một mình. Xét từ góc độ mỗi cá nhân, khai báo luôn là lựa chọn có lợi hơn bất kể đối phương làm gì — nhưng nếu cả hai đều suy luận như vậy, kết quả chung (cả hai cùng khai) lại tệ hơn hẳn so với khi cả hai cùng im lặng.

Mô hình được nhà toán học Merrill Flood và Melvin Dresher phát triển năm 1950 tại RAND Corporation, sau đó nhà toán học Albert W. Tucker đặt tên và diễn giải thành câu chuyện "tù nhân" dễ hiểu hơn. Cốt lõi lý thuyết nằm ở khái niệm cân bằng Nash: trạng thái cả hai cùng phản bội là một điểm cân bằng ổn định vì không ai có động lực đơn phương đổi chiến lược, dù đó không phải kết quả tối ưu cho cả hai (Pareto-tối ưu). Nghiên cứu sau này của Robert Axelrod trong các giải đấu máy tính mô phỏng phiên bản lặp lại (iterated prisoner's dilemma) cho thấy chiến lược đơn giản "tit-for-tat" — hợp tác trước, sau đó bắt chước đúng nước đi gần nhất của đối phương — vượt trội hơn hẳn các chiến lược phức tạp hơn về lâu dài.

Cấu trúc này xuất hiện khắp nơi trong kinh doanh và sản phẩm số: cuộc đua giá giữa các ứng dụng fintech cạnh tranh (mỗi bên giảm phí để giành thị phần, nhưng nếu tất cả cùng giảm thì toàn ngành cùng thiệt hại biên lợi nhuận), hay tình huống các phòng ban trong công ty giữ thông tin riêng thay vì chia sẻ (mỗi phòng ban "an toàn" hơn khi giữ, nhưng công ty nói chung mất hiệu quả nếu ai cũng làm vậy). Hiểu đúng cấu trúc trò chơi giúp thiết kế cơ chế khuyến khích hợp tác thay vì để tất cả rơi vào cân bằng cùng thua — ví dụ xây dựng uy tín thương hiệu dài hạn (biến trò chơi một lần thành trò chơi lặp lại) khiến "hợp tác" (không chơi xấu khách hàng) trở thành lựa chọn có lợi hơn về lâu dài.

Prisoner's dilemma liên hệ chặt với zero-sum-bias — sai lầm coi mọi tương tác là được-mất tuyệt đối trong khi thực ra hợp tác có thể tạo ra tổng lợi ích lớn hơn cho cả hai bên. Nó cũng gắn với escalation-of-commitment khi các bên lún sâu vào vòng xoáy trả đũa lẫn nhau, và với loss-aversion — nỗi sợ bị phản bội và mất mát thường lớn hơn kỳ vọng lợi ích từ hợp tác, khiến nhiều người chọn phản bội trước dù về lý thuyết hợp tác mang lại kết quả tổng thể tốt hơn.
