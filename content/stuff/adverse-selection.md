---
title: Adverse Selection
front: Vì sao gói bảo hiểm càng hào phóng lại càng thu hút đúng những người sắp cần dùng đến nó nhất?
back: Hiện tượng bên nắm nhiều thông tin hơn về rủi ro của chính mình (thường là rủi ro cao) chủ động tham gia giao dịch nhiều hơn, kéo chất lượng trung bình của cả thị trường đi xuống.
level: 3
categories: [theory]
tags: [economics, risk, information]
links: [moral-hazard, survivorship-bias, risk-compensation]
refs: ['https://en.wikipedia.org/wiki/Adverse_selection', 'https://en.wikipedia.org/wiki/The_Market_for_Lemons']
strategy: 'Khi thiết kế sản phẩm bảo hiểm/tín dụng, dùng câu hỏi sàng lọc + dữ liệu hành vi thay vì chỉ dựa vào tự khai báo để giảm khoảng cách thông tin.'
published: true
---

Adverse selection (lựa chọn ngược) xảy ra khi một bên trong giao dịch biết về rủi ro của chính mình nhiều hơn bên còn lại, và thông tin bất cân xứng đó khiến những người rủi ro cao có động lực tham gia mạnh nhất — trong khi người rủi ro thấp dần rút lui vì thấy giá không còn hời. Kết quả là chất lượng trung bình của thị trường tụt dốc theo thời gian, đôi khi đến mức thị trường sụp đổ hoàn toàn.

Khái niệm này được kinh tế gia George Akerlof hình thức hóa năm 1970 trong bài "The Market for Lemons", lấy thị trường xe cũ làm ví dụ: người bán biết xe mình là "peach" (tốt) hay "lemon" (dở), người mua thì không. Vì không phân biệt được, người mua chỉ sẵn sàng trả mức giá trung bình — mức giá đó lại quá thấp với người bán xe tốt, nên họ rút khỏi thị trường, kéo chất lượng trung bình còn lại tiếp tục giảm, một vòng xoáy tự củng cố. Akerlof nhận giải Nobel Kinh tế năm 2001 một phần nhờ công trình này.

Trong fintech, adverse selection lộ rõ nhất ở sản phẩm bảo hiểm và cho vay tín chấp. Một app bảo hiểm sức khỏe tự khai báo tình trạng bệnh nền, nếu không có cơ chế xác minh, sẽ hút đúng nhóm người biết mình sắp cần dùng bảo hiểm nhất — khiến tỷ lệ chi trả cao hơn dự tính, buộc công ty tăng phí, và vòng xoáy lặp lại: người khỏe mạnh rời đi, người ốm ở lại. Tương tự, nền tảng cho vay ngang hàng nếu chỉ dựa vào hồ sơ tự khai mà thiếu dữ liệu hành vi giao dịch thực tế sẽ dễ thu hút đúng nhóm vay có rủi ro vỡ nợ cao nhất — vì họ là người có động lực vay mạnh nhất khi biết ngân hàng truyền thống đã từ chối mình.

Adverse selection có quan hệ gần với moral-hazard: cả hai đều bắt nguồn từ thông tin bất cân xứng, nhưng adverse selection xảy ra trước giao dịch (ai tham gia), còn moral-hazard xảy ra sau (hành vi thay đổi thế nào một khi đã được bảo vệ). Nó cũng gợi nhắc đến survivorship-bias ở việc dữ liệu quan sát được (khách hàng còn lại) không đại diện cho toàn bộ thị trường ban đầu, và liên quan tới risk-compensation — cách con người điều chỉnh hành vi rủi ro khi cấu trúc chi phí thay đổi. Trong thiết kế sản phẩm, hiểu adverse selection giúp lý giải vì sao "càng hào phóng càng lỗ" đôi khi không phải do vận hành kém, mà do chính cấu trúc thông tin của thị trường.
