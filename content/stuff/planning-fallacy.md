---
title: Planning fallacy
front: '''Planning fallacy'' là gì, và nó tác động thế nào đến cách bạn nghĩ hoặc ra quyết định?'
back: We tend to underestimate how long something will take. A version of optimism bias.
level: 2
categories: [mental-models]
links: [optimism-bias, overconfidence-effect, illusion-of-control]
refs: ['https://en.wikipedia.org/wiki/Planning_fallacy']
strategy: 'Ước lượng effort/thời gian một dự án bằng reference class forecasting: lấy dữ liệu thực tế từ 5-10 dự án tương tự đã hoàn thành trong quá khứ, thay vì tự ước lượng from scratch dựa trên kế hoạch lý tưởng.'
published: true
---

Planning fallacy là xu hướng ước lượng thời gian, chi phí hoặc rủi ro của một dự án thấp hơn thực tế đáng kể, ngay cả khi người ước lượng đã biết rõ những dự án tương tự trước đây từng trễ hạn. Thuật ngữ này được Daniel Kahneman và Amos Tversky đặt ra năm 1979, như một hệ quả cụ thể của optimism bias trong bối cảnh lập kế hoạch.

Ví dụ kinh điển nhất là Nhà hát Opera Sydney: dự kiến hoàn thành trong 4 năm với ngân sách 7 triệu AUD, công trình thực tế mất 14 năm và tiêu tốn hơn 100 triệu AUD. Trong nghiên cứu học thuật, một thí nghiệm thường được trích dẫn yêu cầu sinh viên năm cuối ước lượng thời gian hoàn thành luận văn ở ba kịch bản: "tốt nhất", "thực tế", và "xấu nhất". Kết quả: thời gian hoàn thành thực tế trung bình còn vượt cả ước lượng "xấu nhất" mà sinh viên tự đưa ra. Kahneman giải thích cơ chế bằng khái niệm inside view và outside view: khi lập kế hoạch, con người có xu hướng dùng inside view — tập trung vào chi tiết cụ thể của kế hoạch trước mắt, hình dung kịch bản mọi thứ diễn ra suôn sẻ — thay vì outside view, tức nhìn vào dữ liệu thống kê của các dự án tương tự đã từng xảy ra, bất kể chi tiết riêng của chúng là gì.

Trong sản phẩm và vận hành, planning fallacy là nguyên nhân phổ biến khiến roadmap liên tục trễ: một team ước lượng "2 sprint" cho việc migrate design system, dựa trên kế hoạch lý tưởng hóa mọi dependency sẽ sẵn sàng đúng lúc — bỏ qua thực tế rằng những lần migrate tương tự trước đó của chính team luôn phát sinh vấn đề tích hợp không lường trước. Reference class forecasting — kỹ thuật do Bent Flyvbjerg phát triển dựa trên nghiên cứu của Kahneman — đề xuất giải pháp thực dụng: thay vì cố ước lượng chính xác hơn từ đầu, hãy tra cứu phân phối thời gian hoàn thành của các dự án "cùng lớp" (cùng độ phức tạp, cùng loại) đã xảy ra trong quá khứ, và neo ước lượng mới vào phân phối đó thay vì vào cảm giác lạc quan của riêng dự án hiện tại.

Planning fallacy là biểu hiện trực tiếp của optimism-bias trong bối cảnh ước lượng thời gian/nguồn lực. Nó cũng liên hệ chặt với overconfidence-effect — niềm tin quá mức vào độ chính xác của chính ước lượng mình đưa ra, khiến khoảng dao động dự phòng bị co hẹp lại thay vì mở rộng. Và nó thường đi kèm illusion-of-control — niềm tin rằng team có thể kiểm soát hoặc lường trước mọi biến số bên ngoài (dependency, nhân sự, thay đổi yêu cầu), trong khi phần lớn độ trễ dự án đến từ chính những yếu tố nằm ngoài tầm kiểm soát đó.
