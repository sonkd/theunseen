---
title: Chesterton's fence
front: "Trước khi dỡ bỏ một quy trình 'vô lý', bạn đã thực sự hiểu vì sao nó được dựng lên chưa?"
back: "Chesterton's fence là nguyên tắc tư duy: đừng gỡ bỏ một quy tắc, quy trình hay ranh giới nào cho tới khi hiểu rõ lý do ban đầu nó được dựng lên — dù lý do đó có vẻ không còn cần thiết ở hiện tại."
level: 2
categories: [mental-models]
links: [status-quo-bias, bucket-error]
refs: ['https://en.m.wikipedia.org/wiki/Wikipedia:Chesterton%27s_fence']
strategy: "Trước khi loại bỏ một bước trong quy trình hoặc một điều khoản trong sản phẩm vì thấy nó 'thừa thãi', hãy tìm hiểu ai đã thêm nó vào và trong bối cảnh nào — nếu không tìm ra lý do, mới cân nhắc gỡ bỏ."
published: true
---

Chesterton's fence là nguyên tắc tư duy được đặt tên theo một đoạn văn của nhà văn G. K. Chesterton trong cuốn "The Thing" (1929). Ông kể về hai kiểu người đứng trước một hàng rào chắn ngang đường: người cải cách nóng vội nói "tôi không thấy lý do gì hàng rào này ở đây, dỡ nó đi", còn người thận trọng hơn đáp lại: "nếu anh không thấy lý do nó ở đây, thì càng không nên dỡ nó — hãy đi tìm ra lý do đó trước, rồi quay lại nói cho tôi biết, lúc đó tôi sẽ cân nhắc việc dỡ bỏ".

Điểm mấu chốt của nguyên tắc này không phải là "đừng bao giờ thay đổi", mà là đảo ngược thứ tự thao tác: thay vì hành động rồi giải thích sau, hãy hiểu nguyên nhân trước khi hành động. Rất nhiều quy tắc, quy trình hay ràng buộc tồn tại vì lý do lịch sử không còn hiển nhiên ở thời điểm hiện tại — có thể để giải quyết một sự cố đã từng xảy ra, để tuân thủ một quy định pháp lý cũ, hoặc để cân bằng lợi ích giữa các nhóm mà người mới không nhìn thấy. Gỡ bỏ nó mà không hiểu gốc rễ có nguy cơ lặp lại đúng vấn đề mà nó từng được dựng lên để ngăn chặn.

Trong sản phẩm số và fintech, nguyên tắc này cực kỳ thiết thực khi tái thiết kế các luồng có vẻ "rườm rà" như xác thực hai lớp trước khi chuyển tiền, giới hạn hạn mức giao dịch trong ngày, hay bước xác nhận lại số tài khoản người nhận. Một designer mới có thể muốn bỏ bớt các bước này để "giảm ma sát" (friction), nhưng nếu không tìm hiểu rằng bước xác nhận đó từng được thêm vào sau một đợt lừa đảo chuyển khoản nhầm hàng loạt, việc gỡ bỏ có thể mở lại đúng lỗ hổng đó. Ngược lại, nguyên tắc này cũng không có nghĩa mọi rào cản cũ đều đúng — sau khi điều tra, có thể phát hiện lý do ban đầu đã lỗi thời (ví dụ giới hạn kỹ thuật của hệ thống cũ không còn tồn tại), và lúc đó việc gỡ bỏ hoàn toàn hợp lý.

Chesterton's fence có tinh thần gần với status-quo-bias nhưng đi theo hướng ngược lại: status-quo-bias là xu hướng bám giữ hiện trạng một cách vô thức và thiếu lý do, còn Chesterton's fence là một kỷ luật tư duy chủ động — buộc bản thân phải tìm hiểu lý do trước khi phá vỡ hiện trạng, chứ không mặc định giữ nguyên hay thay đổi. Nó cũng liên quan tới bucket-error, vì cả hai đều là công cụ tư duy phổ biến trong cộng đồng duy lý nhằm làm chậm phản xạ "gạt bỏ ngay lập tức" để nhường chỗ cho việc điều tra kỹ hơn trước khi kết luận.
