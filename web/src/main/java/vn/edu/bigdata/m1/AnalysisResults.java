package vn.edu.bigdata.m1;

import com.mongodb.client.model.Filters;
import org.bson.Document;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

/** Reads immutable batch outputs. Exactly one active pointer read per request; no cache. */
@Service
@ConditionalOnProperty(name = "app.mode", havingValue = "DEVELOPMENT")
public class AnalysisResults {
    static final String SCHEMA = "m0-contract-v1";
    static final String RANKING = "confidence-lift-support-codepoint-v1";
    public static class Unavailable extends RuntimeException {
        Unavailable(String message) { super(message); }
    }
    public record Item(String code, String name, long baskets) {}
    public record Itemset(List<String> codes, long frequency, double support, String key) {}
    public record Month(String month, long invoices, BigDecimal amount) {
        public String gbp() { return money(amount); }
    }
    public record Size(int size, long baskets) {}
    public record Popular(String code, long baskets, long quantity) {}
    public record Snapshot(String runId, long version, String basketSet, String source, String policy,
                           int k, long trainCount, List<Item> items, List<Itemset> itemsets,
                           List<RuleRanking.Rule> rules, List<Month> months, List<Size> sizes,
                           List<Popular> popular, Document quality, Document manifest, BigDecimal amount) {
        public String gbp() { return money(amount); }
        public String name(String code) {
            return items.stream().filter(i -> i.code().equals(code)).map(Item::name).findFirst().orElse(code);
        }
        public String describe(Collection<String> codes) {
            return String.join(" + ", codes.stream().map(c -> c + " — " + name(c)).toList());
        }
        public long stage(String field) { return count(doc(manifest, "stage_counts"), field); }
        public long trainItems() { return items.size(); }
        public String qualityLabel(String key) {
            return switch(key) {
                case "missing_invoice" -> "Thiếu Invoice"; case "missing_stock" -> "Thiếu StockCode";
                case "invalid_date" -> "Ngày không hợp lệ"; case "invalid_quantity" -> "Quantity sai kiểu / miền";
                case "invalid_price" -> "Price sai kiểu / miền"; case "cancelled" -> "Invoice có tiền tố hủy C";
                case "quantity_nonpositive" -> "Quantity không dương"; case "price_nonpositive" -> "Price không dương";
                case "missing_customer" -> "Thiếu Customer ID"; default -> key;
            };
        }
    }
    private final MongoTemplate mongo;
    AnalysisResults(MongoTemplate mongo) { this.mongo = mongo; }

    Snapshot snapshot() {
        Document pointer = mongo.getCollection("publication").find(Filters.eq("_id", "active")).first();
        require(pointer != null, "Chưa có lượt dữ liệu được công bố.");
        require(SCHEMA.equals(pointer.getString("schema_version")), "Schema chưa được hỗ trợ.");
        Document run = mongo.getCollection("runs").find(Filters.eq("_id", pointer.getString("run_id"))).first();
        require(run != null, "Thiếu manifest của lượt công bố.");
        Document manifest = doc(run, "manifest");
        Document preprocessing = mongo.getCollection("runs").find(Filters.eq("_id", manifest.getString("preprocessing_run_id"))).first();
        Document dataset = mongo.getCollection("datasets").find(Filters.eq("_id", run.getString("dataset_id"))).first();
        String id = pointer.getString("run_id"), basket = pointer.getString("basket_set_id");
        return assemble(pointer, run, preprocessing, dataset, rows("items", "run_id", id),
            rows("frequent_itemsets", "run_id", id), rows("association_rules", "run_id", id),
            rows("summaries", "basket_set_id", basket));
    }

    private List<Document> rows(String collection, String field, String value) {
        return mongo.getCollection(collection).find(Filters.eq(field, value)).into(new ArrayList<>());
    }

