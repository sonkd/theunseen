---
title: Phi Phenomenon
front: Vì sao hai bóng đèn tắt-bật xen kẽ lại khiến bạn "thấy" một đốm sáng di chuyển, dù chẳng có gì thực sự chuyển động?
back: Ảo giác chuyển động trong đó não cảm nhận có một vật thể di chuyển liên tục từ điểm này sang điểm khác, khi thực tế chỉ là hai (hoặc nhiều) kích thích tĩnh xuất hiện và biến mất luân phiên ở các vị trí khác nhau trong thời gian ngắn.
level: 1
categories: [perception]
tags: [illusion, motion, vision]
links: [motion-aftereffect, change-blindness]
refs: ['https://en.wikipedia.org/wiki/Beta_movement']
strategy: 'Khi thiết kế animation chuyển tiếp giữa hai trạng thái UI, tận dụng phi phenomenon để tạo cảm giác mượt mà bằng các khung hình trung gian tối giản — thay vì animate toàn bộ chi tiết, vốn tốn hiệu năng hơn nhiều mà chưa chắc mượt hơn.'
published: true
---

Phi phenomenon xuất hiện khi hai đèn tĩnh đặt cạnh nhau được bật tắt luân phiên với khoảng cách thời gian phù hợp (thường khoảng 60-200 mili giây): thay vì thấy hai đèn nhấp nháy riêng biệt, người xem cảm nhận một đốm sáng duy nhất đang di chuyển mượt mà từ vị trí đèn thứ nhất sang vị trí đèn thứ hai. Đây chính là nguyên lý nền tảng đứng sau toàn bộ ngành công nghiệp điện ảnh và hoạt hình: một chuỗi khung hình tĩnh chiếu liên tiếp đủ nhanh tạo cảm giác chuyển động liên tục, dù thực chất không có gì "di chuyển" giữa các khung hình.

Nhà tâm lý học người Đức Max Wertheimer công bố nghiên cứu này năm 1912, và nó trở thành viên gạch đầu tiên đặt nền móng cho trường phái tâm lý học Gestalt — trường phái nhấn mạnh rằng não nhận thức tổng thể có tổ chức chứ không chỉ ghép nối các mảnh cảm giác rời rạc. Cơ chế đứng sau liên quan tới cách hệ thần kinh thị giác xử lý thông tin theo thời gian: khi hai kích thích xuất hiện đủ gần nhau về không gian và thời gian, não "nội suy" một quỹ đạo chuyển động liên tục để giải thích hợp lý nhất cho chuỗi sự kiện quan sát được — một chiến lược tiến hóa hữu ích để theo dõi vật thể chuyển động trong môi trường tự nhiên nhiều nhiễu.

Ứng dụng thực tế rõ nhất là toàn bộ animation giao diện số: một nút bấm chuyển từ trạng thái này sang trạng thái khác, một thanh trượt di chuyển, hay biểu tượng loading xoay vòng — tất cả đều là chuỗi khung hình tĩnh tận dụng phi phenomenon để tạo cảm giác chuyển động mượt. Hiểu nguyên lý này giúp nhà thiết kế tối ưu hiệu năng: không cần render đầy đủ chi tiết ở mọi khung hình trung gian, chỉ cần đủ điểm mốc quan trọng đúng nhịp thời gian, não người dùng sẽ tự "lấp đầy" phần còn lại thành một chuyển động liền mạch trong nhận thức, dù dữ liệu thực tế thưa hơn nhiều.

Phi phenomenon có quan hệ gần với motion-aftereffect ở việc cả hai đều là bằng chứng cho thấy hệ thống phát hiện chuyển động của não là một cơ chế tính toán chuyên biệt, tách rời khỏi nhận diện hình dạng tĩnh, và có thể bị kích hoạt hoặc đánh lừa độc lập. Nó cũng liên hệ change-blindness theo hướng ngược lại: nếu não giỏi "dựng" chuyển động từ các điểm tĩnh rời rạc đến vậy, thì việc bỏ sót một thay đổi thực sự xảy ra ngoài vùng chú ý cũng dễ hiểu hơn — cả hai đều cho thấy nhận thức về chuyển động và thay đổi không phải một bản ghi thụ động mà là một diễn giải chủ động.
