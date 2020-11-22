const lifts = ['Deadlift', 'Overhead Press', 'Squat', 
    'Bent Over Row', 'Bench Press'];
const lifsp = lifts.map(l => l.split(' ').join('+').toLowerCase());

const selector = document.querySelector('.lselect');

const weight = document.querySelector('#mass');

for (var i=0; i < lifts.length; i++) {
    var opt = document.createElement("option");
    opt.textContent = lifts[i];
    opt.value = lifsp[i];
    selector.appendChild(opt);
};

document.querySelector('form button').addEventListener("click", (e) => {
    const params = {act: 'change', lift: selector.value, value: weight.value};
    var query = "https://4twbzcqm75.execute-api.eu-west-2.amazonaws.com/Prod/skip/?";
    Object.keys(params).forEach(key => query += `${key}=${params[key]}&`);
    query = query.slice(0, -1);
    window.location.replace(query);
});