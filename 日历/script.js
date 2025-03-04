const calendarBody = document.getElementById("calendar-body");
const currentMonthYear = document.getElementById("current-month-year");
const prevMonthButton = document.getElementById("prev-month");
const nextMonthButton = document.getElementById("next-month");
const clearAllButton = document.getElementById("clear-all");

const colorSums = {
  2: 0,
  3: 0,
  10: 0,
};

let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

function updateCalendar(month, year) {
    calendarBody.innerHTML = "";
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
  
    currentMonthYear.textContent = `${year}年${month + 1}月`;
  
    // 重置颜色总和
    colorSums[2] = 0;
    colorSums[3] = 0;
    colorSums[10] = 0;
  
    let rows = [];
    let row = [];
    for (let i = 1; i < firstDay; i++) {
      row.push("<td></td>");
    }
  
    for (let day = 1; day <= daysInMonth; day++) {
      const isToday = day === today.getDate() && month === today.getMonth() && year === today.getFullYear();
  
      row.push(`
        <td class="${isToday ? 'today' : ''}" onclick="showOptions(this, ${day})" data-date="${year}-${month + 1}-${day}">
          <div>${day}</div>
          <div class="options" style="display: none;">
            <select onchange="changeColor(this)">
              <option value="">选择颜色</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="10">10</option>
            </select>
          </div>
        </td>
      `);
  
      if (row.length === 7) {
        rows.push(`<tr>${row.join('')}</tr>`);
        row = [];
      }
    }
  
    if (row.length > 0) {
      while (row.length < 7) {
        row.push("<td></td>");
      }
      rows.push(`<tr>${row.join('')}</tr>`);
    }
  
    calendarBody.innerHTML = rows.join('');
  
    loadFromLocalStorage();
  }  

function showOptions(td) {
  const options = td.querySelector('.options');
  const allOptions = document.querySelectorAll('.options');
  
  allOptions.forEach(opt => {
    opt.style.display = 'none';
  });

  options.style.display = 'block';

  setTimeout(() => {
    options.style.display = 'none';
  }, 5000);
}

function changeColor(selectElement) {
  const td = selectElement.parentElement.parentElement;
  const selectedValue = selectElement.value;
  const date = td.getAttribute("data-date");

  // 清除旧颜色
  td.style.backgroundColor = "";
  const oldValue = td.getAttribute("data-value");
  if (oldValue) {
    colorSums[oldValue] -= parseInt(oldValue);
  }

  // 设置新颜色
  if (selectedValue) {
    td.style.backgroundColor = getColor(selectedValue);
    colorSums[selectedValue] += parseInt(selectedValue);
    td.setAttribute("data-value", selectedValue);
    saveToLocalStorage(date, selectedValue);
  } else {
    td.removeAttribute("data-value");
    removeFromLocalStorage(date);
  }

  updateColorSums();
}

function getColor(value) {
  switch (value) {
    case '2': return "#00ffff";
    case '3': return "#006400";
    case '10': return "#ffa500";
    default: return "";
  }
}

function updateColorSums() {
  document.getElementById("color-sum-2").textContent = colorSums[2];
  document.getElementById("color-sum-3").textContent = colorSums[3];
  document.getElementById("color-sum-10").textContent = colorSums[10];
}

function saveToLocalStorage(date, value) {
  const data = JSON.parse(localStorage.getItem("calendarData")) || {};
  data[date] = value;
  localStorage.setItem("calendarData", JSON.stringify(data));
}

function removeFromLocalStorage(date) {
  const data = JSON.parse(localStorage.getItem("calendarData")) || {};
  delete data[date];
  localStorage.setItem("calendarData", JSON.stringify(data));
}

function loadFromLocalStorage() {
  const data = JSON.parse(localStorage.getItem("calendarData")) || {};
  for (const date in data) {
    const value = data[date];
    const td = document.querySelector(`td[data-date="${date}"]`);
    if (td) {
      td.style.backgroundColor = getColor(value);
      td.setAttribute("data-value", value);
      colorSums[value] += parseInt(value);
    }
  }
  updateColorSums();
}

function clearAll() {
  localStorage.removeItem("calendarData");
  colorSums[2] = 0;
  colorSums[3] = 0;
  colorSums[10] = 0;
  updateColorSums();
  updateCalendar(currentMonth, currentYear);
}

prevMonthButton.addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  updateCalendar(currentMonth, currentYear);
});

nextMonthButton.addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  updateCalendar(currentMonth, currentYear);
});

function updateColorSums() {
  document.getElementById("color-sum-2").textContent = colorSums[2];
  document.getElementById("color-sum-3").textContent = colorSums[3];
  document.getElementById("color-sum-10").textContent = colorSums[10];
  updateTotalSalary();
}

function updateTotalSalary() {
  const baseSalary = 4600;
  const G1Rate = 39.65517;
  const G2Rate = 52.87356;

  const G1Days = colorSums[2] + colorSums[3]; // 青色和绿色为 G1
  const G2Days = colorSums[10]; // 橙色为 G2

  const totalSalary = baseSalary + (G1Days * G1Rate) + (G2Days * G2Rate);

  document.getElementById("total-salary").textContent = `总工资：${totalSalary.toFixed(2)} 元`;
};



clearAllButton.addEventListener("click", clearAll);

updateCalendar(currentMonth, currentYear);
