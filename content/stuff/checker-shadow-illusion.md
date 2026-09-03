---
title: Checker Shadow Illusion
front: Hai ô trên bàn cờ có cùng một sắc xám chính xác — vì sao bạn không thể bắt mắt mình nhìn thấy điều đó?
back: Trong ảo giác bàn cờ của Adelson, một ô nằm trong vùng bóng đổ và một ô ngoài sáng có độ xám vật lý giống hệt nhau, nhưng hệ thị giác vẫn thấy chúng khác nhau rõ rệt vì nó đang cố suy ra độ phản xạ thật của bề mặt.
level: 1
categories: [perception]
tags: [vision, brightness, context]
links: [color-constancy, size-constancy, muller-lyer-illusion, kanizsa-triangle]
refs: ['https://en.wikipedia.org/wiki/Checker_shadow_illusion', 'https://en.wikipedia.org/wiki/Lightness_constancy']
strategy: 'Khi so sánh hai con số lấy từ hai bối cảnh khác nhau, hãy tách chúng khỏi bối cảnh trước — nếu không, bộ máy diễn giải sẽ tự động "hiệu chỉnh" giúp bạn và bạn sẽ không nhận ra điều đó.'
published: true
---

Checker shadow illusion là hình do Edward Adelson tại MIT công bố năm 1995. Một bàn cờ ô sáng ô tối, một hình trụ xanh lá đặt bên cạnh đổ bóng lên bàn cờ. Ô ký hiệu A nằm ngoài vùng bóng, thuộc nhóm ô tối. Ô ký hiệu B nằm trong vùng bóng, thuộc nhóm ô sáng. Đo bằng máy, hai ô có cùng một giá trị xám. Nhìn bằng mắt, B trông sáng hơn A một cách không thể chối cãi. Và điều gây khó chịu nhất: biết sự thật không làm ảo giác biến mất.

Điểm mấu chốt là hệ thị giác không có nhiệm vụ báo cáo lượng ánh sáng chạm vào võng mạc. Nhiệm vụ của nó là suy ra bề mặt ngoài kia thực chất màu gì — vì đó mới là thông tin hữu dụng để nhận diện vật thể. Ánh sáng tới mắt là tích của độ phản xạ bề mặt và cường độ chiếu sáng, nên muốn tách được cái thứ nhất, não phải ước lượng cái thứ hai. Ở đây nó dùng vài manh mối: vùng có bóng đổ thì được chiếu sáng ít hơn, nên một ô trong bóng mà vẫn phản chiếu chừng ấy ánh sáng thì hẳn phải là bề mặt sáng màu. Kết luận ấy đúng trong thế giới thật, và chính vì nó đúng nên nó vẫn chạy khi ta cố tình dựng cảnh để đánh lừa.

Vì thế Adelson nhấn mạnh đây không phải "thất bại" của hệ thị giác mà là bằng chứng nó đang làm tốt việc của mình. Ảo giác lộ ra thuật toán, không lộ ra lỗi. Cùng nguyên lý ấy giải thích vì sao ta vẫn nhận ra tờ giấy là màu trắng dưới ánh nến vàng hay ánh đèn huỳnh quang xanh.

Ứng dụng gần nhất nằm ở chỗ đọc dữ liệu và thiết kế giao diện. Một sắc độ nền hay một khung bao quanh có thể làm hai giá trị bằng nhau trông lệch hẳn — điều này khiến biểu đồ nhiệt và bảng tô màu theo ngưỡng dễ gây kết luận sai. Ở cấp trừu tượng hơn, cùng một tỷ lệ chuyển đổi 2% trông rất khác khi đặt cạnh một chiến dịch tệ so với khi đặt cạnh một chiến dịch tốt: người xem không đọc con số mà đọc con số đã trừ đi bối cảnh, y hệt cách võng mạc bị trừ đi vùng bóng.

Card này là phiên bản độ sáng của cùng nguyên lý đứng sau color-constancy và size-constancy: tri giác báo cáo thuộc tính suy ra chứ không phải tín hiệu thô. Nó chia họ hàng với muller-lyer-illusion ở chỗ ngữ cảnh hình học và ngữ cảnh chiếu sáng đều bẻ cong phán đoán, và với kanizsa-triangle ở chỗ não bổ sung thứ không có trong dữ liệu.
