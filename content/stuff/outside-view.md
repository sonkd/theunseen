---
title: Outside View
front: Dự án của bạn có gì đặc biệt đến mức nó sẽ không trễ như 90% dự án tương tự trước đó?
back: Cách ước lượng dựa trên thống kê của lớp các trường hợp tương tự, thay vì dựa trên chi tiết cụ thể và kế hoạch riêng của trường hợp đang xét.
level: 4
categories: [theory, mental-models]
tags: [forecasting, estimation, planning]
links: [planning-fallacy, base-rate-fallacy, calibrated-confidence, regression-to-the-mean]
refs: ['https://en.wikipedia.org/wiki/Reference_class_forecasting', 'https://en.wikipedia.org/wiki/Planning_fallacy']
strategy: 'Bắt đầu mọi ước lượng bằng con số thực tế của mười dự án tương tự gần nhất, rồi mới điều chỉnh theo đặc thù của dự án này — và ghi rõ lý do cho từng lần điều chỉnh.'
published: true
---

Outside view là cách ước lượng bắt đầu từ bên ngoài trường hợp đang xét: xác định lớp tham chiếu gồm những trường hợp cùng loại đã xảy ra, lấy phân phối kết quả thực tế của lớp đó, rồi dùng nó làm điểm neo. Inside view thì làm ngược lại — đi sâu vào chi tiết riêng của trường hợp này, dựng kế hoạch từng bước, cộng thời gian lại, và rút ra một con số.

Daniel Kahneman kể lại nguồn gốc khái niệm qua trải nghiệm của chính ông khi tham gia biên soạn một bộ giáo trình. Cả nhóm ước tính mất khoảng hai năm. Sau đó ông hỏi một thành viên có kinh nghiệm về những nhóm tương tự trước đây: tỉ lệ hoàn thành và thời gian thực tế là bao nhiêu. Câu trả lời là một phần đáng kể các nhóm không bao giờ hoàn thành, còn nhóm nào hoàn thành thì mất bảy tới mười năm. Nhóm biết con số đó, thấy nó đáng ngại, rồi vẫn tiếp tục theo ước lượng cũ. Dự án cuối cùng mất khoảng tám năm. Đây là điểm cay đắng nhất của khái niệm: biết outside view chưa đủ, phải thực sự dùng nó làm điểm xuất phát.

Bengt Flyvbjerg phát triển ý này thành reference class forecasting cho các dự án hạ tầng quy mô lớn, nơi vượt chi phí và trễ tiến độ là quy luật chứ không phải ngoại lệ. Quy trình có ba bước: chọn một lớp tham chiếu đủ tương tự về bản chất nhưng đủ rộng để có số liệu, lập phân phối kết quả thực tế của lớp đó, rồi đặt dự án hiện tại vào phân phối và điều chỉnh có kiểm soát. Cách này đã được đưa vào hướng dẫn thẩm định dự án công ở một số quốc gia.

Lý do inside view thất bại có hệ thống nằm ở chỗ nó chỉ mô phỏng được kịch bản mà ta hình dung ra. Kế hoạch chi tiết cộng thời gian của các bước đã biết, nhưng phần lớn độ trễ thực tế đến từ những thứ không có trong kế hoạch: một phụ thuộc bên ngoài trượt, một yêu cầu pháp lý phát sinh, một người nghỉ việc. Lớp tham chiếu thì đã chứa sẵn tất cả các loại bất ngờ đó dưới dạng thống kê, dù ta không biết cụ thể lần này sẽ là bất ngờ nào.

Trong công việc sản phẩm, cách dùng khá đơn giản và ít ai làm. Trước khi ước lượng một tính năng, mở lại mười lần giao gần nhất của đội và xem tỉ số giữa ước lượng ban đầu và thời gian thực tế; hệ số đó là điểm xuất phát mới. Trước khi dự báo tác động của một thay đổi giao diện, xem phân phối uplift của các thử nghiệm cùng loại đã chạy — con số trung vị thường khiêm tốn hơn nhiều so với kỳ vọng trong tài liệu đề xuất. Việc điều chỉnh khỏi mức nền vẫn được phép, nhưng phải viết rõ lý do và mức điều chỉnh, để lần sau còn kiểm lại được.

Outside view là liều thuốc trực tiếp cho planning-fallacy. Nó chính là việc dùng tỉ lệ nền một cách có kỷ luật, tức chữa base-rate-fallacy ở dạng ứng dụng. Nó cải thiện calibrated-confidence vì nó cho khoảng ước lượng dựa trên dữ liệu thay vì cảm giác. Và nó là hệ quả thực dụng của regression-to-the-mean: những trường hợp trông cực đoan khi nhìn từ bên trong thường trở về gần mức trung bình của lớp khi kết thúc.
