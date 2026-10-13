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
    "tip-of-the-tongue-phenomenon": (
        "hollow_chain",
        "Brown & McNeill (1966): người trong trạng thái TOT đoán đúng chữ cái đầu và số "
        "âm tiết trên mức ngẫu nhiên — tức hai đầu chuỗi được truy xuất, khúc giữa rỗng, "
        "mà cái khung bao quanh lại khiến nó đọc thành 'sắp bật ra'. hierarchy không có "
        "quan hệ nào ở đây; khác `veil` (thông tin bị che) và `cue_lock` (thiếu mảnh "
        "khớp) ở chỗ TOT là truy cập MỘT PHẦN, và chính phần có được mới sinh ra cảm giác"),
    "trait-ascription-bias": (
        "near_side_detail",
        "quan hệ cốt lõi là bất đối xứng về ĐỘ PHÂN GIẢI hai bên một ranh giới mình/người "
        "khác: phía mình phân giải được thành từng tình huống riêng khác cỡ nhau, phía "
        "người khác là một khối liền không có nét chia nào — đúng cái bất cân xứng thông "
        "tin mà Nisbett & Ross mô tả. hierarchy nói cha-con, không nói gì về chênh lệch "
        "độ phân giải; `mirror` (actor-observer-bias) nói cùng một sự việc hai cách quy "
        "kết, còn ở đây cái lệch là lượng chi tiết nhìn thấy được ở mỗi phía. "
        "`granularity` cũng đúng nghĩa nhưng amber đã bị cross-race-effect chiếm nên "
        "trùng byte; near_side_detail hơn ở chỗ vẽ hẳn cái ranh giới ra"),
    "ultimate-attribution-error": (
        "liking_flip",
        "card là một bảng 2x2: trong-nhóm/ngoài-nhóm × thành công/thất bại, và trọng số "
        "quy kết ĐẢO NGƯỢC giữa hai phía. liking_flip đúng cấu trúc đó (hai vòng "
        "trong/ngoài ở trên, hai ô mỗi bên đảo cỡ nhau ở dưới). nested_scope trong xlsx "
        "chỉ vẽ được 'vòng ngoài chứa lõi' — mất sạch phần đảo chiều, vốn là toàn bộ "
        "nội dung; `in_out_ring` cũng chỉ nói ranh giới thuộc về, không nói sự bất đối xứng"),
    "unit-bias": (
        "fill_to_frame",
        "Geier/Rozin/Wansink (2006): khẩu phần lớn hơn thì ăn nhiều hơn dù nhu cầu thật "
        "không đổi — khối tiêu thụ giãn chạm mép của bất kỳ khung đơn vị nào được đưa, "
        "còn lõi đặc (nhu cầu thật) hai bên bằng nhau chằn chặn. hierarchy không diễn "
        "được quan hệ này. Dùng chung hình với parkinsons-law là có chủ ý: cùng một quan "
        "hệ 'khung quyết định lượng, không phải nhu cầu', và parkinsons-law hiện đang để "
        "mint nên không trùng byte"),
    "von-restorff-effect": (
        "isolate_recalled",
        "HÌNH MỚI. Card cần hai vế: nền đồng nhất + một phần tử khác loại (vế này "
        "`odd_one_out` có, nhưng mint đã bị bizarreness-effect chiếm nên trùng byte), VÀ "
        "phần tử đó được NHỚ hơn — vế sau mới là phát hiện của von Restorff và không hình "
        "nào trong 177 hình có. isolate_recalled thêm hàng thanh nhớ lại chỉ cao ở đúng "
        "ô lệch. divergence trong xlsx (một điểm rẽ nhiều nhánh) không liên quan gì"),
    "weber-fechner-law": (
        "base_blind",
        "quan hệ cốt lõi: CÙNG một mức thay đổi tuyệt đối đọc trên hai cái nền khác hẳn "
        "nhau — giảm 10k trên 100k là 10%, trên 2 triệu là 0,5%. Cái nền quyết định thay "
        "đổi có được nhận ra hay không lại là thứ bị nhìn xuyên qua. hierarchy không có "
        "quan hệ nào; `equal_step_unequal_gain` sát nghĩa nhưng amber đã bị "
        "time-saving-bias chiếm nên trùng byte"),
    "well-traveled-road-effect": (
        "discounted_across_line",
        "tiền đề của card là hai quãng đường DÀI BẰNG NHAU, chỉ khác quen/lạ, và ước "
        "lượng thời gian lệch hẳn. discounted_across_line đúng cấu trúc đó: vách dọc chia "
        "quen/lạ, hai khối bằng nhau tuyệt đối, thanh ước lượng dưới mỗi khối lệch hẳn. "
        "Quy ước đọc (đừng đảo ở batch sau): khối ĐẶC = tuyến LẠ — đúng chữ của card, "
        "tuyến lạ đòi chú ý liên tục nên mỗi phút cảm giác 'dày' hơn — nên nó mang thanh "
        "ước lượng CAO; khối RỖNG = tuyến quen, đi tự động nên rỗng chú ý và thanh thấp. "
        "divergence trong xlsx vẽ 'một điểm rẽ nhiều nhánh' — đọc thành chọn tuyến, mà "
        "card không nói về chọn tuyến, nó nói về sai số ước lượng trên hai tuyến bằng nhau"),
    "zeigarnik-effect": (
        "open_loop_retained",
        "HÌNH MỚI. Biến duy nhất của card là trạng thái KHÉP/HỞ: việc xong thì nhả khỏi "
        "trí nhớ, việc bị ngắt giữa chừng thì giữ nguyên sức căng (lý thuyết trường của "
        "Lewin). Không hình nào trong 177 hình lấy chỗ-vòng-không-khép làm nội dung — "
        "`cycle` thì ngược hẳn (vòng khép tự củng cố), `odd_one_out` nói lệch-khỏi-nền "
        "chứ không nói dở-dang. hierarchy trong xlsx không liên quan"),
    "zero-risk-bias": (
        "certain_inside_branch",
        "card là một đánh đổi sai: dốc sức vét MỘT buồng nhỏ xuống đúng số 0 trong khi "
        "buồng lớn vẫn đầy nguyên. certain_inside_branch đúng hình đó — khung chia hai "
        "buồng lệch cỡ, buồng nhỏ trống hẳn, buồng lớn tô đầy sát mép. hierarchy không "
        "diễn được; `balance` sát nghĩa đánh đổi nhưng cả mint lẫn amber đều đã bị chiếm, "
        "và balance cũng không nói được chỗ 'trống HẲN' — tức sức hút riêng của con số 0"),
    "zero-sum-bias": (
        "fixed_total_split",
        "HÌNH MỚI. Card có hai vế: (a) tổng bị coi là CỐ ĐỊNH nên được của người này là "
        "mất của người kia, (b) thực tế tổng có thể nở ra nhưng khả năng đó không có mặt "
        "trong cách nghĩ. `balance` chỉ có vế (a) và đã bị chiếm ở cả hai hue; "
        "`share_of_field` nói tỉ phần tĩnh, không có sự bù trừ. fixed_total_split giữ cả "
        "hai: khung rộng y hệt ở hai hàng với vách dịch, cộng khối rỗng ngoài mép phải. "
        "divergence trong xlsx không liên quan"),
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
        # sửa ở batch #4: bản pull trùng BYTE với anchoring (cùng hue mint), mà anchoring mới là
        # card "khối nặng kéo lệch ước lượng" đúng nghĩa.
        "gate",
        "concept object: chỉ thông tin mang nhãn thẩm quyền được lọt qua cổng, bằng chứng trái "
        "chiều bị chặn lại — cơ chế là sàng lọc theo nguồn, không phải lực kéo. mint phân biệt "
        "với automation-bias (gate/amber), bản 'thẩm quyền = cái máy' của cùng quan hệ này"),
    "automation-bias": (
        "gate",
        "concept object: chỉ thông tin đến từ hệ thống tự động mới lọt qua cổng; "
        "thông tin trái ngược dù đúng vẫn bị chặn"),
    "availability-cascade": (
        "echo",
        "concept object: chính sự lan truyền lặp lại tạo ra cảm giác đáng tin, không phải bằng chứng. "
        "echo sát hơn cycle vì cascade là khuếch đại một chiều, không phải vòng khép kín"),
    "availability-heuristic": (
        # sửa ở batch #4: bản spectrum trùng BYTE với ambiguity-effect (cùng hue amber), mà
        # ambiguity-effect mới là dải liên tục đúng nghĩa (biết rõ xác suất → mù mờ).
        "echo",
        "concept object: cái được nhắc lại nhiều thì bật ra trong đầu dễ hơn, và chính độ dễ bật "
        "ra đó bị đọc thành 'phổ biến / nguy hiểm hơn thực tế' — khuếch đại từ lặp lại. amber "
        "phân biệt với availability-cascade (echo/mint), vốn là bản lan truyền trong xã hội"),

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

    # ---- batch #4 (2026-10-02) — xlsx gán 8 hierarchy + 1 branching + 1 nesting.
    # Chỉ 1/10 (choice-overload) đúng. Lưu ý thêm: phải tránh cả cặp (metaphor, hue) đã dùng —
    # mirror/amber đã thuộc actor-observer-bias, coverage_sphere/amber thuộc affect-heuristic,
    # veil/amber thuộc armchair-fallacy, nên 3 hình sát nghĩa nhất của batch này bị loại.
    "cathedral-effect": (
        "coverage_sphere",
        "một yếu tố môi trường (chiều cao trần) phủ lên toàn bộ cách xử lý thông tin, kể cả "
        "những vấn đề chẳng liên quan gì tới không gian — đúng nghĩa 'một thứ phủ lên tất cả'. "
        "hierarchy của xlsx sai hẳn: không có quan hệ cha-con nào. mint để phân biệt với "
        "affect-heuristic (coverage_sphere/amber)"),
    "change-blindness": (
        "beam",
        "concept object: chỉ phần nằm trong vùng được rọi mới được xử lý sâu, phần còn lại được "
        "lấp bằng phỏng đoán — con khỉ đột nằm ngoài chùm sáng. Card tự nói rõ cơ chế này. amber "
        "để không đụng attentional-bias (beam/mint), card anh em mà chính bài có đem ra so sánh"),
    "cheerleader-effect": (
        "halo_spill",
        "bối cảnh nhóm lan sang đánh giá về một gương mặt cụ thể — chính gương mặt đó không đổi, "
        "chỉ có vùng ảnh hưởng xung quanh làm nó được chấm cao hơn. nesting của xlsx chỉ nói "
        "'nhóm chứa cá nhân', mất mất phần quan trọng nhất là đánh giá bị dịch chuyển"),
    "chestertons-fence": (
        "nested_scope",
        "hàng rào là vòng ngoài nhìn thấy được, lý do dựng nó là cái lõi bị che phía trong — "
        "nguyên tắc buộc phải chạm tới lõi trước khi động vào vòng ngoài. veil sát nghĩa hơn "
        "nhưng veil/amber đã là armchair-fallacy"),
    "choice-overload": (
        "divergence",
        "giữ nguyên xlsx — ca hiếm mà cột Hero shape đúng: một điểm quyết định rẽ thành quá "
        "nhiều nhánh tương đương, và chính sự bùng nổ nhánh đó làm throughput sụp (24 loại mứt "
        "→ 3% mua). mint để không đụng bystander-effect (divergence/amber)"),
    "choice-supportive-bias": (
        "fracture",
        "concept object: ký ức về quyết định và những gì thực sự biết lúc quyết định lẽ ra phải "
        "khớp, nhưng lệch nhau — card nói rõ bộ nhớ còn chỉnh sửa lại chi tiết sự kiện. branching "
        "của xlsx chỉ vẽ được lúc đang phân vân, không vẽ được phần hậu-quyết-định"),
    "circle-of-competence": (
        "in_out_ring",
        "cả mental model là một đường viền và việc mình đang đứng trong hay ngoài nó — in_out_ring "
        "là hình duy nhất lấy ranh giới thuộc-về làm trung tâm. hierarchy của xlsx gợi thang bậc "
        "kiến thức, mà card nói rõ vòng to hay nhỏ không quan trọng"),
    "clustering-illusion": (
        "odd_one_out",
        "nền rải rác đồng đều tự nhiên sinh ra một cụm dày, và cụm đó bị đọc thành tín hiệu — nền "
        "đồng nhất là MỘT PHẦN của cơ chế (bom V-1 rơi theo phân phối Poisson). Không dùng network "
        "vì network/amber đã là apophenia, card gần nghĩa nhất, hai ô sẽ đọc như một"),
    "cognitive-dissonance": (
        "contrast",
        "hai nhận thức không thể cùng đứng trong một khung — căng thẳng sinh ra từ chính sự đối "
        "lập hình học đó. fracture sát nghĩa ngang nhưng fracture/mint đã là belief-bias; "
        "contrast/mint còn trống (attribute-substitution dùng amber)"),
    "cognitive-load-theory": (
        "layers",
        "bộ nhớ làm việc là vật chứa có chiều cao hữu hạn, trong đó ba loại tải (intrinsic / "
        "extraneous / germane) xếp thành tầng và tranh nhau chỗ — đúng quan hệ tầng/trầm tích. "
        "hierarchy của xlsx không diễn được phần 'giới hạn sức chứa'"),
    # ---- batch 2026-10-03 (selective-perception → social-comparison-bias) ----
    # xlsx gán CẢ 10 card là branching -> divergence. 10 card một hình, hue xen kẽ
    # mint/amber => 5 cặp trùng byte. Chẩn đoán lại toàn bộ theo `back` của từng card.
    "selective-perception": (
        "same_record_two_reads",
        "object mới. Không phải một điểm rẽ nhánh: cùng MỘT bản ghi khách quan, mỗi người giữ lại "
        "phần khớp kỳ vọng và quên nhanh phần gây khó chịu (Hastorf-Cantril 1954 - cùng một đoạn "
        "phim, mỗi trường thấy đối phương phạm lỗi nhiều hơn). Không dùng asymmetric_fade: "
        "fading-affect-bias đã sở hữu đúng nghĩa 'tốc độ phai lệch nhau', còn card này nằm ở tầng "
        "tri giác/tiếp nhận chứ không phải tầng phai của ký ức"),
    "self-consistency-bias": (
        "overwrite_seam",
        "ký ức niềm tin cũ bị tái dựng theo niềm tin hiện tại mà KHÔNG để lại mối ghép "
        "nào để lần ra — đúng nghĩa 'viết đè không đường may'. divergence sai hẳn: ở đây "
        "không có lựa chọn nào rẽ ra, chỉ có một khối bị thay ruột"),
    "self-fulfilling-prophecy": (
        "self_made_evidence",
        "object mới. Vòng khép kín: dự đoán rỗng (chưa có bằng chứng) -> hành vi phòng thủ "
        "-> kết cục đặc, bằng đúng cỡ dự đoán, bị đọc thành bằng chứng cho nó. Bank run của "
        "Merton: 'tin đồn sai tự tạo ra bằng chứng cho chính nó'. cycle (đã dùng cho "
        "abilene-paradox) chỉ nói 'có lặp', không nói được chỗ bằng chứng là nội sinh"),
    "self-licensing": (
        "licence_overdraw",
        "object mới. Tín nhiệm kiếm được ở một việc tốt bị tiêu vào một việc kém sâu hơn "
        "hẳn — card ghi rõ 'xét tổng thể ngân sách, hai hành vi này không hề bù trừ nhau "
        "hợp lý', nên không dùng offset_safety (bù trừ THẬT, tổng không đổi). amber phân "
        "biệt với self-relevance-effect (mint) trong cùng batch"),
    "self-relevance-effect": (
        "dual_route",
        "cùng một mặt tiếp nhận, cùng một dữ kiện; khi có yếu tố tự liên hệ thì nó đi qua "
        "NHIỀU đường dẫn (mạng ký ức–cảm xúc–kinh nghiệm sẵn có) và để lại dấu vết đậm "
        "hơn. Rogers–Kuiper–Kirker 1977: nhóm tự liên hệ nhớ vượt cả nhóm xử lý theo nghĩa. "
        "Không lấy encoding_depth: trục ở đó là ĐỘ SÂU đối lại SỐ LẦN LẶP, còn ở đây là SỐ "
        "ĐƯỜNG MÓC TREO"),
    "self-serving-bias": (
        "esteem_ratchet",
        "object mới. Thành công: nguyên nhân ghi vào bên trong; thất bại cùng độ lớn: nguyên nhân "
        "đẩy ra ngoài, và chỉ phía thắng được tô đặc. Không dùng locus_flip: "
        "fundamental-attribution-error (card mà chính self-serving-bias trỏ tới) đã sở hữu bản "
        "mint, extrinsic-incentive-error giữ bản amber - ở đây trục là THẮNG/THUA của cùng một "
        "người, không phải mình đối với người khác"),
    "semmelweis-reflex": (
        "wall_rebuff",
        "object mới. Bằng chứng càng mạnh, càng trái chuẩn đã lập thì bị giữ càng xa: khoảng hở "
        "tỉ lệ với cỡ khối và KHÔNG khối nào chạm tới dải (bác bỏ thẳng, không tiếp nhận một "
        "phần). Không dùng inverse_weight: law-of-triviality đã sở hữu bản mint của quan hệ "
        "nghịch đó; gate thì vẫn có thứ lọt qua"),
    "serial-position-effect": (
        "u_shaped_recall",
        "object mới. Chữ U theo VỊ TRÍ trong chuỗi: hai đầu cao và đặc, hai vị trí giữa thấp và "
        "nhạt - primacy cộng recency. Không dùng hollow_chain: illusion-of-explanatory-depth đã "
        "sở hữu bản amber, và ở đó biến là chỗ-nào-được-tô trong một khung liền, không phải chiều "
        "cao theo vị trí"),
    "serial-recall-effect": (
        "ordered_chain",
        "object mới. Truy xuất phụ thuộc thứ tự đã học: cùng một bộ phần tử, có trục nối "
        "theo đúng trình tự thì lấy ra được, bốc rời khỏi trình tự thì không. Tách khỏi "
        "hollow_chain của serial-position-effect ngay trong batch này bằng biến CÓ/KHÔNG "
        "trục nối thay cho chỗ-nào-được-tô"),
    "social-comparison-bias": (
        "neighbor_scale",
        "object mới. Card nói rõ: tự đánh giá bằng cách so với người khác THAY VÌ theo một "
        "chuẩn khách quan — nên chuẩn phải có mặt mà bỏ rỗng, còn phần được tô đặc là "
        "khoảng hở so với người kề bên. contrast-effect (đã có ảnh) và juxtaposition nói về "
        "chênh lệch do đặt cạnh nhau; ở đây nội dung là CHUẨN NÀO được dùng để đo"),

    # ---- batch 2026-10-04 ----
    "social-desirability-bias": (
        "observed_lift",
        "xlsx gán divergence (một điểm rẽ nhiều nhánh) — card không có nhánh nào. "
        "Quan hệ cốt lõi: cùng một hành vi thật, con số TỰ THUẬT đổi vì có người đọc "
        "câu trả lời. observed_lift dựng đúng thế: dãy đều nhau, riêng phần nằm trong "
        "phạm vi được quan sát thì cao hẳn lên. hawthorne-effect (đã có ảnh) ăn phải "
        "divergence nên ô này còn trống"),
    "social-loafing": (
        "per_hand_decline",
        "object mới. xlsx gán nested_scope (vòng ngoài chứa lõi) — card không nói về "
        "phạm vi lồng nhau. dilution là họ gần nhất nhưng đã thuộc "
        "diffusion-of-responsibility ở đúng hue amber (dup check bắt được ngay vòng "
        "render đầu), và nghĩa của dilution là 'mỗi phần loãng tới mức không đủ KÍCH "
        "HOẠT' — một ngưỡng, tức bystander. Social loafing không có ngưỡng nào: thí "
        "nghiệm Ringelmann 1913 đo nỗ lực MỖI người giảm liên tục theo cỡ nhóm (2 "
        "người = 186%, 8 người = 392%). Hình mới khoá bề rộng cột không đổi để biến "
        "duy nhất là chiều cao mỗi người"),
    "source-confusion": (
        "source_swap",
        "xlsx gán hierarchy (cha–con) — sai hẳn. source_swap đã có sẵn trong registry "
        "và được viết đúng cho quan hệ này: khối nội dung tô ĐẶC (ký ức nguyên vẹn) "
        "đội mái tam giác của nguồn đã sinh ra nó, nhưng đường dẫn duy nhất chạy sang "
        "hình tròn — sai ở chỗ quy nguồn, không ở nội dung. Chưa card nào dùng. Khác "
        "gap_fill (confabulation: vá chỗ hổng) và cue_lock (cue-dependent-forgetting: "
        "không mở ra được)"),
    "spacing-effect": (
        "spaced_repeats",
        "object mới. xlsx gán cycle (vòng lặp khép kín) — spacing effect không khép "
        "vòng, nó trải trên một trục thời gian. Tiền đề của card là TỔNG thời gian ôn "
        "BẰNG NHAU, chỉ khác mật độ; không hình nào có sẵn giữ được tiền đề đó: "
        "steep_then_flat nói độ cong của đường quên, echo nói số lần lặp. Hình mới "
        "khoá cứng 4 vạch mỗi hàng, biến duy nhất là khoảng cách"),
    "spotlight-effect": (
        "share_of_field",
        "object mới. xlsx gán divergence — không có nhánh nào. Hai ứng viên có sẵn đều "
        "hỏng: foreground_swell đã thuộc identifiable-victim-effect ở hue mint (dup "
        "check bắt), còn asymmetric_probe render ra hai vòng tròn có chấm giữa, ở 64px "
        "đọc thành CẶP MẮT KÍNH và độ lệch của hai mũi thăm dò biến mất — vi phạm cả "
        "'không vật thể nhận dạng được' lẫn 'đọc được ở 64px' (đã render rồi nhìn mới "
        "thấy). signal_leak thì đúng nghĩa illusion-of-transparency, phiên bản hướng "
        "nội, không phải card này. Hình mới giữ hai khung bằng nhau và chỉ đổi tỉ phần "
        "mình chiếm trong trường chú ý — đúng thí nghiệm Gilovich 2000"),
    "status-quo-bias": (
        "preset_holds",
        "object mới. xlsx gán divergence. latch là định nghĩa nguyên văn của card "
        "nhưng dual-process-theory đã chiếm nó ở đúng hue amber (dup check bắt được) — "
        "một gán sai nên báo lại chứ không tự sửa ở batch này. latch còn dựng một BỨC "
        "TƯỜNG: bất đối xứng nằm ở công sức phải vượt. Ở status quo bias không ai bị "
        "chặn — Samuelson–Zeckhauser 1988 giữ nguyên nội dung danh mục, chỉ thêm nhãn "
        "'đang nắm giữ', và TỈ LỆ CHỌN vọt lên. Hình mới: hai phương án giống nhau tới "
        "từng chi tiết, một cái có bệ, thanh tỉ lệ chọn dưới nó cao gấp nhiều lần"),
    "stereotyping": (
        "trait_from_band",
        "object mới. xlsx gán divergence. Chiều của quan hệ mới là điểm chết: "
        "stereotyping đi NHÓM → CÁ THỂ, còn one_for_all có sẵn đi CÁ THỂ → NHÓM "
        "(group-attribution-error, đã render). tint_carryover thì cần một ô CÓ bằng "
        "chứng rồi lây sang ô kề (halo-effect) — ở đây không cá thể nào từng được "
        "quan sát. Hình mới: dải nhóm đặc, ba ô thành viên mang sắc độ của dải với "
        "ruột rỗng, nét dọc chỉ chiều xuống. Khác group_tint_applied (implicit-stereotypes, "
        "cùng hue mint): ở đó một CỤM nhỏ nối sang MỘT cá thể lớn; ở đây một DẢI "
        "liền sơn xuống BA cá thể, không cá thể nào có bằng chứng riêng"),
    "streisand-effect": (
        "cover_widens_reach",
        "object mới. xlsx gán divergence. rebound (bật ngược) là họ gần nhất nhưng đã "
        "thuộc backfire-effect ở hue mint, và dùng rebound/amber cho card này sẽ ra "
        "hai ô chỉ khác màu — vi phạm điều kiện 'không hai ô nào trông giống nhau'. "
        "Hơn nữa đại lượng đổi ở Streisand không phải quỹ đạo quay đầu mà là BÁN KÍNH "
        "lan (6 lượt tải → 420.000 lượt truy cập, lõi thông tin không to thêm). Hình "
        "mới khoá hai lõi bằng nhau, chỉ vòng lan nở ra khi có dải che đè lên"),
    "subadditivity-effect": (
        "unpacked_overshoot",
        "object mới. xlsx gán hierarchy. Card là một bất đẳng thức quanh một mốc: "
        "cùng một tập sự kiện, mô tả gộp → ước lượng DƯỚI mức thật, tách gói → tổng "
        "VƯỢT mức thật (58% vs 73%). granularity nói về phân giải cá thể và không có "
        "mốc nào bị vượt; proportion nói phần/tổng. Hình mới giữ một đường mức liền "
        "qua cả hai cột để tiền đề 'cùng một tập' không bị bác"),
    "subjective-validation": (
        "verdict_ignores_fit",
        "object mới. xlsx gán hierarchy. barnum-effect (card gần nhất) đã render bằng "
        "nested_scope. Nội dung riêng của card này: phán quyết 'đúng ghê' KHÔNG đi "
        "theo mức khớp thật — nên hình phải có cả thước khớp (phần chồng lấn giảm "
        "dần) lẫn phán quyết (ba thanh bằng nhau tuyệt đối). tint_carryover thiếu "
        "thước khớp, consensus_merge nói về nhập khối"),

    # ---- batch 2026-10-05 (suggestibility → time-saving-bias) — xlsx gán 5 hierarchy
    # + 4 branching + 1 nesting, tức 9/10 card sẽ nhận đúng 2 hình. Chẩn đoán lại toàn
    # bộ theo `back`. Mọi object sát nghĩa nhất đã bị card khác chiếm, nên batch này
    # viết 10 object mới trong illus.py thay vì dùng lại hình ở hue còn lại (hai ô
    # trông giống nhau là lỗi contact sheet).
    "suggestibility": (
        "prompt_shaped_answer",
        "gợi ý từ ngoài cấp HÌNH DẠNG cho câu trả lời, và không có nét nối nào giữa "
        "khuôn và khối phản hồi — người trả lời đọc nó thành của mình. hierarchy nói "
        "quan hệ cha-con, không có gì liên quan. overwrite_seam sát nghĩa nhưng đã "
        "thuộc misinformation-effect, mà chính card này ghi rõ nó RỘNG hơn "
        "misinformation-effect: suggestibility không cần ký ức sẵn có để bị ghi đè"),
    "sunk-cost-fallacy": (
        "past_outweighs_ahead",
        "một vách 'bây giờ': đại lượng quyết định lựa chọn nằm BÊN TRÁI vách, phía lẽ "
        "ra không được tính. hierarchy không diễn được chuyện này. pull (anchoring) "
        "thiếu trục thời gian — sunk cost không phải một mỏ neo trên cùng mặt phẳng, "
        "nó là chi phí đã chôn được mang sang phép tính tương lai"),
    "survivorship-bias": (
        "sample_minus_eliminated",
        "khung dữ liệu quan sát được chỉ chứa nhóm sống sót, nhóm bị loại đông hơn hẳn "
        "và nằm ngoài khung, tường khung vẽ liền (không bị che — chưa bao giờ vào "
        "được). hierarchy sai hẳn. gate vẽ quá trình lọc và đã thuộc authority-bias/"
        "automation-bias; ở đây quá trình đã xong, cái phải thấy là bảng dữ liệu còn lại"),
    "swimmers-body-illusion": (
        "trait_precedes_frame",
        "lỗi của card là CHIỀU nhân quả, không phải việc lọc: ba khối bằng nhau xuất "
        "hiện đặc TRƯỚC khung, đặc trong khung, rỗng SAU khung — phần 'do hoạt động "
        "tạo ra' bỏ rỗng. nesting/nested_scope chỉ nói lồng nhau. Phải khác hẳn "
        "survivorship-bias dù hai card là họ hàng: ở đó cái vắng là nhóm bị loại, ở "
        "đây cái vắng là hệ quả được gán cho hoạt động"),
    "system-justification": (
        "braced_from_below",
        "điểm gây tranh cãi nhất của card: thanh đỡ duy nhất của cấu trúc mọc lên từ "
        "chính bậc rỗng — nhóm yếu thế biện minh mạnh nhất. hierarchy vẽ đúng cấu trúc "
        "nhưng dừng ở đó, mà cấu trúc không phải nội dung card; NGUỒN của lực đỡ mới là"),
    "telescoping-effect": (
        "recall_slides_on_axis",
        "hai độ lệch NGƯỢC CHIỀU quanh mốc hiện tại trên một trục thời gian (forward + "
        "backward telescoping). branching/divergence chỉ có một điểm rẽ nhánh, mất sạch "
        "nửa card. extreme_then_center cũng đối xứng qua mốc nhưng nói hồi quy về trung "
        "bình — ở đây không có lực kéo về trung tâm, chỉ có vị trí bị định vị sai"),
    "testing-effect": (
        "pulled_out_deeper",
        "chiều của động tác mới là nội dung: LẤY RA (một mẩu rút khỏi hốc của chính "
        "khối) cho dấu vết sâu hơn nhiều lượt nạp vào. branching sai hẳn. encoding_depth "
        "đã thuộc levels-of-processing-effect và nói về độ sâu xử lý; self_built thuộc "
        "generation-effect (tự dựng vs nhận nguyên si) — cả hai là card họ hàng được "
        "link ngay trong bài, nên phải phân biệt được bằng mắt"),
    "third-person-effect": (
        "uniform_field_self_blank",
        "dải tác động chạy LIỀN dưới cả bốn ô bằng nhau, chỉ ô 'mình' để rỗng — trường "
        "phủ như nhau, khác nhau ở việc có tự xếp mình vào nhóm bị phủ. branching sai. "
        "self_exempt đã thuộc optimism-bias và ở đó biến là CHIỀU CAO cột tự ước lượng; "
        "ở đây mọi ô cao bằng nhau, biến là được tô hay không"),
    "time-discounting": (
        "distance_discounts_fill",
        "hai khung cao BẰNG NHAU tuyệt đối (phần thưởng danh nghĩa bằng nhau) trên một "
        "trục thời gian, phần tô teo đi theo khoảng cách. branching sai. steep_then_flat "
        "đã thuộc hyperbolic-discounting và vẽ ĐỘ CONG của đường chiết khấu — đúng là "
        "card em của card này, nên hình phải khác: ở đây chỉ hai mốc và đại lượng là "
        "phần giá trị còn lại trong khung; discounted_across_line đã thuộc "
        "reactive-devaluation"),
    "time-saving-bias": (
        "equal_step_unequal_gain",
        "quan hệ PHI TUYẾN: hai mẩu tăng tốc bằng nhau tuyệt đối cho hai kết quả chênh "
        "hẳn, và khung rỗng cao bằng kết quả bên trái chính là lượng trực giác tưởng sẽ "
        "nhận được. branching sai. inert_input ngược chiều (hai đầu vào chênh, hai kết "
        "quả bằng nhau); anchoring/pull chỉ bắt được phần neo, không bắt được tính phi tuyến"),

}

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
    # Article Index (230 dòng) đã phủ 100% từ 2026-10-06. Các card được thêm vào
    # content/stuff/ sau khi xlsx được sinh ra thì không có dòng nào trong đó, nên
    # từ 2026-10-12 danh sách batch được nối thêm EXTRA_CARDS (khai báo cuối file).
    out += EXTRA_CARDS
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


