const lifts = [
  "Deadlift",
  "Overhead Press",
  "Squat",
  "Bent Over Row",
  "Bench Press",
];
const lifsp = lifts.map((l) => l.split(" ").join("+").toLowerCase());

const selector = document.querySelector(".lselect");

const weight = document.querySelector("#mass");

for (var i = 0; i < lifts.length; i++) {
  var opt = document.createElement("option");
  opt.textContent = lifts[i];
  opt.value = lifsp[i];
  selector.appendChild(opt);
}

var query = "https://liftapi.kaizadwadia.com/?";

document.querySelector("form button").addEventListener("click", async (e) => {
  const params = { act: "change", lift: selector.value, value: weight.value };
  Object.keys(params).forEach((key) => (query += `${key}=${params[key]}&`));
  fetch(query.slice(0, -1)).then(response => {
    return response.text()
  })
  .then((data) => {
    document.querySelector('div.body').innerHTML = data;
    document.querySelector('.back').style.visibility = 'visible';
  });
});

const skipbtn = e => {
    console.log('yes');
    const param = 'act=' + e.target.value;
    query += param;
    fetch(query).then(response => {
        return response.text()
        })
        .then((data) => {
        document.querySelector('div.body').innerHTML = data;
        document.querySelector('.back').style.visibility = 'visible';
        });
}