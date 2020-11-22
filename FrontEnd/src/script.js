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
    var query = "https://df25skxur7.execute-api.eu-west-2.amazonaws.com/Prod/?";
    Object.keys(params).forEach(key => query += `${key}=${params[key]}&`);
    window.location.replace(query.slice(0, -1));
});