# ---------------------------------------------------------------------------
# Batch ngoài Article Index. xlsx chỉ phủ 230/342 card; phần còn lại được chẩn
# đoán trực tiếp từ `back` của từng card rồi khai báo ở đây — shape ghi "(ngoài
# xlsx)" để báo cáo phân biệt được nguồn, metaphor lấy từ OVERRIDES như mọi card khác.
# ---------------------------------------------------------------------------

OVERRIDES.update({
    "action-bias": (
        "best_off_board",
        "card không nằm trong xlsx nên không có shape nào để đối chiếu. Quan hệ cốt lõi "
        "nằm ở bước DỰNG tập phương án, không ở bước chấm: Bar-Eli cho thấy đứng yên có "
        "kỳ vọng tốt hơn, nhưng nó không bao giờ lên bảng so sánh — đúng chữ trong "
        "strategy của card. Khác `visible_hand` (omission-bias, mint) vốn nói về quy kết "
        "tác nhân khi hậu quả đã xảy ra; ở đây chưa có hậu quả nào, chỉ có một tập thiếu"),
    "afterimage-effect": (
        "complement_rebound",
        "cơ chế là cặp đối lập Hering mất điểm cân bằng, nên hình phải có một đường cân "
        "bằng và hai độ lệch ĐỐI XỨNG quanh nó, phần sau để rỗng vì không có kích thích "
        "nào ở đó. Khác `setpoint_return` (hedonic adaptation) vốn vẽ đường trở về mức "
        "nền; dư ảnh không phải sự trở về mà là một độ lệch mới ở phía chưa bị dùng"),
    "autokinetic-effect": (
        "drift_attribution",
        "phép trừ chuyển động mất mẫu số khi bối cảnh biến mất — nên biến phải là SỰ CÓ "
        "MẶT của khung tham chiếu, và nét rung phải giữ y nguyên để thấy nó chỉ đổi chủ. "
        "Không chọn nhánh Sherif (chuẩn nhóm) vì `prompt_shaped_answer` đã thuộc "
        "suggestibility, và `back` của card đặt trọng tâm ở cơ chế thị giác"),
    "barbell-strategy": (
        "ends_loaded",
        "điểm phân biệt với đa dạng hoá là phần GIỮA bị bỏ trống có chủ ý, nên khoảng "
        "giữa phải được vẽ ra thành một khung rỗng chứ không để trắng. Ba cược nhỏ rời "
        "nhau để nói điều kiện không-tương-quan — bẫy thứ hai card nêu. Khác `tail_event` "
        "(black-swan-theory, amber): ở đó đuôi là thứ xảy đến, ở đây là thứ được chọn"),
    "barber-pole-illusion": (
        "aperture_cue",
        "aperture problem: thông tin thiếu ngay từ gốc, và hệ thị giác lấy manh mối ở ĐẦU "
        "MÚT trên cạnh dài của cửa sổ. Nên hình phải giữ nguyên độ nghiêng vạch, đổi hình "
        "cửa sổ, và đánh dấu đầu mút — đó là toàn bộ lập luận 'hướng ta thấy là hình dạng "
        "của cái khung'. Khác `coincident_view` vì ở đây hai khung khác hình nhau"),
    "bayesian-updating": (
        "weighted_shift",
        "nội dung là phép TRỘN CÓ TỈ LỆ, nên phải vẽ hai lần với trọng số đảo nhau mới "
        "thấy được tính tỉ lệ; vạch kết quả không chạm cực nào vì card bác bỏ đúng hai "
        "cách đọc 'bỏ qua bằng chứng' và 'lật ngược vì một mẫu nhỏ'. Khác `balance` vốn "
        "chỉ nói cán cân lệch có hướng, không nói mức lệch do đâu quyết định"),
    "ben-franklin-effect": (
        "act_tints_actor",
        "chiều tác động là người CHO đổi thái độ, và điều kiện tắt là cảm giác bị ép — "
        "nên thanh đè phải có mặt như biến điều tiết, giống cách `liking_flip` vẽ biến "
        "điều tiết ra. Khác `effort_price` (effort-justification + ikea-effect đã chiếm "
        "cả mint và amber) vì ở đó vật được định giá bằng công sức, còn ở đây đối tượng "
        "được định giá lại là một NGƯỜI và đại lượng là sắc độ thái độ"),
    "binocular-rivalry": (
        "exclusive_state",
        "nội dung nằm ở cái KHÔNG xảy ra: không có lưới caro. Nên hình phải cho hai trạng "
        "thái chiếm cùng một chỗ mà chỉ một cái được tô. Khác `overlap_phases` (vùng giao "
        "đậm lên) vì đó chính là phép trộn mà hiện tượng này bác bỏ — dùng nó sẽ vẽ ra "
        "đúng câu trả lời sai mà front của card đặt ra"),
    "bounded-rationality": (
        "stop_at_threshold",
        "satisficing: đặt ngưỡng, dừng ở phương án đầu vượt ngưỡng, và cái tối ưu vẫn còn "
        "đó nhưng chưa bao giờ được mở ra vì tìm kiếm có giá. Phần rỗng phải nằm SAU vạch "
        "dừng mới nói được là chi phí tìm kiếm chứ không phải lỗi phán đoán. Khác "
        "`noticed_from_here` ở chiều tô: ở đó phần rỗng nằm trước vạch"),
    "calibrated-confidence": (
        "identity_line_shortfall",
        "hiệu chỉnh là khớp giữa mức phát biểu và tần suất đúng, nên mốc phải là đường "
        "đồng nhất CHO TRƯỚC, không phải đường khớp từ dữ liệu. Khoảng rơi nới rộng dần "
        "để mang luôn hard-easy-effect. Khác `narrow_interval` (overconfidence-effect, "
        "mint) vốn lấy bề rộng khoảng tin cậy làm đại lượng, và khác `fitted_overreach` "
        "(illusion-of-validity) vốn nói đường khớp chạy ra ngoài vùng có dữ liệu"),
})

