#!/usr/bin/env python3
"""Render thumbnail 128x128 cho stuff card chưa có ảnh.

Nguồn: docs/theunseen_illustration_prompt_library.xlsx, sheet `Article Index`.
Idempotent: bỏ qua mọi card đã có public/assets/stuff/<slug>.png.

    python3 scripts/illustrations/render_thumbs.py [--limit 10] [--dry-run]
"""
import argparse
import hashlib
import io
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import openpyxl                      # noqa: E402
import cairosvg                      # noqa: E402
from illus import thumb, SHAPE_MAP   # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
XLSX = os.path.join(ROOT, "docs", "theunseen_illustration_prompt_library.xlsx")
ASSETS = os.path.join(ROOT, "public", "assets", "stuff")
CONTENT = os.path.join(ROOT, "content", "stuff")

# Override thủ công khi shape trong xlsx rõ ràng sai với nội dung card.
# Cột Hero shape trong xlsx dồn ~58% corpus vào hierarchy + branching (README của
# chính file ghi đây là "design hypothesis"), nên phải chẩn đoán lại theo `back`
# của từng card. slug -> (metaphor, "lý do")
OVERRIDES = {
    "abilene-paradox": (
        "cycle",
        "vòng phản hồi tự củng cố — im lặng của mỗi người được người kế tiếp đọc thành "
        "đồng thuận; dùng cycle thay network để không trùng hình với apophenia"),
    "actor-observer-bias": (
        "mirror",
        "concept object: cùng MỘT hành vi soi qua hai khung quy kết (mình=hoàn cảnh / "
        "người khác=tính cách). mirror sát nghĩa hơn contrast vì contrast chỉ nói 'hai thứ khác nhau', "
        "còn ở đây phải thấy được là cùng một sự việc"),
    "adverse-selection": (
        "funnel",
        "thị trường bị sàng lọc lệch — nhóm rủi ro cao tự chọn tham gia và đọng lại, "
        "không phải quan hệ cha-con"),
    "affect-heuristic": (
        "coverage_sphere",
        "một tín hiệu cảm xúc duy nhất phủ lên toàn bộ đánh giá rủi ro/lợi ích"),
    "affective-forecasting": (
        "proportion",
        "focalism: cảm xúc hiện tại chiếm tỉ trọng quá lớn trong bức tranh tương lai — "
        "proportion đọc rõ hơn contrast và không trùng với actor-observer-bias"),
    "ambiguity-effect": (
        "spectrum",
        "dải từ biết rõ xác suất tới mù mờ; mức né tăng dần theo độ mơ hồ"),
    "anchoring": (
        "pull",
        "concept object: một khối nặng kéo lệch toàn bộ ước lượng còn lại. divergence chỉ ra "
        "'một điểm rẽ nhiều nhánh' — thiếu mất lực kéo, vốn là bản chất của anchoring"),
    "anthropomorphism": (
        "overlap_phases",
        "ranh giới người / không-người bị chồng lấn, không phải phân loại tầng bậc"),
    "antifragility": (
        "threshold",
        "vượt ngưỡng biến động thì hệ mạnh lên thay vì vỡ — đúng định nghĩa tipping point"),
    "apophenia": (
        "network",
        "áp một mạng liên kết lên các điểm vốn rời rạc"),

    # ---- batch #2 (2026-08-27) — xlsx gán 4 hierarchy + 5 divergence + 1 cycle,
    # tức 9/10 card sẽ nhận đúng 2 hình. Chẩn đoán lại toàn bộ theo `back`.
    "appeal-to-novelty": (
        "balance",
        "concept object: hai thứ giống hệt nhau, khác biệt duy nhất là tuổi, nhưng cán cân "
        "vẫn nghiêng về phía 'mới' — divergence không diễn được sự thiên lệch này"),
    "appeal-to-probability-fallacy": (
        # sửa ở batch #3: bản proportion trùng byte với base-rate-fallacy (cùng hue amber),
        # mà base-rate-fallacy mới là card phần/tổng đúng nghĩa. threshold cũng sát nghĩa hơn.
        "threshold",
        "một xác suất chưa tới 100% bị làm tròn thành 'chắc chắn' khi vượt qua một ngưỡng chủ "
        "quan — đúng nghĩa tipping point. amber ở đây phân biệt được với antifragility (mint)"),
    "argument-from-fallacy": (
        "hierarchy",
        "kết luận treo dưới lập luận: cắt nút cha thì nhánh con bị coi là rơi theo. "
        "Đây là ca hiếm mà hierarchy của xlsx thực sự đúng"),
    "armchair-fallacy": (
        "veil",
        "concept object: ràng buộc, dữ liệu và trade-off của người trong cuộc bị che khuất — "
        "cái không nhìn thấy mới là nguồn của sự tự tin sai chỗ"),
    "attentional-bias": (
        "beam",
        "concept object: chú ý dồn vào một thứ khiến nó nổi bật lên, phần còn lại tối đi. "
        "Tần suất thật không đổi, chỉ có vùng được rọi sáng thay đổi"),
    "attribute-substitution": (
        "contrast",
        "một câu hỏi khó bị đánh tráo bằng một câu hỏi dễ — hai khối có độ phức tạp hình học "
        "trái ngược, đặt thay chỗ nhau"),
    "authority-bias": (
        "contrast",
        "một nguồn quyền lực đứng như một khối nặng đối lập với toàn bộ bằng chứng còn lại — "
        "đổi từ pull sang contrast vì pull+mint đã trùng byte với anchoring (anchoring giữ pull, "
        "đúng nghĩa 'kéo lệch ước lượng' hơn vì có một con số neo cụ thể, còn ở đây là trọng "
        "lượng của nguồn phát ngôn, không phải một điểm neo)"),
    "automation-bias": (
        "gate",
        "concept object: chỉ thông tin đến từ hệ thống tự động mới lọt qua cổng; "
        "thông tin trái ngược dù đúng vẫn bị chặn"),
    "availability-cascade": (
        "echo",
        "concept object: chính sự lan truyền lặp lại tạo ra cảm giác đáng tin, không phải bằng chứng. "
        "echo sát hơn cycle vì cascade là khuếch đại một chiều, không phải vòng khép kín"),
    "availability-heuristic": (
        "funnel",
        "rất nhiều ký ức tồn tại, nhưng chỉ những thứ dễ bật ra trong đầu mới lọt qua để trở "
        "thành phán đoán về tần suất/nguy hiểm — đổi từ spectrum sang funnel vì spectrum+amber "
        "đã trùng byte với ambiguity-effect (ambiguity-effect giữ spectrum, đúng nghĩa 'dải liên "
        "tục từ biết rõ tới mù mờ' hơn, còn ở đây bản chất là một phễu lọc theo độ dễ nhớ)"),

    # ---- batch #3 (2026-08-28) — xlsx gán 5 hierarchy + 4 branching + 1 proportion.
    # Chỉ 1/10 (base-rate-fallacy) là đúng. Thêm 2 concept object mới: `rebound`, `odd_one_out`
    # (registry 24 -> 26) vì không hình nào trong 24 hình cũ diễn được hai quan hệ đó.
    "backfire-effect": (
        "rebound",
        "concept object MỚI: đính chính đập vào rào cản bản sắc rồi bật ngược — niềm tin sai "
        "chẳng những không giảm mà còn đậm hơn. Không hình nào trong registry cũ diễn được "
        "'kết quả đi ngược ý định'; divergence chỉ nói 'một điểm rẽ nhiều nhánh'"),
    "bandwagon-effect": (
        "pull",
        "concept object: đám đông là một khối có trọng lực — càng đông thì lực hút càng mạnh, "
        "cá nhân bị kéo vào vì khối lượng chứ không vì bằng chứng. hierarchy của xlsx sai hẳn: "
        "ở đây không có quan hệ cha-con nào"),
    "barnum-effect": (
        "nested_scope",
        "một mô tả phủ được gần như mọi người nhưng được đọc thành cái lõi riêng của một người: "
        "vòng ngoài = ai cũng đúng, lõi = 'đúng với riêng tôi'"),
    "base-rate-fallacy": (
        "proportion",
        "giữ nguyên xlsx — ca hiếm mà cột Hero shape đúng: cả bài là quan hệ phần/tổng, "
        "lát cắt dương tính thật quá nhỏ so với khối dương tính giả"),
    "belief-bias": (
        "fracture",
        "concept object: cấu trúc lập luận và kết luận lẽ ra phải khớp theo logic, nhưng ở đây "
        "lệch nhau — và ta vẫn chấp nhận vì kết luận nghe đúng. hierarchy đã dùng cho "
        "argument-from-fallacy với đúng nghĩa cha-con nên không dùng lại ở đây"),
    "bias-blind-spot": (
        "balance",
        "concept object: chuẩn kép — cùng một loại bằng chứng, cân về phía người khác thì nặng "
        "trịch, về phía mình thì nhẹ tênh. Đã loại 2 phương án trước vì render ra ảnh TRÙNG BYTE "
        "với card cũ cùng hue amber: veil đụng armchair-fallacy, mirror đụng actor-observer-bias"),
    "bizarreness-effect": (
        "odd_one_out",
        "concept object MỚI: nền đồng nhất là MỘT PHẦN của cơ chế — card nói rõ hiệu ứng biến "
        "mất nếu cả danh sách đều kỳ lạ. contrast chỉ nói 'hai thứ khác nhau', không có nền"),
    "black-swan-theory": (
        "tail_event",
        "concept object MỚI: đuôi phân phối — chuỗi biến cố thường xuyên nhưng nhỏ, và một biến "
        "cố hiếm có độ lớn áp đảo nằm tách hẳn. spectrum (thử đầu) bị loại vì đã có ambiguity-effect "
        "và availability-heuristic dùng, cả ba cùng hue amber sẽ ra ba thumbnail giống hệt nhau; "
        "threshold thì đụng antifragility — card anh em của Taleb"),
    "bucket-error": (
        "overlap_phases",
        "các mệnh đề lẽ ra độc lập bị chồng vào chung một vùng — chạm vào vùng giao thì cả hai "
        "cùng bị đụng, nên sửa một mảnh nhỏ bị cảm nhận như phủ nhận cả khối"),
    "bystander-effect": (
        "divergence",
        "khuếch tán trách nhiệm: một tình huống cần giúp bị chia thành nhiều phần cho nhiều "
        "người, càng nhiều nhánh mỗi nhánh càng loãng cho tới khi không ai hành động"),
    "cathedral-effect": (
        "spectrum",
        "trần thấp → trần cao là một dải liên tục, và kiểu xử lý thông tin trượt dần theo dải đó "
        "(cụ thể → trừu tượng). hierarchy sai vì không có quan hệ cha-con nào ở đây, chỉ có một "
        "biến độc lập kéo một biến phụ thuộc theo mức độ"),
    "change-blindness": (
        "beam",
        "chú ý dồn hết vào một nhiệm vụ khiến phần còn lại của cảnh (kể cả thay đổi rõ ràng) "
        "chìm vào tối — đúng nghĩa đen của beam, không phải quan hệ cha-con"),
    "cheerleader-effect": (
        "halo_spill",
        "ấn tượng trung bình của cả nhóm lan sang cách đánh giá từng khuôn mặt riêng lẻ, khiến "
        "khuôn mặt gốc 'ăn theo' vẻ hấp dẫn của trung bình nhóm. nested_scope sai vì đây không "
        "phải quan hệ lồng nhau mà là một ấn tượng tràn/lan sang đánh giá lân cận"),
    "chestertons-fence": (
        "veil",
        "lý do dựng hàng rào không biến mất, chỉ đang bị che khuất khỏi người muốn dỡ nó — đúng "
        "nghĩa veil (thông tin bị che, không phải không tồn tại), không phải quan hệ cha-con"),
    "choice-overload": (
        "funnel",
        "nhiều lựa chọn đổ vào nhưng số quyết định chốt được lại ít đi — hội tụ giảm dần đúng "
        "kiểu funnel. divergence bị loại vì hướng đi ngược lại: đây là hội tụ, không phải rẽ nhánh"),
    "choice-supportive-bias": (
        "balance",
        "sau khi chọn, cán cân đánh giá bị đẩy lệch thêm về phía đã chọn (khen thêm) và lệch xa "
        "phía đã từ chối (chê thêm) — một cán cân có hướng, không phải một điểm rẽ nhiều nhánh"),
    "circle-of-competence": (
        "nested_scope",
        "một lõi (điều thực sự biết rõ) nằm lọt bên trong một vùng ngoài rộng hơn (điều tưởng là "
        "biết, hoặc không biết) — quyết định chỉ an toàn trong lõi. hierarchy sai vì không có "
        "cấp bậc, chỉ có ranh giới bao trong-ngoài"),
    "clustering-illusion": (
        "echo",
        "một chuỗi kết quả lặp lại (thắng liên tiếp) được khuếch đại thành cảm giác có quy luật "
        "— đúng cơ chế echo (lặp lại → khuếch đại), không phải một điểm rẽ nhiều nhánh"),
    "cognitive-dissonance": (
        "fracture",
        "hai mảnh lẽ ra phải khớp (niềm tin và hành động) bị lệch nhau, gây khó chịu cho tới khi "
        "một trong hai bị chỉnh lại — đúng nghĩa fracture (bất nhất), không phải cha-con"),
    "cognitive-load-theory": (
        "threshold",
        "bộ nhớ làm việc xử lý tốt cho tới một ngưỡng, vượt ngưỡng đó thì hiểu bài sụp đổ — "
        "tipping point rõ ràng, không phải quan hệ cha-con"),

    # ---- batch #5 (2026-09-05) — xlsx gán 7/10 card là hierarchy. Không card nào
    # trong 10 card này là quan hệ cha-con, nên chẩn đoán lại toàn bộ theo body.
    # Thêm 3 concept object mới (registry 27 -> 30): gap_fill, granularity, cue_lock.
    "confabulation": (
        "gap_fill",
        "concept object MỚI: não không nhớ sai một cách lộ liễu — nó VÁ khoảng trống bằng "
        "chi tiết hợp lý rồi đọc lại toàn bộ như một ký ức liền mạch. Không hình nào trong "
        "registry cũ diễn được 'chỗ hổng bị lấp bằng vật liệu lạ': fracture để lộ chỗ lệch, "
        "veil chỉ che chứ không thay thế"),
    "confirmation-bias": (
        "cycle",
        "vòng tự củng cố: niềm tin quyết định bằng chứng nào được tìm và giữ, bằng chứng đó "
        "lại làm niềm tin chắc thêm. gate (sàng lọc) sát nghĩa hơn về cơ chế nhưng gate+amber "
        "đã thuộc automation-bias nên sẽ ra ảnh trùng byte"),
    "congruence-bias": (
        "gate",
        "khác confirmation-bias ở chỗ thiên lệch nằm ngay trong THIẾT KẾ phép thử: chỉ phép "
        "thử khớp với giả thuyết mới được cho chạy, nên đầu ra gần như chắc chắn là xác nhận. "
        "nested_scope cũng đúng nghĩa (quy luật giả định là tập con) nhưng nested_scope+mint "
        "đã có barnum-effect và circle-of-competence"),
    "conjunction-fallacy": (
        "nested_scope",
        "'A và B' là tập con nằm gọn trong 'A' nhưng lại được chấm xác suất cao hơn — quan hệ "
        "bao hàm là toàn bộ nội dung của card. proportion sát nhưng proportion+amber đã thuộc "
        "base-rate-fallacy"),
    "conservatism": (
        "layers",
        "đính chính được ĐẮP THÊM lên chứ không thay thế: lớp niềm tin cũ vẫn nằm dưới và vẫn "
        "ánh lên qua các lớp mới (fill-opacity làm đúng việc đó). Phân biệt với "
        "continued-influence-effect cùng batch: ở đây vấn đề là biên độ cập nhật thiếu, "
        "không phải sự bất nhất giữa lời nói và suy luận"),
    "continued-influence-effect": (
        "fracture",
        "niềm tin có ý thức đã sửa (người ta nhắc lại đúng lời đính chính) nhưng mô hình "
        "nhân-quả ngầm thì chưa — hai mảnh lẽ ra phải khớp lại lệch nhau. Không dùng rebound "
        "vì rebound là backfire-effect (niềm tin sai đậm THÊM), còn ở đây nó chỉ dai dẳng"),
    "contrast-effect": (
        "contrast",
        "giữ nguyên xlsx — ca hiếm mà cột Hero shape đúng, và đây là card contrast đúng nghĩa "
        "nhất trong corpus: cùng một vật, đặt cạnh vật khác thì đọc ra giá trị khác"),
    "cross-race-effect": (
        "granularity",
        "concept object MỚI: cơ chế là ĐỘ PHÂN GIẢI tri giác, không phải tỉ trọng (proportion "
        "của xlsx sai hẳn). Cùng một số lượng gương mặt: nhóm quen thì phân giải được thành "
        "từng cá thể, nhóm lạ thì nhoè thành một khối đồng nhất. Cố ý KHÔNG dùng in_out_ring "
        "để dành hình đó cho in-group-bias và out-group-homogeneity-bias"),
    "cryptomnesia": (
        "mirror",
        "cùng MỘT nội dung xuất hiện hai lần dưới hai nhãn khác nhau: lần đầu là thứ đã đọc/"
        "nghe, lần sau quay lại mà mất nhãn nguồn nên được đọc thành 'ý tưởng của mình'. "
        "mirror là hình duy nhất diễn được 'một sự việc, hai cách quy kết'"),
    "cue-dependent-forgetting": (
        "cue_lock",
        "concept object MỚI: card nói rõ ký ức VẪN CÒN NGUYÊN, chỉ thiếu cue để truy xuất. "
        "veil (bị che) và gate (bị chặn) đều sai cơ chế, và cả hai đều đã dùng ở hue amber. "
        "Ở đây nội dung hiện đầy đủ, cái thiếu là mảnh khớp nằm tách hẳn bên ngoài"),

    # ---- batch #6 (2026-09-06) — xlsx gán 8/10 card là branching. Không card nào
    # trong 10 card này là "một điểm rẽ nhiều nhánh", nên chẩn đoán lại toàn bộ.
    # Thêm 6 concept object mới (registry 30 -> 36): depletion, foil, latch,
    # dilution, reference_kink, juxtaposition. Lý do phải thêm nhiều: 5 card mint và
    # 5 card amber của batch này rơi vào nhóm quan hệ mà 30 hình cũ không có
    # (cạn kiệt, mồi nhử, quán tính mặc định, loãng trách nhiệm, bất đối xứng quanh
    # mốc, so sánh cạnh nhau vs riêng lẻ) — dùng lại hình cũ sẽ ra ảnh TRÙNG BYTE
    # với card không liên quan về nghĩa.
    "curse-of-knowledge": (
        "veil",
        "cái người nghe THIẾU thì vô hình với người nói — kiến thức của chính người nói "
        "là tấm màn. Đây là mặt đối của armchair-fallacy (veil+amber), nên dùng veil+mint "
        "để cùng họ nghĩa mà không trùng byte. branching sai hẳn: không có điểm rẽ nào"),
    "decision-fatigue": (
        "depletion",
        "concept object MỚI: chất lượng giảm dần vì chính chuỗi quyết định trước đó đã rút "
        "cạn nguồn lực. spectrum là dải TĨNH của một biến (và spectrum+amber đã thuộc "
        "ambiguity-effect + availability-heuristic); ở đây việc sử dụng mới là nguyên nhân"),
    "declinism": (
        "rosy_tilt",
        "concept object MỚI. Bản dựng đầu dùng depletion+mint, nhưng contact sheet ở khổ 64px "
        "cho thấy nó chỉ khác decision-fatigue (depletion+amber) ở MÀU — hai card cạnh nhau "
        "trong library sẽ trông như lỗi render. Quan trọng hơn, depletion sai nghĩa: declinism "
        "không phải cái gì đó mất đi thật, mà là cùng một thực tại bị chấm điểm nhạt dần theo "
        "thời gian. Nên: kích thước 4 ô GIỮ NGUYÊN, chỉ sắc độ đổi"),
    "decoy-effect": (
        "foil",
        "concept object MỚI: phương án thứ ba tồn tại chỉ để làm phương án đích trông vượt "
        "trội. odd_one_out (amber còn trống) sai cơ chế — nó nói về độ nổi bật trên nền đồng "
        "nhất, còn decoy thì chưa bao giờ được chọn, nó chỉ đổi khung so sánh"),
    "default-effect": (
        "latch",
        "concept object MỚI: các phương án ngang giá, nhưng giữ nguyên thì miễn phí còn đổi "
        "thì phải vượt một bức tường công sức. Không hình nào trong registry cũ diễn được "
        "quán tính; gate là sàng lọc (có khe, có người bị chặn) — ở đây không ai bị chặn cả"),
    "defensive-attribution-hypothesis": (
        "in_out_ring",
        "người quan sát vẽ lại ranh giới thuộc về để đẩy nạn nhân ra ngoài 'nhóm giống tôi', "
        "nhờ đó rủi ro cũng rơi ra ngoài vòng của mình. LƯU Ý cho batch sau: in_out_ring+mint "
        "nên để dành cho in-group-bias; out-group-homogeneity-bias dùng granularity+amber "
        "(đã thuộc cross-race-effect, card anh em) hoặc cần một object mới"),
    "denomination-effect": (
        "granularity",
        "cùng MỘT tổng giá trị, khác nhau ở độ chia: một tờ lớn nguyên khối vs nhiều tờ nhỏ "
        "tách rời. Đây là card granularity đúng nghĩa đen nhất corpus. hierarchy của xlsx sai "
        "hẳn — không có quan hệ cha-con nào"),
    "diffusion-of-responsibility": (
        "dilution",
        "concept object MỚI: một nghĩa vụ chia cho N người, mỗi phần loãng tới mức dưới ngưỡng "
        "hành động. BẮT BUỘC khác bystander-effect (divergence+amber) vì hai card là anh em "
        "gần nghĩa — dùng lại divergence sẽ ra hai thumbnail trùng byte cạnh nhau trong library"),
    "disposition-effect": (
        "reference_kink",
        "concept object MỚI: cùng một biên độ lệch khỏi giá vốn, nhưng phía lãi thì buông sớm "
        "còn phía lỗ thì ôm chặt. threshold+mint (antifragility) đọc thành 'vượt mốc thì mạnh "
        "lên' — sai nghĩa. Object này sẽ dùng lại được cho loss-aversion, sunk-cost, endowment"),
    "distinction-bias": (
        "juxtaposition",
        "concept object MỚI: cùng một cặp, đặt sát nhau thì chênh lệch thành bậc thang nhìn "
        "thấy được, tách xa thì biến mất. contrast (xlsx) sai chiều — contrast nói 'hai thứ "
        "khác nhau', còn card này nói hai thứ THỰC RA gần như nhau, chỉ cách nhìn tạo ra khác biệt"),

    # ---- batch #7 (2026-09-07) — xlsx gán 7 hierarchy + 3 divergence cho 10 card,
    # tức cả batch sẽ chỉ ra ĐÚNG 2 hình. Chẩn đoán lại toàn bộ theo `back`.
    # Mọi cặp (metaphor, hue) dưới đây đã được đối chiếu với 60 SVG đã render để
    # không trùng byte — xem ghi chú về lỗi dupe-checker ở cuối file.
    "door-in-the-face-technique": (
        "foil",
        "yêu cầu lớn mở đầu tồn tại CHỈ để làm yêu cầu thật trông vừa phải — đúng định nghĩa "
        "foil. divergence (xlsx) đọc thành 'một điểm rẽ nhiều lựa chọn', mất hẳn ý 'phương án "
        "mồi bị bỏ đi ngay'"),
    "dual-process-theory": (
        "latch",
        "System 1 nằm sẵn phía trước, miễn phí; muốn tới System 2 phải vượt một bức tường công "
        "sức. Bất đối xứng CHI PHÍ mới là nội dung của card, không phải quan hệ cha-con "
        "(hierarchy) hay hai tầng chồng nhau (layers, vốn vẽ 4 đĩa nên đọc sai thành 4 tầng)"),
    "dunning-kruger-effect": (
        "overclaim",
        "concept object MỚI: khung lớn = năng lực tự nhận, phần đặc ở đáy = năng lực thật, "
        "khoảng rỗng ở giữa để TRỐNG vì đó đúng là thứ người trong cuộc không thấy. "
        "Bản dựng đầu dùng coverage_sphere nhưng nhìn contact sheet 512 thì nó đọc thành quả "
        "bóng biển (vật thể nhận dạng được — vi phạm Step 6) và không nói gì về card. "
        "granularity sát nghĩa nhưng cả hai hue đều đã bị chiếm (denomination-effect, cross-race-effect)"),
    "duration-neglect": (
        "odd_one_out",
        "chuỗi khoảnh khắc gần như đồng nhất và không được đếm; chỉ MỘT điểm (đỉnh cường độ) "
        "lệch hẳn ra và chiếm trọn ký ức. hierarchy (xlsx) không có quan hệ cha-con nào ở đây"),
    "effort-justification": (
        "effort_price",
        "concept object MỚI: cột chia đốt = công sức đếm được, khối đặc cạnh bên cao ĐÚNG bằng "
        "cột = giá trị cảm nhận đọc ra từ công sức. Không hình nào trong registry diễn được "
        "quan hệ 'input tạo ra định giá': spectrum là dải tĩnh, proportion là phần/tổng, "
        "depletion là mất mát thật"),
    "egocentric-bias": (
        "halo_spill",
        "lõi đậm = góc nhìn của chính mình, sắc độ lan sang mọi đánh giá lân cận (đóng góp, "
        "công sức, vai trò). proportion sát nghĩa hơn nhưng proportion+amber đã thuộc "
        "base-rate-fallacy"),
    "empathy-gap": (
        "juxtaposition",
        "cùng một lựa chọn, nhìn từ trạng thái 'nóng' (sát, chênh lệch hiện rõ) và từ trạng thái "
        "'lạnh' (xa, chênh lệch biến mất). Biến thay đổi là KHOẢNG CÁCH chứ không phải bản thân "
        "lựa chọn — đúng cơ chế của empathy gap"),
    "endowment-effect": (
        "reference_kink",
        "bất đối xứng quanh mốc sở hữu: cùng một món đồ, giá sẵn sàng BÁN và giá sẵn sàng MUA "
        "lệch hẳn nhau. Object này đã được ghi chú dành sẵn cho endowment ở entry disposition-effect"),
    "escalation-of-commitment": (
        "depletion",
        "nguồn lực hữu hạn bị rút cạn bởi chính việc dồn thêm để bảo vệ quyết định cũ. "
        "cycle sát nghĩa nhưng cycle+mint đã thuộc abilene-paradox"),
    "essentialism": (
        "hierarchy",
        "niềm tin vào các 'loại' cố định có bản chất bất biến — đây là card taxonomy đúng nghĩa "
        "nhất của batch, nên giữ nguyên gợi ý hierarchy của xlsx (hierarchy+amber còn trống)"),

    # --- batch 2026-09-08 -------------------------------------------------
    # Cả 10 gợi ý của xlsx đều sai (7 branching/hierarchy máy móc). Vốn hình cũ đã
    # dùng 63/78 tổ hợp (metaphor × hue) nên hầu hết hình đúng nghĩa đều kẹt hue —
    # batch này phải mở thêm 9 concept object mới trong illus.py.
    "extension-neglect": (
        "base_blind",
        "bỏ qua KÍCH THƯỚC tập hợp đứng sau một tỉ lệ. proportion vẽ cả phần lẫn tổng nên "
        "tỉ lệ đọc ra được ngay — đúng cái mà card nói là người ta KHÔNG làm; branching của "
        "xlsx thì không liên quan. base_blind giữ tử số y hệt và cho mẫu số đổi"),
    "extrinsic-incentive-error": (
        "locus_flip",
        "động lực người khác bị gán ra NGOÀI, của mình thì để BÊN TRONG. mirror sát nghĩa "
        "self↔other nhưng mirror+amber đã thuộc actor-observer-bias, và mirror nói về sắc độ "
        "quy kết chứ không nói vị trí trong/ngoài của cái đẩy — đó mới là nội dung card"),
    "fading-affect-bias": (
        "asymmetric_fade",
        "cảm xúc tiêu cực phai NHANH HƠN tích cực — luận điểm là chênh lệch tốc độ, nên phải "
        "có đủ hai dãy. rosy_tilt (một dãy phai đều) vẽ được kết quả nhưng không vẽ được "
        "nguyên nhân, và rosy_tilt+mint đã thuộc declinism"),
    "false-consensus-effect": (
        "overclaim",
        "phạm vi đồng thuận tự nhận lớn hơn phần thực có, và khoảng chênh để RỖNG vì chính "
        "người trong cuộc không thấy nó — đúng ngữ pháp overclaim. coverage_sphere cũng nói "
        "'phủ lên toàn bộ' nhưng thiếu vế 'ước lượng quá tay' và đã kẹt amber ở affect-heuristic"),
    "first-principles-thinking": (
        "from_primitives",
        "tháo vấn đề xuống thành phần cơ bản rồi DỰNG LẠI từ đó. granularity đúng vế 'phân "
        "giải' nhưng không có vế lắp lại, và granularity+mint đã thuộc denomination-effect; "
        "page_structure còn trống nhưng vẽ ra một trang wireframe — vật thể nhận dạng được"),
    "focalism": (
        "foreground_swell",
        "một sự kiện phình to trong dự đoán trong khi phần đời còn lại vẫn chạy tiếp. beam là "
        "hình đúng nhất về mặt nghĩa nhưng beam+amber đã thuộc change-blindness; hơn nữa beam "
        "làm phần còn lại TỐI ĐI, còn card này nói phần còn lại vẫn diễn ra bình thường"),
    "foot-in-the-door-technique": (
        "ratchet",
        "yêu cầu nhỏ đã nhận trở thành chỗ tựa cho yêu cầu lớn. spectrum chỉ là dải độ lớn "
        "rời nhau, không có quan hệ phụ thuộc giữa các bậc — mà phụ thuộc mới là kỹ thuật; "
        "spectrum+mint cũng đã thuộc cathedral-effect"),
    "framing-effect": (
        "two_frames",
        "cùng một mốc, kể theo phía 'được' hay phía 'mất'. contrast vẽ hai khối khác chất = "
        "đối lập có thật, ngược hẳn luận điểm 'bản chất hoàn toàn giống nhau'; mirror+amber "
        "đã bị chiếm. two_frames giữ mực nước ở đúng một độ cao trong cả hai khung"),
    "frequency-illusion": (
        "salience_pop",
        "tần suất thật KHÔNG tăng, chỉ độ để ý tăng. echo vẽ số lượng/độ lớn tăng dần tức là "
        "vẽ đúng cái ảo giác chứ không vẽ khái niệm; odd_one_out thì nói phần tử khác biệt. "
        "salience_pop giữ nguyên viền cho cả 9 chấm để đếm được rằng chúng vốn đã ở đó"),
    "functional-fixedness": (
        "one_affordance",
        "vật có nhiều công dụng khả thi nhưng chỉ một mối ghép từng được dùng. cue_lock nói "
        "THIẾU mảnh khớp (không mở được) — ở đây mảnh khớp không thiếu, cái chặn nằm trong "
        "thói quen; latch+amber cũng đã thuộc dual-process-theory"),
    "fundamental-attribution-error": (
        "locus_flip",
        "cùng MỘT hành vi, nguồn nhân quả bị đặt bên trong (tính cách người khác) hay bên "
        "ngoài (hoàn cảnh của mình) — đúng định nghĩa dispositional vs situational. xlsx cho "
        "divergence (một điểm rẽ nhiều nhánh) là mất hẳn phần 'cùng một hành vi'; mirror sát "
        "nghĩa nhưng mirror+mint đã thuộc cryptomnesia và mirror+amber thuộc actor-observer-bias"),
    "gamblers-fallacy": (
        "owed_reversal",
        "hình mới. Luận điểm là một chuỗi kết quả CÓ THẬT dồn về một phía, cộng với một ô "
        "RỖNG phía đối diện = cái 'phải đổi chiều để cân bằng' không tồn tại. xlsx cho "
        "hierarchy (cha-con) không liên quan gì; balance vẽ cán cân lệch có thật, tức là vẽ "
        "đúng cái ảo giác chứ không vẽ khái niệm; reference_kink có hai độ lệch đều CÓ THẬT"),
    "generation-effect": (
        "self_built",
        "hình mới. Cùng một nội dung qua hai lối: tự dựng lên từng phần thì giữ được dấu vết, "
        "nhận nguyên si thì nhạt. xlsx cho divergence là sai chiều; asymmetric_fade đúng ý "
        "'một dãy phai nhanh hơn' nhưng asymmetric_fade+mint đã thuộc fading-affect-bias, và "
        "generation-effect nói về NGUỒN GỐC của nội dung chứ không về tốc độ phai theo thời gian"),
    "goodharts-law": (
        "proxy_inflates",
        "hình mới. Phép đo và mục tiêu từng cao bằng nhau rồi tách hẳn ra đúng lúc phép đo bị "
        "lấy làm đích — nên bắt buộc phải vẽ được trạng thái 'trước'. xlsx cho page_structure "
        "(bố cục/IA) lạc đề hẳn; rebound nói kết quả bật ngược nhưng thiếu mất cặp đại lượng "
        "từng trùng nhau; fracture+amber đã thuộc continued-influence-effect"),
    "group-attribution-error": (
        "one_for_all",
        "hình mới. Tính chất của đúng một cá thể bị sơn lên toàn bộ vùng chứa nó. xlsx cho "
        "nested_scope (các tầng phạm vi lồng nhau) chỉ vẽ được cái bao chứa, không vẽ được "
        "việc suy rộng; in_out_ring là ranh giới THUỘC VỀ (không có gì lan ra); halo_spill thì "
        "lan có nhạt dần và đã bị halo-effect trong cùng batch này chiếm về mặt nghĩa"),
    "groupthink": (
        "consensus_merge",
        "hình mới. Các quan điểm chồng lên nhau thành một khối đồng sắc, phần tử không nhập "
        "vào bị bỏ rỗng ngoài rìa. xlsx cho funnel (nhiều vào ít ra) đọc thành 'quy trình lọc "
        "hợp lý' — ngược hẳn luận điểm rằng chất lượng quyết định GIẢM; funnel+amber cũng đã "
        "thuộc availability-heuristic"),
    "halo-effect": (
        "tint_carryover",
        "hình mới. Bốn ô đánh giá CÙNG một sắc độ, chỉ một ô có bằng chứng bên trong — chỗ "
        "'không nhạt đi' mới là nội dung: các phẩm chất kia được chấm điểm y hệt mà không có "
        "dữ liệu nào. halo_spill là hình chính danh của khái niệm này nhưng halo_spill+mint đã "
        "thuộc cheerleader-effect và +amber thuộc egocentric-bias; xlsx cho hierarchy vô nghĩa ở đây"),
    "hanlons-razor": (
        "parsimony",
        "hình mới. Cùng một hệ quả, hai lối giải thích khác hẳn nhau về SỐ MẮT XÍCH giả định — "
        "ác ý cần ba giả định (cố ý + có động cơ + nhắm vào mình), vô tâm cần một. xlsx cho "
        "divergence vẽ một điểm rẽ nhiều nhánh, ngược chiều; balance+amber đã bị chiếm hai lần "
        "và cán cân nói 'nặng/nhẹ' chứ không nói 'ít giả định hơn'"),
    "hard-easy-effect": (
        "regression_crossing",
        "hình mới. Điểm cắt là toàn bộ nội dung: độ lệch ĐỔI DẤU qua nó — việc khó thì tự đánh "
        "giá cao hơn thật, việc dễ thì thấp hơn thật. xlsx cho hierarchy vô nghĩa; overclaim "
        "chỉ lệch một chiều nên vẽ ra sẽ thành Dunning-Kruger; reference_kink có hai ô lệch RỜI "
        "nhau quanh một mốc, không có đường thứ hai cắt qua để tạo chỗ đổi dấu"),
    "hawthorne-effect": (
        "observed_lift",
        "hình mới. Dãy cột đều nhau, riêng phần nằm trong cung 'đang bị quan sát' thì cao hẳn "
        "lên dù không điều kiện nào đổi. xlsx cho divergence sai hẳn; beam nói chú ý của CHÍNH "
        "chủ thể dồn vào một điểm, còn ở đây cái nhìn đến từ bên ngoài và thứ đổi là hành vi "
        "của người bị nhìn; veil thì ngược (che đi, không phải soi vào)"),

    # ---- batch #6 (2026-09-12) — xlsx gán 6 branching + 3 hierarchy + 1 nesting,
    # tức 9/10 card dồn vào 2 hình. Chẩn đoán lại toàn bộ theo `back`.
    # 5 hình mới phải viết vì không hình nào trong 57 hình sẵn có diễn được quan hệ.
    # 2 card đổi hue (không đổi metaphor) vì metaphor đúng đã bị chiếm ở hue của xlsx —
    # đổi hue rẻ hơn đổi nghĩa, và hai lần đổi ngược chiều nhau nên cân bằng mint/amber
    # của corpus không đổi.
    "hedonic-treadmill": (
        "setpoint_return",
        "hình mới. Quan hệ là QUAY VỀ MỨC NỀN: một độ lệch lên và một độ lệch xuống, cả hai dựng "
        "dốc rồi thoải về đúng đường nền — thích nghi không phân biệt tin tốt với tin xấu. xlsx "
        "cho branching vô nghĩa (không có gì rẽ nhánh). cycle đã gần nhưng vòng khép kín nói "
        "'lặp lại', còn ở đây không có vòng nào, chỉ có cái đuôi tắt dần. threshold thì ngược hẳn: "
        "vượt ngưỡng rồi Ở LUÔN trạng thái mới, đúng cái mà hedonic treadmill phủ định"),
    "hindsight-bias": (
        "retrofit_path",
        "hình mới. Ba kết cục khả dĩ để RỖNG và cùng cỡ, chỉ kết cục đã xảy ra được tô đặc và nối "
        "vào một đường liền về điểm đầu. xlsx cho nesting sai hẳn. divergence vẽ mọi nhánh đều "
        "đặc — đúng trạng thái TRƯỚC khi biết, mà hindsight bias lại nằm ở chỗ ba nhánh kia bị "
        "xoá khỏi ký ức; cái rỗng mới là nội dung, nên phải để rỗng thật"),
    "horn-effect": (
        "halo_spill",
        "một ấn tượng nổi bật lan sang các đánh giá lân cận không liên quan — hình này trung tính "
        "về hoá trị nên dùng được cho cả halo lẫn horn (card tự gọi mình là 'mặt trái của halo "
        "effect'). halo-effect trong corpus đi với tint_carryover (nói về chuyện chấm điểm y hệt "
        "mà ruột rỗng), nên halo_spill còn trống và về nghĩa thì đúng hơn cho horn. xlsx cho "
        "hierarchy sai: không có quan hệ cha–con nào ở đây"),
    "hot-hand-fallacy": (
        "streak_projection",
        "hình mới. Bốn kết quả BẰNG NHAU (mỗi lần thử độc lập và giống hệt nhau) rồi một ô rỗng "
        "cùng phía nhưng cao hơn hẳn = kỳ vọng nối dài chuỗi, mà không gì trong chuỗi sinh ra nó. "
        "xlsx cho branching sai. Bản thử đầu dùng echo nhưng echo NHẠT VÀ THẤP DẦN — vẽ ra thành "
        "'chuỗi đang tắt', tức ngược hẳn nội dung card. Cặp đối của nó là owed_reversal "
        "(gamblers-fallacy, amber): ở đó ô rỗng nằm phía ĐỐI DIỆN đường mốc, ở đây cùng phía và "
        "cao hơn — đủ khác để không lẫn ở 64px"),
    "hyperbolic-discounting": (
        "steep_then_flat",
        "hình mới. Nội dung là ĐỘ CONG, không phải độ giảm: mức sụt ở đoạn gần lớn hơn tổng các "
        "mức sụt còn lại, rồi gần như nằm ngang ở đoạn xa — chính chỗ nằm ngang giải thích nghịch "
        "lý đảo chiều ưu tiên trong `front`. xlsx cho branching sai. spectrum giảm ĐỀU nên vẽ ra "
        "sẽ thành chiết khấu tuyến tính, tức phủ định đúng điểm của card; depletion có vạch 'mức "
        "đầy' bị rút dần — mất mát do sử dụng, không phải định giá theo khoảng cách thời gian"),
    "identifiable-victim-effect": (
        "foreground_swell",
        "một cá thể phình to trong khi dãy đều đặn vẫn chạy tiếp ở cả hai phía — cỡ nó chiếm "
        "trong phản ứng của ta không phải cỡ thật của vấn đề. xlsx cho branching sai. granularity "
        "(phân giải được thành cá thể ↔ nhoè thành khối) sát nghĩa nhất nhưng đã hết cả hai hue "
        "(cross-race-effect, denomination-effect). ĐỔI HUE amber→mint: foreground_swell+amber đã "
        "là focalism"),
    "ikea-effect": (
        "effort_price",
        "công sức bỏ ra được đọc thành giá trị của vật — đúng định nghĩa card, sát hơn bất cứ hình "
        "nào khác. xlsx cho hierarchy sai. ĐỔI HUE mint→amber: effort_price+mint đã là "
        "effort-justification (giữ nguyên, đã ship). Hai card này là họ hàng gần nên dùng chung "
        "hình là đúng; phân biệt bằng hue, không bịa một hình lệch nghĩa chỉ để khác nhau"),
    "illusion-of-asymmetric-insight": (
        "asymmetric_probe",
        "hình mới. Hai khối Y HỆT NHAU (thực tế đối xứng — không ai có lợi thế thông tin) nhưng "
        "mũi thăm dò một bên cắm sâu tới tâm, mũi bên kia đứng lại giữa khoảng trống. xlsx cho "
        "branching sai. mirror nói cùng MỘT sự việc qua hai khung quy kết, chỉ có một đối tượng; "
        "ở đây phải có HAI chủ thể cùng tự nhận về phía đối diện. overclaim lệch một chiều, một "
        "chủ thể — mất mất tính đối xứng vốn là toàn bộ cái ảo giác"),
    "illusion-of-control": (
        "unlinked_control",
        "hình mới. Một mấu nối chỉ ĐÚNG HƯỚNG vào vùng kết quả ngẫu nhiên, nhưng không có gì băng "
        "qua khoảng trống: cảm giác điều khiển là có thật, mối liên kết thì không. xlsx cho "
        "branching sai. fracture có nối nhưng lệch khớp (bất nhất), ở đây không có khớp nào; veil "
        "thì thông tin vẫn tồn tại sau tấm che, còn ở đây liên kết vốn không tồn tại — khác nhau "
        "về bản chất, không về mức độ"),
    "illusion-of-explanatory-depth": (
        "hollow_chain",
        "hình mới. Một khung liền vây quanh cả chuỗi = lời tự nhận 'hiểu từ đầu tới cuối'; bên "
        "trong chỉ mắt đầu và mắt cuối được tô, hai mắt giữa rỗng. xlsx cho hierarchy sai. "
        "overclaim đúng nghĩa nhất nhưng đã hết cả hai hue (dunning-kruger, false-consensus) và "
        "vẽ lại sẽ thành Dunning-Kruger; gap_fill là chỗ hổng ĐƯỢC VÁ bằng vật liệu lạ, còn ở đây "
        "không ai vá — lỗ vẫn nguyên, chỉ là chưa ai nhìn vào, và đó mới là điểm của card"),

    # ---- batch 2026-09-16 — xlsx gán 9 branching + 1 nesting, tức 9/10 card sẽ nhận
    # ĐÚNG một hình (divergence). Không card nào trong batch là "một điểm rẽ nhiều
    # nhánh". Chẩn đoán lại toàn bộ theo `back`; 9 concept object mới phải viết vì các
    # hình gần nghĩa nhất (locus_flip, veil, overclaim, echo, base_blind, one_for_all)
    # đều đã kín cả hai hue. Card thứ 10 (in-group-bias) dùng hình cũ + đổi hue.
    "illusion-of-external-agency": (
        "outward_credit",
        "hình mới. Cảm giác do CHÍNH MÌNH sinh ra (chấm đặc nằm trong khối bản thân) nhưng "
        "công được ghi cho một tác nhân bên ngoài 'thấu hiểu' — vẽ rỗng vì tác nhân đó không "
        "làm gì cả. xlsx cho branching sai hẳn: không có điểm rẽ nào. locus_flip là hình sát "
        "nghĩa nhất nhưng đã kín cả hai hue (fundamental-attribution-error, "
        "extrinsic-incentive-error) và nó nói 'nguồn được đặt trong HAY ngoài' — ở đây nguồn "
        "đã xác định là bên trong, cái được thêm vào mới là chỗ rỗng. unlinked_control+mint "
        "(illusion-of-control) thì không có mối nối nào cả"),
    "illusion-of-transparency": (
        "signal_leak",
        "hình mới. Ba đại lượng bắt buộc: cường độ nội tâm (đặc), lượng thực sự lọt qua ranh "
        "giới (chấm nhỏ), và lượng ta TIN là lọt ra (khung lớn). xlsx cho branching sai. "
        "overclaim đúng ngữ pháp 'tự nhận > thực có' nhưng đã kín hai hue (dunning-kruger, "
        "false-consensus) và thiếu mất cái ranh giới — mà ranh giới trong–ngoài mới là chỗ "
        "khác biệt của card này. veil kín cả hai hue và sai chiều: ở đây không ai che gì"),
    "illusion-of-validity": (
        "fitted_overreach",
        "hình mới. Cơ chế của card là ĐỘ MẠCH LẠC sinh ra tự tin: các điểm thẳng hàng hoàn "
        "hảo, và đường khớp chạy tiếp ra ngoài vùng có dữ liệu. xlsx cho branching sai. "
        "overclaim/hollow_chain nói về phạm vi tự nhận nhưng không vẽ được chỗ 'quá gọn nên "
        "dễ kể thành câu chuyện' — mà đó là nguyên nhân card nêu ra, không phải hệ quả"),
    "illusory-correlation": (
        "one_cell_counted",
        "hình mới. Bảng 2x2 đủ bốn ô, chỉ ô đồng xuất hiện được tô — khớp thẳng với "
        "`strategy` của card ('đếm cả những lần X xảy ra mà KHÔNG có Y'). xlsx cho branching "
        "sai. network+mint còn trống nhưng network là apophenia (áp một mạng lên các điểm rời "
        "rạc) — ở đây chỉ có ĐÚNG hai biến và vấn đề là ba ô không được đếm, không phải một "
        "mạng liên kết. echo (lặp lại → khuếch đại) kín cả hai hue và sai cơ chế"),
    "illusory-superiority": (
        "all_above_median",
        "hình mới. Luận điểm nằm ở tính BẤT KHẢ THỐNG KÊ: mọi chấm đều trên đường trung bình "
        "và nửa dưới bỏ trống. xlsx cho branching sai. overclaim (dunning-kruger, mint) là "
        "họ hàng gần nhất nhưng nó vẽ MỘT chủ thể tự nhận quá tay; ở đây phải thấy được cả "
        "một quần thể cùng làm thế thì nghịch lý mới hiện ra"),
    "illusory-truth-effect": (
        "stacked_copies",
        "hình mới. Ba bản sao y hệt, mỗi bản nhạt như nhau (không bản nào mang thêm bằng "
        "chứng), chỗ chồng lên nhau thì đậm. xlsx cho branching sai. echo là hình chính danh "
        "nhưng kín cả hai hue (clustering-illusion, availability-cascade) và echo NHẠT/THẤP "
        "DẦN — vẽ ra thành 'đang tắt', ngược với việc lặp lại làm niềm tin đậm thêm. "
        "availability-cascade là card anh em nên càng phải tránh dùng lại đúng hình đó"),
    "immune-neglect": (
        "unseen_cushion",
        "hình mới. Card nói rõ cái bị bỏ sót là CƠ CHẾ ĐỐI PHÓ, nên nó phải có mặt trong hình "
        "mà vẫn đọc ra là 'không được tính' — dải đệm vẽ rỗng, nằm giữa cú rơi và mức dự đoán. "
        "xlsx cho branching sai. setpoint_return+amber còn trống và đúng nghĩa về mặt quỹ đạo, "
        "nhưng nó thuộc hedonic-treadmill (mint) — dùng lại sẽ ra hai thumbnail chỉ khác MÀU "
        "cho hai card link nhau, đúng lỗi declinism/decision-fatigue mà batch 2026-09-08 phải "
        "sửa. Hơn nữa setpoint_return VẼ RA sự hồi phục, còn card này nói nó bị bỏ quên"),
    "impact-bias": (
        "over_scaled_forecast",
        "hình mới. Card nói rõ phóng đại CẢ 'length' LẪN 'intensity', nên khung dự báo phải "
        "lớn hơn trên hai trục và chung gốc với khối trải nghiệm thật. xlsx cho branching sai. "
        "overclaim chỉ lệch một trục (phần đặc trải hết bề ngang) nên mất đúng vế 'kéo dài bao "
        "lâu', và nó đã kín cả hai hue. Phân biệt với immune-neglect cùng batch: ở đó nội dung "
        "là lực đỡ bị bỏ quên, ở đây là quy mô bị gán sai"),
    "implicit-stereotypes": (
        "group_tint_applied",
        "hình mới, là chiều NGƯỢC của one_for_all (mint, group-attribution-error): ở đó một cá "
        "thể được quan sát rồi sơn lên cả nhóm; ở đây sắc độ của nhóm chảy nguyên vẹn vào một "
        "cá thể mà ruột cá thể đó rỗng. xlsx cho branching sai. one_for_all+amber còn trống "
        "nhưng vẽ đúng chiều ngược lại thì thành card khác. halo_spill (nhạt dần khi lan) kín "
        "cả hai hue và sai: ở đây sắc độ sang cá thể không nhạt đi chút nào"),
    "in-group-bias": (
        "in_out_ring",
        "hình cũ, đúng nghĩa: ranh giới THUỘC VỀ và trọng số khác nhau ở hai phía. Đây là card "
        "mà chú thích ở entry defensive-attribution-hypothesis (batch 2026-09-06) đã ghi rõ là "
        "để dành in_out_ring+mint cho nó. xlsx gán nesting (nested_scope) — nested_scope nói "
        "quan hệ BAO HÀM (tập con nằm trong tập mẹ), còn in-group bias là hai nhóm TÁCH nhau "
        "với một vành phân định, và nested_scope cũng đã kín cả hai hue"),
}

