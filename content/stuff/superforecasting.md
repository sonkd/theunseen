---
title: Superforecasting
front: Dự báo tương lai là tài năng bẩm sinh, hay là một kỹ năng đo được và luyện được?
back: "Kết quả từ Good Judgment Project của Philip Tetlock: một nhóm người thường, được chọn và huấn luyện, dự báo sự kiện địa chính trị chính xác hơn cả nhà phân tích tình báo có tài liệu mật."
level: 4
categories: [theory, mental-models]
tags: [forecasting, probability, calibration]
links: [calibrated-confidence, reference-class-forecasting, outside-view, bayesian-updating]
refs: ['https://en.wikipedia.org/wiki/Superforecasting', 'https://en.wikipedia.org/wiki/Brier_score']
strategy: "Ghi dự báo kèm xác suất và thời hạn vào một chỗ không sửa được, rồi tính điểm định kỳ - không có bảng điểm thì không có hiệu chỉnh, chỉ có cảm giác mình dự báo giỏi."
published: true
---

Superforecasting là tên cuốn sách năm 2015 của Philip Tetlock và Dan Gardner, tóm lại kết quả của Good Judgment Project - một cuộc thi dự báo quy mô lớn do cộng đồng tình báo Mỹ tài trợ. Hàng nghìn tình nguyện viên dự báo các sự kiện địa chính trị dưới dạng xác suất có thời hạn, và được chấm bằng Brier score, thước đo vừa phạt sai hướng vừa phạt tự tin quá mức. Qua nhiều mùa, một nhóm nhỏ nổi lên với độ chính xác bền vững chứ không phải may mắn một lần. Nhóm này chính xác hơn khoảng ba mươi phần trăm so với các nhà phân tích tình báo có quyền truy cập tài liệu mật.

Phát hiện quan trọng không phải là có người giỏi dự báo, mà là cái gì làm nên khác biệt. Không phải IQ, không phải bằng cấp, không phải chuyên môn sâu về khu vực. Điểm phân biệt nằm ở cách làm việc: chia câu hỏi lớn thành các câu hỏi nhỏ trả lời được, bắt đầu từ tỷ lệ cơ sở của lớp sự kiện tương tự trước khi tính tới chi tiết của ca này, lấy nhiều góc nhìn độc lập rồi tổng hợp, và - điểm mạnh nhất - cập nhật niềm tin bằng những bước nhỏ, thường xuyên khi có tin mới, thay vì đổi ý một lần thật to hoặc không bao giờ đổi.

Điều này bác bỏ một thế nhị phân sai mà tổ chức hay mắc: hoặc tin chuyên gia, hoặc bỏ dự báo vì tương lai bất định. Lựa chọn thứ ba là biến dự báo thành một quy trình có điểm số. Điều kiện cần là dự báo phải phát biểu dưới dạng kiểm tra được: không phải tỷ lệ chấp nhận sẽ tăng đáng kể, mà tỷ lệ chấp nhận đơn vay tháng mười hai nằm trong khoảng ba mươi tám đến bốn mươi hai phần trăm, với độ tin cậy bảy mươi phần trăm.

Cách triển khai trong một tổ chức sản phẩm khá rẻ. Trước mỗi release lớn, mỗi người liên quan ghi dự báo xác suất cho hai ba chỉ số chính, kèm thời hạn, vào một log không sửa được. Sau mỗi quý, tính Brier score cho từng người và cho cả nhóm. Trong vài vòng, bảng điểm cho thấy những thứ không cuộc họp nào nói ra: ai lạc quan hệ thống, ai bị neo vào quý trước, loại quyết định nào cả nhóm cùng dự báo tệ. Chi phí gần bằng không, và nó đụng trực tiếp vào overconfidence - thứ đắt nhất trong một lộ trình sản phẩm.

Năng lực cốt lõi mà superforecasting đo chính là calibrated-confidence: xác suất nói ra khớp với tần suất xảy ra thật. Hai kỹ thuật nền của nó là reference-class-forecasting và outside-view, cùng buộc người dự báo bắt đầu từ lớp sự kiện tương tự thay vì từ câu chuyện của ca đang xét. Và nhịp cập nhật nhỏ, liên tục chính là bayesian-updating được thực hành bằng tay, bởi người không viết ra công thức nào.
