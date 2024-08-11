document.addEventListener('DOMContentLoaded', (event) => {
    import('https://cdn.jsdelivr.net/npm/chart.js').then(() => {
        const ctx = document.getElementById('my-chart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Water Level',
                    data: [],
                    borderColor: 'blue',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'category',
                        title: {
                            display: true,
                            text: 'Time (seconds may be inaccurate)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Water Level'
                        },
                        suggestedMin: 0,
                        suggestedMax: 30
                    }
                }
            }
        });

        async function fetchData() {
            try {
                const response = await fetch('/data');
                const newData = await response.json();

                const connection = newData.connection
                const elementConnectionState = document.getElementById('server-connection').children[0]
                if (connection == "OK") {
                    if (elementConnectionState.innerText != "CONNECTED") {
                        elementConnectionState.innerText = "CONNECTED"
                        elementConnectionState.style.color = "green"
                    }
                } else if (elementConnectionState.innerText != "DISCONNECTED") {
                    elementConnectionState.innerText = "DISCONNECTED"
                    elementConnectionState.style.color = "red"
                }

                const new_state = newData.state
                const new_valve_level = newData.valve_level
                const new_water_levels = newData.water_levels
                const new_water_times = newData.water_times
                const new_modality = newData.modality
                const new_busy = newData.busy

                const elementStatus = document.getElementById('system-status').children[0]
                if (elementStatus.innerText != new_state) {
                    elementStatus.innerText = new_state;
                }
                const elementValveLevel = document.getElementById('valve-level').children[0]
                if (elementValveLevel.innerText != `${new_valve_level} %`) {
                    elementValveLevel.innerText = `${new_valve_level} %`;
                }
                const currentModeLabel = document.getElementById('system-modality').children[0]
                const manualForm = document.getElementById('manual-form')
                if (currentModeLabel.innerText != new_modality) {
                    if (currentModeLabel.innerText === 'AUTOMATIC') {
                        currentModeLabel.innerText = 'MANUAL'
                        manualForm.style.display = 'block'
                    } else {
                        currentModeLabel.innerText = 'AUTOMATIC'
                        manualForm.style.display = 'none'
                    }
                }
                const elementServerBusy = document.getElementById('busy').children[0]
                if (elementServerBusy.innerText != new_busy) {
                    elementServerBusy.innerText = new_busy;
                }

                // if (myChart.data.datasets[0].data.toString() !== new_water_levels.toString()) {
                const dataPoints = new_water_times.map((x, index) => ({ x: x, y: new_water_levels[index] }));
                myChart.options.scales.x.labels = new_water_times
                myChart.data.labels = dataPoints.map((_, index) => index);
                myChart.data.datasets[0].data = dataPoints;
                myChart.update();
                // }

                document.getElementById('my-chart-title').innerText = `Water Level Trend (Last ${new_water_times.length} data)`
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        fetchData()
        setInterval(fetchData, 2500);
    })
});
