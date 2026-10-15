package vn.edu.bigdata.m1;

import com.mongodb.MongoException;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@Controller
class SampleController {
    private final SampleResults results;
    SampleController(SampleResults results) { this.results = results; }

    @GetMapping("/")
    String page(Model model) { return render(model, null, null, List.of()); }

    @PostMapping("/recommend")
    String recommend(@RequestParam String runId, @RequestParam long version,
                     @RequestParam(required = false) List<String> items, Model model) {
        return render(model, runId, version, items == null ? List.of() : items);
    }

    private String render(Model model, String submittedRun, Long submittedVersion, List<String> input) {
        try {
            SampleResults.Snapshot data = results.snapshot();
            model.addAttribute("data", data);
            model.addAttribute("recommendations", List.of());
            model.addAttribute("selected", new HashSet<>(input));
            if (submittedRun != null) {
                Set<String> catalog = new HashSet<>(data.items().stream().map(d -> d.getString("stock_code")).toList());
                if (!data.runId().equals(submittedRun) || data.version() != submittedVersion) {
                    model.addAttribute("message", "Lượt dữ liệu đã đổi. Tải lại lựa chọn rồi gửi giỏ.");
                } else if (input.isEmpty()) {
                    model.addAttribute("message", "Hãy chọn ít nhất một sản phẩm.");
                } else if (!catalog.containsAll(input)) {
                    model.addAttribute("message", "Giỏ có mã không hợp lệ; hãy chọn lại từ danh mục.");
                } else {
                    List<RuleRanking.Rule> ranked = RuleRanking.recommend(data.rules(), input, data.k());
                    model.addAttribute("recommendations", ranked);
                    model.addAttribute("message", ranked.isEmpty() ? "Không có luật gợi ý cho giỏ này." : "Gợi ý từ luật của lượt mẫu hiện tại.");
                }
            }
        } catch (MongoException exc) {
            model.addAttribute("error", "Không kết nối được MongoDB mẫu. Kiểm tra tiến trình M1.");
        } catch (IllegalStateException exc) {
            model.addAttribute("error", exc.getMessage());
        }
        return "sample";
    }

    /** Endpoint đọc để nhận receipt M1; không tạo public API sản phẩm. */
    @GetMapping("/m1/verification")
    @ResponseBody
    ResponseEntity<Map<String, Object>> verification() {
        try {
            Map<String, Object> proof = results.proof(results.snapshot());
            return ResponseEntity.status(Boolean.TRUE.equals(proof.get("all_passed")) ? 200 : 503).body(proof);
        } catch (MongoException | IllegalStateException exc) {
            return ResponseEntity.status(503).body(Map.of("all_passed", false, "mode", "SAMPLE", "error", "M1_RESULT_UNAVAILABLE"));
        }
    }
}