# Đổi hue khi metaphor đúng đã bị một card khác chiếm ở hue mà xlsx gán (cùng metaphor +
# cùng hue = ảnh trùng byte). Đổi hue rẻ hơn đổi metaphor: hue không mang nghĩa, chỉ ảnh
# hưởng cân bằng mint/amber của corpus. slug -> (hue, "lý do")
HUE_OVERRIDES = {
    "identifiable-victim-effect": (
        "mint", "foreground_swell+amber đã là focalism"),
    "ikea-effect": (
        "amber", "effort_price+mint đã là effort-justification"),
    "in-group-bias": (
        "mint", "in_out_ring+amber đã là defensive-attribution-hypothesis; mint vốn được "
                "ghi chú để dành sẵn cho card này từ batch 2026-09-06"),
}


OVERRIDES.update({
    # ---- batch #9 (2026-09-17) — xlsx gán 9/10 card là `hierarchy`, tức gần như toàn
    # batch sẽ nhận đúng một hình. Chẩn đoán lại từ `back` của từng card. Chín hình
    # dưới đây là hình MỚI viết cho batch này: các hình sát nghĩa sẵn có đều đã bị
    # card khác chiếm ở CẢ hai hue, mà dùng hình gần-đúng chính là thứ runbook cảnh báo.
    "inattentional-blindness": (
        "unattended_object",
        "hình mới. `beam` mới là nghĩa gốc (chú ý dồn một điểm) nhưng beam+mint đã là "
        "attentional-bias và beam+amber đã là change-blindness. Vả lại beam vẽ nón chiếu "
        "từ một nguồn, còn điểm của card này là vật KHÔNG bị che, không nằm ngoài rìa, "
        "chỉ đơn giản không nhận được nét mực nào — nên vẽ vòng lớn rỗng cạnh cụm nhỏ "
        "đặc. `veil` sai hẳn: ở đó có tấm che thật"),
    "information-bias": (
        "inert_input",
        "hình mới. xlsx đoán hierarchy — card không có quan hệ cha–con nào. Quan hệ thật "
        "là đầu vào tăng mà đầu ra đứng yên, nên hai ô kết quả phải vẽ y hệt nhau ở cùng "
        "độ cao. `funnel` (nhiều vào ít ra) nói về sàng lọc, `depletion` nói về hao mòn — "
        "cả hai đều làm cái gì đó THAY ĐỔI, tức phủ định đúng điểm của card"),
    "insensitivity-to-sample-size": (
        "spread_by_n",
        "hình mới. `base_blind` (mẫu số bị nhìn xuyên qua) là họ hàng gần nhất nhưng "
        "base_blind+mint đã là extension-neglect, và nó nói về tỉ lệ chứ không về phương "
        "sai. Quan hệ đúng ở đây là ĐỘ VĂNG quanh giá trị thật thay đổi theo cỡ mẫu — "
        "hàng ít phần tử văng rộng, hàng nhiều phần tử bám sát. Chỉ khác số lượng thôi "
        "thì thành `granularity`"),
    "inversion": (
        "negative_space",
        "hình mới. `rebound` (bật ngược, kết quả đi ngược ý định) nghe hợp chữ 'đảo "
        "ngược' nhưng sai nghĩa: inversion là một THỦ PHÁP chủ động, không phải một cú "
        "phản tác dụng. Vẽ đúng cái card mô tả: chỉ các vùng phải tránh được tô, lời "
        "giải là khoảng rỗng còn lại và cố ý không vẽ ra"),
    "just-world-hypothesis": (
        "deserved_backfill",
        "hình mới. Điểm đau của card nằm ở chiều SUY NGƯỢC — 'bị phạt thì hẳn là đáng "
        "đời'. Nên cột kết cục (quan sát được) vẽ đặc, cột phẩm chất (suy ra) vẽ rỗng mà "
        "khít từng cặp. `cycle` bắt được vế tự củng cố nhưng cả hai hue đều đã dùng và nó "
        "không cho thấy cái nào có thật cái nào được lấp vào. `mirror` sai: hai cột đây là "
        "hai thứ khác nhau, không phải một sự việc soi hai lần"),
    "lake-wobegone-effect": (
        "all_above_median",
        "giữ hình có sẵn: 'on average we all think we're above average' đúng là phân bố "
        "bất khả mà t_all_above_median vẽ ra. Hình này đang dùng cho illusory-superiority "
        "(mint) — hai card vốn là cùng một hiện tượng nên dùng chung hình là TRUNG THỰC, "
        "không phải lười; hue amber của xlsx đã đủ tách byte"),
    "law-of-narrative-gravity": (
        "narrative_tilt",
        "hình mới. Chữ 'gravity' trỏ thẳng tới `pull`, nhưng pull+mint là anchoring và "
        "pull+amber là bandwagon-effect. Quan trọng hơn: pull bóp hẹp KHOẢNG CÁCH (ước "
        "lượng bị kéo dịch chỗ), còn card này nói sự kiện trung tính bị kéo về mặt DIỄN "
        "GIẢI — nên giữ nguyên cỡ và khoảng cách, chỉ cho góc nghiêng tăng dần khi lại gần"),
    "law-of-the-instrument": (
        "forced_fit",
        "hình mới. `one_affordance` là card anh em (functional-fixedness) nhưng ở đó vật "
        "KHÔNG biến dạng — chỉ là các công dụng khác không được nhìn ra. Ở đây chiều ngược "
        "lại: chính bài toán bị bẻ cho vừa công cụ, nên phải thấy hình tròn bị cắt phẳng "
        "bốn cạnh theo khung vuông. `gate` sai vì không có gì bị chặn, chỉ có hình bị đổi"),
    "law-of-triviality": (
        "inverse_weight",
        "hình mới. Quan hệ là TỈ LỆ NGHỊCH giữa hai đại lượng đo được (tầm quan trọng ↔ "
        "thời gian bàn), cần thấy hai cặp bắt chéo nhau quanh một đường mốc. `proportion` "
        "(phần/tổng) và `foreground_swell` (một phần tử phình to) đều chỉ có MỘT đại "
        "lượng, và cả hai hue của cả hai hình đều đã dùng"),
    "learned-helplessness": (
        "unused_exit",
        "hình mới. xlsx gán iteration→cycle, mà cycle+mint (abilene-paradox) và "
        "cycle+amber (confirmation-bias) đều đã dùng. Cycle cũng chỉ kể được vế lặp lại, "
        "bỏ mất vế quyết định: lối thoát CÓ THẬT và đang mở mà vẫn không được dùng — nên "
        "tường phải có khoảng hở vẽ rõ và khối đặc nép ở tường đối diện. `unlinked_control` "
        "là ảnh phản chiếu sai chiều: ở đó tin vào một liên kết không tồn tại, ở đây là "
        "không tin vào một liên kết có tồn tại"),
})


