---
title: Goal-Gradient Effect
front: Vì sao chiếc thẻ tích điểm còn hai ô trống làm bạn đi mua cà phê nhiều hơn hẳn lúc thẻ còn trống trơn?
back: Nỗ lực tăng lên khi khoảng cách tới đích thu hẹp - động lực không phụ thuộc vào giá trị phần thưởng mà vào tỷ lệ phần đường còn lại, nên cảm giác gần đích đủ sức đổi hành vi.
level: 2
categories: [bias]
tags: [motivation, decision, progress]
links: [zeigarnik-effect, sunk-cost-fallacy, hyperbolic-discounting, loss-aversion]
refs: ['https://en.wikipedia.org/wiki/Clark_Leonard_Hull', 'https://doi.org/10.1509/jmkr.43.1.39']
strategy: "Muốn người dùng hoàn tất một luồng dài, đừng giảm số bước trước - hãy cho thấy họ đã đi được bao xa, vì nỗ lực phản ứng với phần đường còn lại chứ không với tổng số bước."
published: true
---

Goal-gradient effect được Clark Leonard Hull mô tả từ thập niên 1930 khi quan sát chuột trong mê lộ: chúng chạy nhanh hơn ở những đoạn gần thức ăn hơn là ở đoạn đầu. Giả thuyết của ông, gọi là goal gradient hypothesis, nói rằng sinh vật dồn nỗ lực không đều theo hành trình mà dốc dần về phía đích. Điều đáng chú ý là biến số điều khiển hành vi không phải giá trị phần thưởng, cũng không phải tổng chiều dài hành trình, mà là khoảng cách còn lại tới đích.

Ran Kivetz, Oleg Urminsky và Yuhuang Zheng kiểm chứng lại giả thuyết này ở người trong một nghiên cứu công bố trên Journal of Marketing Research năm 2006. Dữ liệu từ một quán cà phê thật cho thấy khách mua thường xuyên hơn khi thẻ tích điểm của họ càng gần mốc đổi ly miễn phí. Phần thú vị nhất là thí nghiệm về tiến độ ảo: một nhóm nhận thẻ mười hai ô nhưng đã được dập sẵn hai ô, nhóm kia nhận thẻ mười ô trống. Cả hai đều phải mua đúng mười lần, nhưng nhóm có hai ô dập sẵn hoàn tất nhanh hơn. Hai con dấu không có giá trị kinh tế nào đã đổi được hành vi, chỉ bằng cách đổi cảm giác về phần đường đã đi. 

Trong sản phẩm số, hiệu ứng này giải thích vì sao thanh tiến độ không phải trang trí. Một luồng eKYC năm bước có tỷ lệ bỏ giữa luồng rất khác nhau tùy cách hiển thị: không có chỉ báo, người dùng không biết mình đang ở đâu nên mỗi bước đều cảm giác như bước đầu; có chỉ báo rõ, phần nỗ lực còn lại trở nên hữu hạn và đo được. Thủ pháp tiến độ ảo dùng được một cách trung thực: tính những việc người dùng đã làm thật nhưng chưa được ghi nhận - số điện thoại đã xác thực, điều khoản đã đồng ý - thành bước đã hoàn thành, thay vì bắt đầu từ số không.

Ranh giới đạo đức nằm ở chỗ có bịa tiến độ hay không: hiển thị tiến độ sai sự thật là dark pattern, trả giá bằng chỉ số tin cậy - thứ đắt hơn một điểm chuyển đổi. Nên theo cùng lúc tỷ lệ hoàn tất, tỷ lệ bỏ theo từng bước và tỷ lệ quay lại.

Hiệu ứng này cùng họ với zeigarnik-effect, nơi việc chưa xong tự giữ chỗ trong trí nhớ và gây căng thẳng nhẹ tới khi hoàn tất. Nó dễ bị lẫn với sunk-cost-fallacy, nhưng khác biệt rõ: sunk cost là bám vào chi phí đã bỏ, còn goal gradient là phản ứng với phần việc còn lại. Nó cũng là mặt ngược của hyperbolic-discounting, nơi giá trị tụt nhanh khi đích còn xa, và nhận lực đẩy thêm từ loss-aversion vì bỏ dở lúc gần xong bị cảm nhận như một mất mát.
