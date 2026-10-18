"use strict";
const search = document.getElementById("catalog-search");
if (search) {
  const labels = [...document.querySelectorAll("#catalog label")];
  const count = document.getElementById("selection-count");
  const selected = document.getElementById("show-selected");
  const clear = document.getElementById("clear-selected");
  let onlySelected = false;
  const filter = () => {
    const q = search.value.toLocaleLowerCase("en");
    let chosen = 0, visible = 0;
    labels.forEach(label => {
      const checked = label.querySelector("input").checked;
      chosen += checked ? 1 : 0;
      const show = onlySelected ? checked : label.textContent.toLocaleLowerCase("en").includes(q);
      label.hidden = !show;
      visible += show ? 1 : 0;
    });
    count.textContent = `${chosen} mã đã chọn · ${visible} / ${labels.length} mã đang hiển thị`;
    selected.textContent = onlySelected ? "Xem danh mục" : "Chỉ xem lựa chọn";
  };
  selected.hidden = false; clear.hidden = false;
  search.addEventListener("input", filter);
  document.getElementById("catalog").addEventListener("change", filter);
  selected.addEventListener("click", () => { onlySelected = !onlySelected; filter(); });
  clear.addEventListener("click", () => { labels.forEach(l => { l.querySelector("input").checked = false; }); filter(); });
  filter();
}