def read_index():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Article Index"]
    rows = ws.iter_rows(values_only=True)
    header = [str(h).strip() if h else "" for h in next(rows)]
    ix = {name: header.index(name) for name in
          ("#", "File", "Title", "Hero shape", "Hue")}
    out = []
    for r in rows:
        if not r or r[ix["File"]] is None:
            continue
        out.append(dict(
            n=r[ix["#"]],
            slug=str(r[ix["File"]]).removesuffix(".md"),
            title=r[ix["Title"]],
            shape=str(r[ix["Hero shape"]]).strip().lower(),
            hue=str(r[ix["Hue"]]).strip().lower(),
        ))
    out.sort(key=lambda d: d["n"])
    return out


def set_frontmatter_image(slug):
    """Set `image:` trong frontmatter. Không đụng field nào khác. True nếu có thay đổi."""
    path = os.path.join(CONTENT, f"{slug}.md")
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?\n)---\n", text, re.S)
    if not m:
        return None
    fm, rest = m.group(1), text[m.end():]
    line = f"image: /assets/stuff/{slug}.png"
    lines = fm.rstrip("\n").split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("image:"):
            if ln.strip() == line:
                return False
            lines[i] = line
            break
    else:
        pub = next((i for i, ln in enumerate(lines) if ln.startswith("published:")), None)
        lines.insert(pub if pub is not None else len(lines), line)
    open(path, "w", encoding="utf-8").write("---\n" + "\n".join(lines) + "\n---\n" + rest)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default=None,
                    help="danh sách slug ngăn cách bằng dấu phẩy — render lại đúng các card này "
                         "(bỏ qua luật idempotent), dùng khi sửa metaphor")
    ap.add_argument("--png-size", type=int, default=512,
                    help="cạnh PNG xuất ra (mặc định 512). Ảnh này vừa là thumbnail 64px vừa là "
                         "ảnh minh hoạ chính của card, nên cần đủ lớn để không vỡ ở khổ lớn; "
                         "SVG đi kèm mới là nguồn scale vô hạn.")
    args = ap.parse_args()

    os.makedirs(ASSETS, exist_ok=True)
    index = read_index()
    if args.only:
        want = [s.strip() for s in args.only.split(",") if s.strip()]
        pending = [c for c in index if c["slug"] in want]
        args.limit = len(pending)
    else:
        pending = [c for c in index if not os.path.exists(os.path.join(ASSETS, f"{c['slug']}.png"))]

    if not pending:
        print("COVERAGE 100% — không còn card nào thiếu ảnh.")
        return 0

    batch = pending[:args.limit]
    print(f"total={len(index)} missing={len(pending)} batch={len(batch)}\n")
    print(f"{'slug':<40} {'idea shape':<14} {'metaphor':<16} hue")

    for c in batch:
        metaphor, reason = OVERRIDES.get(c["slug"], (None, None))
        if metaphor is None:
            metaphor = SHAPE_MAP.get(c["shape"])
        if metaphor is None:
            print(f"  !! shape lạ: {c['slug']} -> {c['shape']}", file=sys.stderr)
            return 1
        hue = c["hue"] if c["hue"] in ("mint", "amber") else "mint"
        hue_ovr, hue_reason = HUE_OVERRIDES.get(c["slug"], (None, None))
        if hue_ovr:
            hue = hue_ovr
        print(f"{c['slug']:<40} {c['shape']:<14} {metaphor:<16} {hue}"
              + (f"   [hue: {c['hue']}->{hue_ovr}, {hue_reason}]" if hue_ovr else "")
              + (f"   [override: {reason}]" if reason else ""))
        if args.dry_run:
            continue

        svg = thumb(metaphor, hue)
        open(os.path.join(ASSETS, f"{c['slug']}.svg"), "w", encoding="utf-8").write(svg)
        # render 2x kích thước đích rồi hạ xuống bằng Lanczos để có antialias sạch
        size = args.png_size
        buf = io.BytesIO()
        cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                         output_width=size * 2, output_height=size * 2)
        # temp ra ngoài repo: thư mục mount có thể không cho unlink
        big = os.path.join(tempfile.gettempdir(), f"{c['slug']}.tmp.png")
        open(big, "wb").write(buf.getvalue())
        subprocess.run(["convert", big, "-filter", "Lanczos", "-resize", f"{size}x{size}",
                        "-strip", os.path.join(ASSETS, f"{c['slug']}.png")], check=True)
        os.remove(big)
        set_frontmatter_image(c["slug"])

    print(f"\nremaining after batch = {len(pending) - (0 if args.dry_run else len(batch))}")

    if not args.dry_run:
        # Hash trên SVG chứ KHÔNG phải PNG: `convert` không cho ra byte tất định giữa
        # các lần chạy, nên bản md5-trên-PNG trước đây bỏ sót 6/8 cặp trùng thật
        # (vd belief-bias == cognitive-dissonance). SVG là nguồn nên so ở đó mới đúng.
        # Chuẩn hoá id của clipPath trước khi hash: các hàm dùng clipPath (granularity,
        # coverage_sphere, mirror, veil...) sinh id từ một biến đếm toàn cục, nên hai card
        # CÙNG metaphor + CÙNG hue vẫn ra hai chuỗi khác nhau. Bản trước hash thô nên bỏ lọt
        # toàn bộ nhóm này — batch 2026-09-07 suýt ship 3 cặp trùng (granularity+mint đụng
        # denomination-effect, coverage_sphere+amber đụng affect-heuristic, mirror+mint đụng
        # cryptomnesia) mà checker vẫn báo sạch.
        dupes = {}
        for c in index:
            f = os.path.join(ASSETS, f"{c['slug']}.svg")
            if os.path.exists(f):
                body = re.sub(r'([a-z]{3,4})\d+', 'ID', open(f, encoding="utf-8").read())
                dupes.setdefault(hashlib.md5(body.encode()).hexdigest(),
                                 []).append(c["slug"])
        clashes = [v for v in dupes.values() if len(v) > 1]
        if clashes:
            print("\n!! TRÙNG BYTE — các card dưới đây render ra ĐÚNG một ảnh:", file=sys.stderr)
            for v in clashes:
                print("   " + " == ".join(v), file=sys.stderr)
            print("   (đổi metaphor hoặc hue cho một trong hai, xem mục C của "
                  "docs/scheduled-task-illustrations.md)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