# --- batch 2026-10-13: 10 card đầu ngoài Article Index, lô thứ hai. Không có dòng nào
# trong xlsx nên KHÔNG có "shape sai" để sửa — mỗi entry dưới đây là chẩn đoán gốc từ
# `back` của card. Chín hình mới được viết cho lô này; `network` là hình có sẵn.
OVERRIDES.update({
    "certainty-effect": (
        "endpoint_premium",
        "quan hệ cốt lõi: hai mức tăng xác suất BẰNG NHAU được gán trọng số lệch hẳn, và "
        "cái lệch dồn vào đúng điểm mút 100% — nghịch lý Allais (1953) đo chính chỗ đó. "
        "endpoint_premium vẽ vách chặn ở mút cộng hai mẩu tăng bằng nhau tuyệt đối. Khác "
        "`value_curve_s` (prospect-theory) vốn vẽ cả hàm giá trị, và khác "
        "`equal_step_unequal_gain` (weber) vốn nói độ cong đều đặn chứ không nói điểm mút"),
    "change-deafness": (
        "label_holds",
        "cái được lưu là NHÃN thô ('một người đàn ông đang nói'), nên một thay đổi không "
        "phá vỡ nhãn thì hệ thống báo là không có gì đổi. label_holds vẽ hai cảnh cùng "
        "khung nhãn y hệt, nội dung lệch một phần tử, dải báo cáo để rỗng. Khác `veil` vì "
        "nội dung mới không bị che chút nào, và khác `granularity` vì hai bên cùng độ "
        "phân giải — cái lệch nằm giữa hai thời điểm, không giữa hai phía"),
    "checker-shadow-illusion": (
        "band_discounted",
        "Adelson (1995): hai ô CÙNG MỘT giá trị xám, một ô nằm trong vùng bóng, và phán "
        "đoán lệch hẳn vì hệ thị giác trừ ngữ cảnh chiếu sáng ra. band_discounted giữ hai "
        "khối cùng fill (tiền đề) và cho dải phủ trùm hẳn một khối. Khác `edge_reads_true` "
        "vì ở đó ngữ cảnh nằm trên đường biên của chính khối, còn ở đây là một vùng bao"),
    "cocktail-party-effect": (
        "attended_stream_leak",
        "Cherry (1953) + Moray (1959): kênh bị bỏ qua không bị TẮT, nó bị HẠ MỨC, và một "
        "mục ngưỡng thấp (tên riêng) vẫn vượt lên — đúng chỗ Treisman thay mô hình lọc "
        "tất-hoặc-không bằng mô hình suy giảm. attended_stream_leak vẽ luồng rỗng (hạ mức, "
        "không tắt) kèm một mẩu đặc nằm trong lòng nó. `beam` không có chỗ cho cái lọt "
        "qua, `gate` thì cần một dòng chảy qua cửa, ở đây chỉ có ba kênh song song"),
    "color-constancy": (
        "illuminant_divided_out",
        "quan hệ: tín hiệu vật lý vào mắt đổi mạnh theo nguồn sáng, thuộc tính suy ra GIỮ "
        "NGUYÊN — suy luận vô thức của Helmholtz. illuminant_divided_out vẽ ba dải nguồn "
        "sáng khác sắc độ trên ba vật cùng sắc độ, ba thanh đọc ra bằng nhau tuyệt đối. "
        "Cùng cơ chế với checker-shadow nhưng NGƯỢC chiều kết quả, nên phải là hai hình "
        "khác nhau: ở đây phép trừ ngữ cảnh chạy đúng, ở kia cảnh được dựng để lừa"),
    "compounding-effect": (
        "multiplied_base",
        "kết quả kỳ này là điểm xuất phát kỳ sau, nên đường đi cong LÊN và phần lớn kết "
        "quả rơi vào đoạn cuối. multiplied_base cho bốn cột gấp đôi dần cộng một nét thẳng "
        "kỳ vọng tuyến tính mà hai cột đầu còn nằm dưới — chính đoạn 'trông như đứng yên' "
        "khiến người ta bỏ dở. Khác `ratchet` (chỗ đứng đã nhận, không có cấp số nhân và "
        "không có mốc tuyến tính để so) và khác `steep_then_flat` ở chiều cong"),
    "compromise-effect": (
        "middle_by_position",
        "Simonson (1989): cùng một sản phẩm được chọn nhiều khi nó là lựa chọn GIỮA và ít "
        "khi nó thành cực của một tập khác — tỉ lệ chọn bám theo vị trí tương đối. "
        "middle_by_position giữ đúng một cột xuất hiện ở cả hai tập và cho nó mất tô khi "
        "rơi về cực. Khác `foil` (decoy) vì phương án thêm vào ở đây là một cực HỢP LỆ, "
        "không bị lấn át — card tự phân biệt chính điểm này"),
    "connectionism": (
        "network",
        "tri thức nằm ở TẬP TRỌNG SỐ phân tán trên toàn mạng, không định vị được ở một "
        "đơn vị nào — `network` là hình đúng nghĩa đen và nghĩa cấu trúc của card. Hue "
        "mint còn trống (amber đã thuộc apophenia). Cân nhắc viết hình riêng cho luận "
        "điểm 'hành vi tuân theo quy tắc không chứng minh có quy tắc bên trong', nhưng ở "
        "128px một khuôn quy tắc rỗng cộng một lưới là quá đông chi tiết dưới 8px"),
    "crux-identification": (
        "load_bearing_one",
        "phép thử ngược: lý do nào mà nếu sai thì kết luận sụp. load_bearing_one vẽ bốn "
        "thanh rỗng DỪNG TRƯỚC khi chạm tấm kết luận và đúng một thanh đặc chạm hẳn — "
        "quan hệ nhị phân chịu lực / không chịu lực. Khác `vital_few` (pareto) vì ở đó đại "
        "lượng là tỉ phần đóng góp; khác `fewer_supports` vì ở đó chỉ đếm số chỗ đỡ"),
    "cutaneous-rabbit-illusion": (
        "interpolated_path",
        "Geldard & Sherrick (1972): da chỉ bị chạm tại ĐÚNG HAI vị trí, nhưng cảm nhận là "
        "một chuỗi điểm rải đều dọc quãng giữa — não nội suy, và nội suy ngược cả thời "
        "gian. interpolated_path vẽ hai cặp chấm đặc ở hai đầu cộng ba chấm rỗng cách đều. "
        "Khác `hollow_chain` (TOT) vì ở đó có khung bao và nội dung là truy xuất MỘT PHẦN; "
        "ở đây phần giữa là thứ được BỔ SUNG. Khác `gap_fill` vì không có vật liệu lạ nào"),
})

