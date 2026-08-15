---
title: Murphy's Law
front: "Vì sao có cảm giác 'điều gì có thể sai thì kiểu gì cũng sẽ sai' đúng vào lúc bạn cần nó nhất?"
back: "Murphy's Law là câu ngạn ngữ dân gian cho rằng nếu có khả năng một việc đi sai, nó rồi sẽ đi sai — và phần lớn sức sống của nó đến từ xu hướng tâm lý nhớ rõ những lần sự cố xảy ra hơn hẳn vô số lần mọi thứ diễn ra suôn sẻ."
level: 2
categories: [heuristic]
links: [illusion-of-control, pessimism-bias, hindsight-bias]
refs: ['https://en.wikipedia.org/wiki/Murphy%27s_law']
strategy: "Khi thiết kế hệ thống hoặc quy trình quan trọng, chủ động giả định lỗi hiếm gặp vẫn sẽ xảy ra ở quy mô đủ lớn (defensive design), thay vì trông chờ vào may mắn để hệ thống luôn vận hành trơn tru."
published: true
---

Murphy's Law thường được trích dẫn như một châm ngôn bi quan về vũ trụ, nhưng nguồn gốc thực tế của nó lại mang tính kỹ thuật hơn nhiều. Tên gọi bắt nguồn từ kỹ sư Edward A. Murphy Jr., người tham gia dự án thử nghiệm giảm tốc bằng tên lửa của Không quân Mỹ (dự án MX981) năm 1949. Sau khi một cảm biến bị lắp sai hướng do lỗi kỹ thuật viên khiến cả thí nghiệm thất bại, Murphy được cho là đã nói một câu đại ý: "nếu có nhiều hơn một cách để làm việc gì đó, và một trong số đó dẫn tới thảm họa, sẽ có người làm theo cách đó." Câu nói ban đầu là một lời cảnh báo về thiết kế hệ thống chống lỗi người dùng, chứ không phải một tuyên ngôn về sự xui xẻo của vũ trụ.

Sức sống lâu bền của câu ngạn ngữ này trong đời sống hằng ngày lại đến từ một cơ chế tâm lý hoàn toàn khác: thiên kiến chọn lọc trong trí nhớ (selection bias). Con người có xu hướng ghi nhớ rất rõ những lần "đúng là xui xẻo" — bánh mì rơi úp mặt bơ xuống sàn, xe hỏng đúng ngày phỏng vấn quan trọng — trong khi hàng nghìn lần mọi việc diễn ra bình thường không để lại dấu ấn nào trong ký ức, vì chúng không có gì đáng chú ý. Kết hợp với hindsight bias, một sự cố sau khi xảy ra thường có cảm giác "đã biết trước sẽ xảy ra", càng củng cố niềm tin rằng vũ trụ có một quy luật ngầm chống lại con người.

Trong kỹ thuật thực tế, tinh thần của Murphy's Law lại được áp dụng một cách nghiêm túc và có chủ đích, đặc biệt trong các hệ thống có rủi ro cao như hàng không vũ trụ và hạ tầng tài chính số. Thiết kế hệ thống thanh toán ngân hàng cần giả định trước rằng máy chủ sẽ có lúc quá tải, mạng sẽ lag đúng lúc cao điểm, và người dùng sẽ nhập sai mã OTP nhiều lần liên tiếp — rồi xây dựng cơ chế dự phòng cho từng kịch bản đó thay vì hy vọng chúng không xảy ra. Nguyên tắc "defense in depth" (phòng thủ theo nhiều lớp) trong bảo mật ngân hàng số chính là hiện thân kỹ thuật của việc coi kịch bản xấu nhất là điều chắc chắn sẽ xảy ra ở một thời điểm nào đó, chứ không phải một khả năng xa vời.

Murphy's Law có quan hệ gần với illusion-of-control — cảm giác bất lực trước "định mệnh xui xẻo" thực chất là mặt trái của niềm tin quá mức vào khả năng kiểm soát mọi việc suôn sẻ khi không có gì bất thường xảy ra. Nó cũng liên hệ tới pessimism-bias, xu hướng đánh giá khả năng xảy ra kết quả xấu cao hơn thực tế trong một số bối cảnh nhất định. Hindsight-bias là cơ chế củng cố trực tiếp: mỗi lần sự cố xảy ra, cảm giác "lẽ ra phải đoán được" khiến câu ngạn ngữ càng có vẻ đúng, dù đó chỉ là ảo giác nhận thức sau sự việc.