    static Snapshot assemble(Document p, Document run, Document pre, Document dataset,
                             List<Document> catalog, List<Document> sets, List<Document> rows, List<Document> summaries) {
        try {
            require(p != null && SCHEMA.equals(p.getString("schema_version")), "Schema chưa được hỗ trợ.");
            String id = p.getString("run_id"), basket = p.getString("basket_set_id");
            require(count(p, "version") > 0 && id != null && basket != null, "Con trỏ công bố không hợp lệ.");
            require(run != null && id.equals(run.getString("_id")) && "READY".equals(run.getString("status"))
                && "FULL_SOURCE".equals(run.getString("mode")) && "MODEL_DEVELOPMENT".equals(run.getString("stage"))
                && "DEVELOPMENT".equals(run.getString("evaluation_stage")) && SCHEMA.equals(run.getString("schema_version"))
                && basket.equals(run.getString("basket_set_id")) && RANKING.equals(run.getString("ranking_version")),
                "Lượt DEVELOPMENT chưa hoàn chỉnh hoặc không được hỗ trợ.");
            Document m = doc(run, "manifest"), config = doc(run, "config"), protocol = doc(m, "protocol");
            require("PASS".equals(m.getString("status")) && id.equals(m.getString("run_id"))
                && "DEVELOPMENT".equals(m.getString("evaluation_stage")) && "NOT_RUN".equals(m.getString("final_status"))
                && SCHEMA.equals(m.getString("schema_version")) && config.equals(doc(m, "config"))
                && run.getString("dataset_id").equals(m.getString("dataset_id"))
                && basket.equals(m.getString("basket_set_id")) && RANKING.equals(protocol.getString("ranking_version"))
                && "m3-temporal-hide-one-v1".equals(protocol.getString("version"))
                && count(config,"k") == count(protocol,"k") && count(config,"k") > 0,
                "Manifest/config của lượt dữ liệu không khớp.");
            require(pre != null && "VALIDATED".equals(pre.getString("status"))
                && "PREPROCESSING".equals(pre.getString("stage")) && "READY".equals(pre.getString("basket_set_status"))
                && basket.equals(pre.getString("basket_set_id")) && SCHEMA.equals(pre.getString("schema_version"))
                && run.getString("dataset_id").equals(pre.getString("dataset_id"))
                && run.getString("policy_hash").equals(doc(pre,"manifest").getString("policy_hash"))
                && dataset != null && "READY".equals(dataset.getString("status")), "Nguồn hoặc bộ giỏ chưa sẵn sàng.");
            Document pm = doc(pre,"manifest"), counts = doc(m,"counts"), stage = doc(m,"stage_counts");
            require(stage.equals(doc(pm,"counts")) && "PASS".equals(pm.getString("status")), "Mẫu số tiền xử lý không khớp.");
            Document validation = doc(m,"output_validation");
            checkOutput(validation,"items",catalog,id); checkOutput(validation,"frequent_itemsets",sets,id);
            checkOutput(validation,"association_rules",rows,id);
            require(catalog.size() == count(counts,"train_items") && sets.size() == count(counts,"itemsets")
                && rows.size() == count(counts,"rules"), "Số output không khớp manifest.");
            long train = count(counts,"train_baskets");
            require(train > 0 && train == count(doc(doc(m,"split"),"train"),"baskets"), "Mẫu số train không hợp lệ.");
            List<Item> items = catalog.stream().map(d -> new Item(text(d,"stock_code"),text(d,"display_name"),count(d,"train_basket_count")))
                .sorted(Comparator.comparing(Item::code,RuleRanking::codePointOrder)).toList();
            Set<String> known = new HashSet<>(items.stream().map(Item::code).toList());
            require(known.size() == items.size() && items.stream().allMatch(i -> i.baskets()>0 && i.baskets()<=train), "Danh mục train không hợp lệ.");
            List<Itemset> itemsets = sets.stream().map(d -> {
                List<String> codes = codes(d,"items"); long frequency = count(d,"frequency"); double support = number(d,"support");
                require(known.containsAll(codes) && count(d,"train_basket_count")==train && frequency>0 && frequency<=train
                    && Double.compare(support,frequency/(double)train)==0, "Tập phổ biến không hợp lệ.");
                return new Itemset(codes,frequency,support,text(d,"itemset_key"));
            }).toList();
            require(itemsets.stream().map(Itemset::key).distinct().count()==sets.size(), "Khóa tập phổ biến trùng.");
            List<RuleRanking.Rule> rules = rows.stream().map(d -> {
                List<String> a = codes(d,"antecedent"); String c = text(d,"consequent");
                require(known.containsAll(a) && known.contains(c), "Luật tham chiếu ngoài catalog train.");
                return new RuleRanking.Rule(a,c,number(d,"support"),number(d,"confidence"),number(d,"lift"));
            }).sorted(RuleRanking.ORDER).toList();
            require(rows.stream().map(d -> text(d,"rule_key")).distinct().count()==rows.size(), "Khóa luật trùng.");
            require(summaries.size()==count(stage,"summaries"), "Thiếu thống kê toàn kỳ.");
            Set<String> summaryKeys = new HashSet<>();
            List<Month> months = new ArrayList<>(); List<Size> sizes = new ArrayList<>(); List<Popular> popular = new ArrayList<>();
            Document quality = null;
            for (Document s : summaries) {
                require(basket.equals(s.getString("basket_set_id")) && run.getString("policy_hash").equals(s.getString("policy_hash")), "Thống kê khác nguồn/chính sách.");
                String scope = text(s,"scope"), kind = text(s,"summary_type"), key = text(s,"bucket_key");
                require(summaryKeys.add(scope+"\n"+kind+"\n"+key), "Thống kê trùng khóa.");
                Document value = doc(s,"payload");
                if (scope.equals("raw") && kind.equals("quality") && key.equals("all")) { quality=value; continue; }
                require(scope.equals("merchandise") && count(s,"denominator_baskets")==count(stage,"baskets"), "Scope/mẫu số thống kê không khớp.");
                switch (kind) {
                    case "month" -> months.add(new Month(key,count(value,"invoices"),new BigDecimal(text(value,"line_value_gbp"))));
                    case "basket_size" -> sizes.add(new Size(Integer.parseInt(key),count(value,"baskets")));
                    case "item" -> popular.add(new Popular(key,count(value,"baskets"),count(value,"quantity")));
                    default -> throw new Unavailable("Loại thống kê chưa được hỗ trợ.");
                }
            }
            require(quality!=null, "Thiếu audit chất lượng.");
            // M2 writes the quality payload before adding output counts to its final manifest.
            // Compare the eight source-stage fields; basket/item counts come from the final manifest.
            for(String field:List.of("raw","duplicates","retained","invalid_or_nonpositive","positive_valid","excluded","merchandise","merchandise_missing_customer"))
                require(count(doc(quality,"stage_counts"),field)==count(stage,field), "Counts chất lượng không khớp tiền xử lý.");
            require(popular.size()==count(stage,"items") && months.stream().mapToLong(Month::invoices).sum()==count(stage,"baskets")
                && sizes.stream().mapToLong(Size::baskets).sum()==count(stage,"baskets"), "Thống kê/mẫu số toàn kỳ không đầy đủ.");
            BigDecimal amount = months.stream().map(Month::amount).reduce(BigDecimal.ZERO,BigDecimal::add);
            require(amount.compareTo(new BigDecimal(text(pm,"merchandise_value_gbp")))==0, "Tổng GBP không khớp tiền xử lý.");
            Document development = doc(m,"development");
            for (String method : List.of("rules","baseline")) {
                Document metric = doc(doc(development,"all"),method); long n = count(metric,"queries");
                require(n==count(counts,"eligible_dev_queries") && count(metric,"hits")<=n && count(metric,"with_recommendations")<=n
                    && (n==0 ? "NOT_APPLICABLE" : "MEASURED").equals(metric.getString("status")), "Thiếu kết quả DEVELOPMENT đúng mẫu số.");
                if(n>0) require(Double.compare(number(metric,"recall_at_k"),count(metric,"hits")/(double)n)==0
                    && Double.compare(number(metric,"recommendation_rate"),count(metric,"with_recommendations")/(double)n)==0, "Metric không khớp tử số/mẫu số.");
            }
            months.sort(Comparator.comparing(Month::month)); sizes.sort(Comparator.comparingInt(Size::size));
            return new Snapshot(id,count(p,"version"),basket,run.getString("dataset_id"),run.getString("policy_version"),
                Math.toIntExact(count(config,"k")),train,items,itemsets,rules,List.copyOf(months),List.copyOf(sizes),
                List.copyOf(popular),quality,m,amount);
        } catch (Unavailable e) { throw e; }
        catch (RuntimeException e) { throw new Unavailable("Dữ liệu hoặc manifest thiếu/sai kiểu; chưa thể hiển thị lượt này."); }
    }

