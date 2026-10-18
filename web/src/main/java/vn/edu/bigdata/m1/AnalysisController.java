package vn.edu.bigdata.m1;

import com.mongodb.MongoException;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@Controller
@ConditionalOnProperty(name="app.mode", havingValue="DEVELOPMENT")
public class AnalysisController {
    static final int PAGE_SIZE=25;
    private final AnalysisResults results;
    AnalysisController(AnalysisResults results) { this.results=results; }
    record Page<T>(List<T> rows, int page, int pages, int total) {}
    record Metric(String method, long queries, long hits, long nonempty, String recall, String rate) {}
    static class Input extends RuntimeException { Input(String message) { super(message); } }

    @GetMapping("/") String overview(@RequestParam MultiValueMap<String,String> p, Model m, HttpServletResponse r) { return render("overview",p,m,r,false); }
    @GetMapping("/patterns") String patterns(@RequestParam MultiValueMap<String,String> p, Model m, HttpServletResponse r) { return render("patterns",p,m,r,false); }
    @GetMapping("/basket") String basket(@RequestParam MultiValueMap<String,String> p, Model m, HttpServletResponse r) { return render("basket",p,m,r,false); }
    @PostMapping(value="/recommend", consumes="application/x-www-form-urlencoded")
    String recommend(@RequestParam MultiValueMap<String,String> p, Model m, HttpServletResponse r) { return render("basket",p,m,r,true); }

    private String render(String view, MultiValueMap<String,String> p, Model m, HttpServletResponse response, boolean submitted) {
        response.setHeader("Cache-Control","no-store");
        m.addAttribute("view",view); m.addAttribute("selected",Set.of()); m.addAttribute("recommendations",List.of());
        m.addAttribute("query",""); m.addAttribute("sort",view.equals("overview")?"baskets":"confidence");
        m.addAttribute("kind","rules"); m.addAttribute("min",0.0); m.addAttribute("size",0);
        try {
            AnalysisResults.Snapshot data=results.snapshot(); // pointer read only here, once
            m.addAttribute("data",data);
            Set<String> catalog=new HashSet<>(data.items().stream().map(AnalysisResults.Item::code).toList());
            List<String> input=p.getOrDefault("items",List.of());
            Set<String> valid=new LinkedHashSet<>(input); valid.retainAll(catalog);
            m.addAttribute("selected",valid); // retain valid choices even when another field is invalid
            prepareOverview(data,m,"baskets","",0);
            preparePatterns(data,m,"rules","confidence","",0,0,0);
            Set<String> allowed=view.equals("overview")?Set.of("runId","version","page","sort","q"):
                view.equals("patterns")?Set.of("runId","version","page","sort","q","kind","min","size"):
                    Set.of("runId","version","items","q");
            if(!allowed.containsAll(p.keySet())) throw new Input("Tham số không được hỗ trợ; chỉ gửi trường của biểu mẫu.");
            if(submitted && (!p.containsKey("runId") || !p.containsKey("version"))) throw new Input("Thiếu mã lượt/phiên của biểu mẫu. Hãy tải lại trang.");
            if(p.containsKey("runId") || p.containsKey("version")) {
                String run=scalar(p,"runId",""); long version=integer(p,"version",0,Long.MAX_VALUE);
                if(!data.runId().equals(run) || version!=data.version()) {
                    response.setStatus(409); m.addAttribute("stale",true);
                    m.addAttribute("message","Dữ liệu đã đổi hoặc biểu mẫu thuộc phiên cũ. Tải lại trang rồi chọn giỏ theo lượt hiện tại.");
                    return "analysis";
                }
            }
            String q=scalar(p,"q",""); if(q.length()>160) throw new Input("Từ tìm kiếm tối đa 160 ký tự.");
            m.addAttribute("query",q);
            if(view.equals("overview")) {
                String sort=scalar(p,"sort","baskets");
                if(!Set.of("baskets","quantity","code").contains(sort)) throw new Input("Thứ tự sắp xếp không hợp lệ.");
                prepareOverview(data,m,sort,q,integer(p,"page",0,1000000)); m.addAttribute("sort",sort);
            } else if(view.equals("patterns")) {
                String kind=scalar(p,"kind","rules"), sort=scalar(p,"sort",kind.equals("rules")?"confidence":"support");
                if(!Set.of("rules","itemsets").contains(kind) || !Set.of("confidence","lift","support","frequency","code").contains(sort)
                    || (kind.equals("rules") && sort.equals("frequency"))
                    || (kind.equals("itemsets") && Set.of("confidence","lift").contains(sort))) throw new Input("Loại bảng/thứ tự không hợp lệ.");
                double min=decimal(p,"min"); int size=integer(p,"size",0,data.items().size());
                preparePatterns(data,m,kind,sort,q,min,size,integer(p,"page",0,1000000));
                m.addAttribute("kind",kind); m.addAttribute("sort",sort); m.addAttribute("min",min); m.addAttribute("size",size);
            } else if(submitted) {
                if(input.size()>data.items().size()*2 || input.stream().anyMatch(s -> s.length()>160)) throw new Input("Input vượt giới hạn kỹ thuật; không cắt giỏ. Hãy gửi lại từ danh mục.");
                if(input.isEmpty()) throw new Input("Hãy chọn ít nhất một sản phẩm.");
                if(!catalog.containsAll(input)) throw new Input("Giỏ có mã không thuộc catalog train; lựa chọn hợp lệ được giữ lại. Hãy kiểm tra và gửi lại.");
                List<RuleRanking.Rule> ranked=RuleRanking.recommend(data.rules(),valid,data.k());
                m.addAttribute("recommendations",ranked);
                m.addAttribute("message",ranked.isEmpty()?"Không có luật gợi ý cho giỏ hợp lệ này. Không dùng fallback phổ biến.":"Gợi ý từ luật DEVELOPMENT; mỗi mã giữ một luật tốt nhất.");
            }
        } catch(Input e) { response.setStatus(400); m.addAttribute("message",e.getMessage()); }
        catch(MongoException e) { response.setStatus(503); m.addAttribute("data",null); m.addAttribute("error","Không kết nối được dữ liệu MongoDB. Thử lại khi nguồn sẵn sàng."); }
        catch(AnalysisResults.Unavailable e) { response.setStatus(503); m.addAttribute("data",null); m.addAttribute("error",e.getMessage()); }
        return "analysis";
    }

