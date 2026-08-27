---
title: Bayesian Updating
front: Làm sao để thay đổi niềm tin của mình một cách hợp lý mỗi khi có bằng chứng mới, thay vì giữ khư khư hoặc đảo ngược hoàn toàn?
back: Framework tư duy dựa trên định lý Bayes, trong đó một niềm tin ban đầu (prior) được điều chỉnh có hệ thống thành niềm tin mới (posterior) khi có bằng chứng mới xuất hiện — mức độ điều chỉnh tỷ lệ với độ mạnh của bằng chứng và độ chắc chắn của niềm tin ban đầu.
level: 3
categories: [mental-models, theory]
links: [base-rate-fallacy, confirmation-bias, overconfidence-effect, regression-to-the-mean]
refs: ['https://en.wikipedia.org/wiki/Bayesian_probability', 'https://en.wikipedia.org/wiki/Bayes%27_theorem']
strategy: 'Trước khi diễn giải một bằng chứng mới (kết quả A/B test, phản hồi khách hàng), viết ra rõ ràng niềm tin trước đó (prior) của mình bằng con số phần trăm — rồi tự hỏi bằng chứng này đủ mạnh để dịch chuyển con số đó bao nhiêu, thay vì để nó lật ngược hoàn toàn kết luận chỉ vì một mẫu nhỏ.'
published: true
---

Bayesian updating là quy trình cập nhật niềm tin theo định lý Bayes: bắt đầu từ một xác suất tiên nghiệm (prior probability) phản ánh mức độ tin tưởng ban đầu vào một giả thuyết, sau đó khi quan sát được bằng chứng mới, ta tính xác suất hậu nghiệm (posterior probability) bằng cách kết hợp có trọng số giữa niềm tin cũ và độ mạnh của bằng chứng mới. Điểm mấu chốt là việc cập nhật này không phải "có bằng chứng mới thì bỏ hết niềm tin cũ" hay "bằng chứng mới yếu thì bỏ qua hoàn toàn" — mà là một phép trộn có tỷ lệ, trong đó bằng chứng càng mạnh và niềm tin ban đầu càng yếu thì mức điều chỉnh càng lớn.

Nền tảng toán học xuất phát từ định lý do mục sư kiêm nhà toán học người Anh Thomas Bayes phát triển, công bố sau khi ông mất năm 1763, và được Pierre-Simon Laplace hoàn thiện độc lập sau đó. Trực giác cốt lõi thường bị bỏ qua trong thực hành là vai trò của tỷ lệ nền (base rate): nếu một xét nghiệm y khoa có độ chính xác 99% nhưng căn bệnh chỉ xuất hiện ở 1/10.000 người, một kết quả dương tính vẫn có xác suất là dương tính giả cao đáng ngạc nhiên — vì tỷ lệ nền quá thấp lấn át gần như hoàn toàn độ chính xác của xét nghiệm. Đây chính là lỗi tư duy phổ biến nhất khi con người cố "cập nhật niềm tin" một cách trực giác mà không qua tính toán: bỏ qua tỷ lệ nền và chỉ tập trung vào bằng chứng mới nhất, sống động nhất.

Trong sản phẩm số, tư duy Bayesian là nền tảng của thử nghiệm A/B nghiêm túc: một kết quả test với mẫu nhỏ, khoảng tin cậy rộng không nên khiến đội ngũ đảo ngược hoàn toàn quyết định đã có nhiều bằng chứng trước đó ủng hộ — điều hợp lý là dịch chuyển niềm tin một mức vừa phải và tiếp tục thu thập thêm dữ liệu. Trong đánh giá rủi ro tín dụng hay phát hiện gian lận ở ngân hàng số, mô hình chấm điểm dựa trên nguyên lý Bayesian liên tục cập nhật xác suất một giao dịch là gian lận khi có thêm tín hiệu mới (địa điểm lạ, thiết bị mới), thay vì áp dụng ngưỡng cứng nhắc chỉ dựa trên một tiêu chí đơn lẻ.

Bayesian updating là lời giải trực tiếp cho confirmation-bias — xu hướng chỉ tìm và tin bằng chứng củng cố niềm tin sẵn có — bằng cách buộc phải cân nhắc bằng chứng trái chiều một cách có trọng số thay vì phớt lờ. Nó cũng liên hệ chặt với base-rate-fallacy (lỗi bỏ qua tỷ lệ nền khi phán đoán), overconfidence-effect (tin chắc vào kết luận hơn mức bằng chứng cho phép), và regression-to-the-mean — hiểu đúng ba khái niệm này cùng lúc giúp tránh phần lớn sai lầm phổ biến khi diễn giải dữ liệu và ra quyết định trong điều kiện không chắc chắn.
