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
