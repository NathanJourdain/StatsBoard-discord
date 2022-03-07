function getSimpleOptions(data, labelName){
    const labels = data.map(x => x[0]);
    const dataset = {
        labels: labels,
        datasets: [{
            label: labelName,
            backgroundColor: 'rgb(10, 105, 69)',
            borderColor: 'rgb(10, 105, 69)',
            data: data.map(x => x[1]),
        }]
    };
    return {
        type: 'bar',
        data: dataset,
        options: {}
      };
}
function getDoubleOptions(data, labelsNames){
    const labels = data.map(x => x[0]);
    const dataset = {
        labels: labels,
        datasets: [{
            label: labelsNames[0],
            backgroundColor: 'rgb(10, 105, 69)',
            borderColor: 'rgb(10, 105, 69)',
            data: data.map(x => x[1]),
        },
        {
            label: labelsNames[1],
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: data.map(x => x[2]),
        }]
    };
    return {
        type: 'bar',
        data: dataset,
        options: {}
      };
}




const charts = {
    'messages' : new Chart(
        document.querySelector('#messages'),
        getSimpleOptions(data.messages, "Messages")
    ),
    'trafic' : new Chart(
        document.querySelector('#trafic'),
        getDoubleOptions(data.trafic, ["New members", "Leaving members"])
    ),
    'reactions' : new Chart(
        document.querySelector('#reactions'),
        getDoubleOptions(data.reactions, ["Reactions add", "Reactions remove"])
    ),
    'invitations' : new Chart(
        document.querySelector('#invitations'),
        getSimpleOptions(data.invitations, "Invitations")
    )
}


document.querySelectorAll('button.change-chart-type').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const canvas = e.target.parentNode.querySelector('canvas');
        if(canvas != undefined && charts[canvas.id] != undefined){
            btn.textContent = "Change to " +  charts[canvas.id].config.type;
            charts[canvas.id].config.type = charts[canvas.id].config.type == 'line' ? 'bar' : 'line';
            charts[canvas.id].update();
        }
    })
})
