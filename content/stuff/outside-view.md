---
title: Outside View
front: Dự án của bạn có hoàn cảnh rất đặc thù — nhưng 90% dự án tương tự đều trễ hạn. Bạn tin vào chi tiết hay tin vào thống kê?
back: Góc nhìn bên ngoài là cách ước lượng dựa trên phân phối kết quả của một lớp trường hợp tương tự, thay vì dựa trên chi tiết cụ thể của trường hợp đang xét.
level: 4
categories: [theory, mental-models]
tags: [forecasting, base-rates, estimation]
links: [planning-fallacy, base-rate-fallacy, insensitivity-to-sample-size, regression-to-the-mean]
refs: ['https://en.wikipedia.org/wiki/Reference_class_forecasting', 'https://en.wikipedia.org/wiki/Planning_fallacy']
strategy: 'Bắt đầu mọi ước lượng bằng phân phối kết quả của các trường hợp tương tự, rồi mới điều chỉnh theo đặc thù — và giới hạn mức điều chỉnh, vì đặc thù luôn cảm thấy quan trọng hơn thực tế.'
published: true
---

Outside view là cách tiếp cận ước lượng do Daniel Kahneman và Amos Tversky phân biệt với inside view. Góc nhìn bên trong xây dựng dự báo từ chi tiết của chính trường hợp đang xét: kế hoạch cụ thể, năng lực đội ngũ, các bước đã vạch ra. Góc nhìn bên ngoài bỏ qua phần lớn chi tiết đó và hỏi một câu khác: những nỗ lực thuộc cùng loại này thường kết thúc như thế nào?

Kahneman kể lại nguồn gốc của khái niệm qua một trải nghiệm của chính nhóm ông khi soạn một giáo trình. Khi ước lượng theo cách thông thường, cả nhóm nhất trí sẽ mất khoảng hai năm. Khi một thành viên được hỏi về các dự án tương tự mà ông từng biết, câu trả lời hoàn toàn khác: phần lớn mất bảy tới mười năm và một tỷ lệ đáng kể không bao giờ hoàn thành. Nhóm nghe con số đó, thấy nó không liên quan tới hoàn cảnh của mình, và tiếp tục. Dự án mất khoảng tám năm.

Chi tiết đó minh hoạ đúng cơ chế. Góc nhìn bên trong không sai vì thiếu thông tin — nó thường có nhiều thông tin hơn — mà vì nó thiếu thông tin về thứ không nằm trong kế hoạch. Kế hoạch chỉ chứa những gì ta nghĩ ra được, còn phân phối kết quả thực tế chứa cả những thứ không ai nghĩ tới, và chính nhóm sau mới quyết định độ trễ. Càng biết nhiều về một trường hợp, cảm giác nó đặc thù càng mạnh, và ta càng dễ gạt thống kê đi.

Quy trình áp dụng, được Bent Flyvbjerg phát triển thành reference class forecasting trong quản lý dự án hạ tầng, gồm bốn bước. Một, chọn lớp tham chiếu — tập các trường hợp đủ giống về bản chất và đủ nhiều để có phân phối. Hai, lấy phân phối kết quả thực tế của lớp đó, không phải kế hoạch của chúng. Ba, đặt trường hợp của mình vào phân phối như một điểm mặc định ở mức trung vị. Bốn, chỉ điều chỉnh khi có lý do định lượng được, và ghi rõ mức điều chỉnh để sau này kiểm tra lại.

Khó khăn thực sự nằm ở bước một. Lớp quá hẹp thì không đủ dữ liệu; quá rộng thì mất liên quan. Trong bối cảnh sản phẩm tài chính, ví dụ hữu dụng là ước lượng tỷ lệ chuyển đổi của một luồng eKYC mới: lớp tham chiếu tốt là các luồng eKYC đã triển khai ở cùng phân khúc và cùng mức yêu cầu giấy tờ, chứ không phải "các tính năng đội mình từng làm".

Card này là liều thuốc trực tiếp cho planning-fallacy. Nó là ứng dụng có kỷ luật của tư duy tỷ lệ nền mà base-rate-fallacy mô tả khi vắng mặt. Nó cần insensitivity-to-sample-size làm cảnh báo khi lớp tham chiếu quá nhỏ, và giải thích vì sao regression-to-the-mean là dự báo mặc định hợp lý cho các trường hợp cực đoan.
