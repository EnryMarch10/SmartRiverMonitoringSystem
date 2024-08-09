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
                            text: 'Time (seconds could not be accurate)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Water Level'
                        }
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
                } else if (elementConnectionState.innerText != "DISCONNECTED") { // connection == "ERROR"
                    elementConnectionState.innerText = "DISCONNECTED"
                    elementConnectionState.style.color = "red"
                }

                const new_state = newData.state
                const new_valve_level = newData.valve_level
                const new_water_levels = newData.water_levels
                const new_water_times = newData.water_times

                const elementStatus = document.getElementById('system-status').children[0]
                if (elementStatus.innerText != new_state) {
                    elementStatus.innerText = new_state;
                }
                const elementWaterLevel = document.getElementById('valve-level').children[0]
                if (elementWaterLevel.innerText != `${new_valve_level} %`) {
                    elementWaterLevel.innerText = `${new_valve_level} %`;
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

        // TODO: understand if this is called in an async way
        fetchData()
        setInterval(fetchData, 2500);  // Fetch new data every 5 seconds
    })
});