EXTRA_CARDS = [
    dict(n=1001, slug="action-bias", title="Action Bias", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1002, slug="afterimage-effect", title="Afterimage Effect", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1003, slug="autokinetic-effect", title="Autokinetic Effect", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1004, slug="barbell-strategy", title="Barbell Strategy", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1005, slug="barber-pole-illusion", title="Barber Pole Illusion", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1006, slug="bayesian-updating", title="Bayesian Updating", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1007, slug="ben-franklin-effect", title="Ben Franklin Effect", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1008, slug="binocular-rivalry", title="Binocular Rivalry", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1009, slug="bounded-rationality", title="Bounded Rationality", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1010, slug="calibrated-confidence", title="Calibrated Confidence", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1011, slug="certainty-effect", title="Certainty Effect", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1012, slug="change-deafness", title="Change Deafness", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1013, slug="checker-shadow-illusion", title="Checker Shadow Illusion", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1014, slug="cocktail-party-effect", title="Cocktail Party Effect", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1015, slug="color-constancy", title="Color Constancy", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1016, slug="compounding-effect", title="Compounding Effect", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1017, slug="compromise-effect", title="Compromise Effect", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1018, slug="connectionism", title="Connectionism", shape="(ngoài xlsx)", hue="mint"),
    dict(n=1019, slug="crux-identification", title="Crux Identification", shape="(ngoài xlsx)", hue="amber"),
    dict(n=1020, slug="cutaneous-rabbit-illusion", title="Cutaneous Rabbit Illusion", shape="(ngoài xlsx)", hue="mint"),
]


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
        print(f"{c['slug']:<40} {c['shape']:<14} {metaphor:<16} {hue}"
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
        dupes = {}
        for c in index:
            f = os.path.join(ASSETS, f"{c['slug']}.png")
            if os.path.exists(f):
                dupes.setdefault(hashlib.md5(open(f, "rb").read()).hexdigest(),
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