    private static void checkOutput(Document validation, String name, List<Document> rows, String id) {
        Document v = doc(validation,name);
        require(count(v,"expected")==rows.size() && count(v,"actual")==rows.size()
            && rows.stream().allMatch(d -> id.equals(d.getString("run_id")))
            && rows.stream().map(d -> text(d,"_id")).distinct().count()==rows.size(), "Output thiếu hoặc khác run: "+name);
        require(text(v,"checksum").matches("[a-f0-9]{64}"), "Thiếu checksum output.");
    }
    static void require(boolean ok, String message) { if(!ok) throw new Unavailable(message); }
    static Document doc(Document d, String field) { require(d!=null && d.get(field) instanceof Document,"Thiếu manifest/thống kê bắt buộc."); return d.get(field,Document.class); }
    static long count(Document d, String field) { require(d.get(field) instanceof Long && (Long)d.get(field)>=0,"Count cần BSON Long không âm."); return d.getLong(field); }
    static String text(Document d, String field) { require(d.get(field) instanceof String && !d.getString(field).isBlank(),"Thiếu trường chuỗi bắt buộc."); return d.getString(field); }
    static double number(Document d, String field) { require(d.get(field) instanceof Number && Double.isFinite(((Number)d.get(field)).doubleValue()),"Metric sai kiểu."); return ((Number)d.get(field)).doubleValue(); }
    static List<String> codes(Document d, String field) {
        List<String> values = d.getList(field,String.class);
        require(values!=null && !values.isEmpty() && values.equals(values.stream().distinct().sorted(RuleRanking::codePointOrder).toList()), "Mảng item chưa canonical.");
        return values;
    }
    public static String money(BigDecimal value) { return value.setScale(2,RoundingMode.HALF_UP).toPlainString(); }
}