    private void prepareOverview(AnalysisResults.Snapshot d, Model m, String sort, String query, int page) {
        Comparator<AnalysisResults.Popular> order=switch(sort) {
            case "quantity" -> Comparator.comparingLong(AnalysisResults.Popular::quantity).reversed();
            case "code" -> Comparator.comparing(AnalysisResults.Popular::code,RuleRanking::codePointOrder);
            default -> Comparator.comparingLong(AnalysisResults.Popular::baskets).reversed();
        };
        m.addAttribute("popular",page(d.popular().stream().filter(i -> matches(i.code(),query)).sorted(order.thenComparing(AnalysisResults.Popular::code,RuleRanking::codePointOrder)).toList(),page));
        m.addAttribute("maxInvoices",Math.max(1,d.months().stream().mapToLong(AnalysisResults.Month::invoices).max().orElse(1)));
        m.addAttribute("maxAmount",d.months().stream().map(AnalysisResults.Month::amount).max(java.math.BigDecimal::compareTo).orElse(java.math.BigDecimal.ONE));
        m.addAttribute("maxSizeCount",Math.max(1,d.sizes().stream().mapToLong(AnalysisResults.Size::baskets).max().orElse(1)));
    }
    private void preparePatterns(AnalysisResults.Snapshot d, Model m, String kind, String sort, String query, double min, int size, int p) {
        if(kind.equals("rules")) {
            Comparator<RuleRanking.Rule> order=switch(sort) {
                case "lift" -> Comparator.comparingDouble(RuleRanking.Rule::lift).reversed();
                case "support" -> Comparator.comparingDouble(RuleRanking.Rule::support).reversed();
                case "code" -> Comparator.comparing(RuleRanking.Rule::consequent,RuleRanking::codePointOrder);
                default -> RuleRanking.ORDER;
            };
            m.addAttribute("rulePage",page(d.rules().stream().filter(r -> r.support()>=min && (size==0 || r.antecedent().size()==size)
                && (matches(d.describe(r.antecedent()),query) || matches(r.consequent()+" "+d.name(r.consequent()),query)))
                .sorted(order.thenComparing(RuleRanking.ORDER)).toList(),p));
        } else {
            Comparator<AnalysisResults.Itemset> order=sort.equals("code")?Comparator.comparing(AnalysisResults.Itemset::key,RuleRanking::codePointOrder):
                Comparator.comparingLong(AnalysisResults.Itemset::frequency).reversed();
            m.addAttribute("setPage",page(d.itemsets().stream().filter(s -> s.support()>=min && (size==0 || s.codes().size()==size)
                && matches(d.describe(s.codes()),query)).sorted(order.thenComparing(AnalysisResults.Itemset::key,RuleRanking::codePointOrder)).toList(),p));
        }
        metrics(d,m);
    }
    private void metrics(AnalysisResults.Snapshot d, Model m) {
        var all=AnalysisResults.doc(AnalysisResults.doc(d.manifest(),"development"),"all");
        List<Metric> metrics=new ArrayList<>();
        for(String method:List.of("rules","baseline")) {
            var metric=AnalysisResults.doc(all,method); long n=AnalysisResults.count(metric,"queries"), hits=AnalysisResults.count(metric,"hits"), nonempty=AnalysisResults.count(metric,"with_recommendations");
            metrics.add(new Metric(method.equals("rules")?"Luật thuần":"Baseline phổ biến train",n,hits,nonempty,percent(hits,n),percent(nonempty,n)));
        }
        m.addAttribute("metrics",metrics);
    }
    static String percent(long a,long n) { return n==0?"Không áp dụng (NOT_APPLICABLE)":String.format(Locale.ROOT,"%.4f%%",100.0*a/n); }
    static boolean matches(String text,String q) { return text.toLowerCase(Locale.ROOT).contains(q.toLowerCase(Locale.ROOT)); }
    static <T> Page<T> page(List<T> values,int index) {
        int pages=Math.max(1,(values.size()+PAGE_SIZE-1)/PAGE_SIZE);
        if(index>=pages) throw new Input("Trang vượt phạm vi kết quả. Chọn lại bộ lọc từ trang đầu.");
        return new Page<>(values.subList(index*PAGE_SIZE,Math.min(values.size(),(index+1)*PAGE_SIZE)),index,pages,values.size());
    }
    static String scalar(MultiValueMap<String,String> p,String key,String fallback) {
        List<String> values=p.get(key); if(values==null) return fallback;
        if(values.size()!=1) throw new Input("Tham số "+key+" phải là một giá trị.");
        return values.get(0);
    }
    static int integer(MultiValueMap<String,String> p,String field,int fallback,int max) { return Math.toIntExact(integer(p,field,(long)fallback,max)); }
    static long integer(MultiValueMap<String,String> p,String field,long fallback,long max) {
        String text=scalar(p,field,Long.toString(fallback));
        try { if(!text.matches("[0-9]{1,19}")) throw new NumberFormatException(); long value=Long.parseLong(text); if(value>max) throw new NumberFormatException(); return value; }
        catch(NumberFormatException e) { throw new Input("Tham số "+field+" phải là số nguyên trong phạm vi cho phép."); }
    }
    static double decimal(MultiValueMap<String,String> p,String field) {
        String text=scalar(p,field,"0");
        try { if(text.length()>30) throw new NumberFormatException(); double value=Double.parseDouble(text);
            if(!Double.isFinite(value) || value<0 || value>1) throw new NumberFormatException(); return value; }
        catch(NumberFormatException e) { throw new Input("Support tối thiểu phải là số từ 0 đến 1."); }
    }
}
