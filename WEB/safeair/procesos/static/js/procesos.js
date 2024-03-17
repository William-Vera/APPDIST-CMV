$(document).ready(function () {
    var ctx1 = document.getElementById('chart1').getContext('2d');
    var chart1 = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Dispositivo Sala',
                data: [],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    min: 0,
                    max: 700
                }
            }
        }
    });

    var ctx2 = document.getElementById('chart2').getContext('2d');
    var chart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Humedad',
                data: [],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    min: 0,
                    max: 100
                }
            }
        }
    });

    var ctx3 = document.getElementById('chart3').getContext('2d');
    var chart3 = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperatura', // El label se actualizará con el valor en tiempo real más adelante
                data: [],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    min: 0,
                    max: 50
                }
            }
        }
    });

    var ctx4 = document.getElementById('chart4').getContext('2d');
    var chart4 = new Chart(ctx4, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Dispositivo cocina', // El label se actualizará con el valor en tiempo real más adelante
                data: [],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    min: 0,
                    max: 1000
                }
            }
        }
    });

    // var firebaseConfig = {
    //     apiKey: "AIzaSyAzpxs7qMAtNA-1wHNn84BaTwmf-19znPM",
    //     authDomain: "safeair-4fcf5.firebaseapp.com",
    //     databaseURL: "https://safeair-4fcf5-default-rtdb.firebaseio.com",
    //     projectId: "safeair-4fcf5",
    //     storageBucket: "safeair-4fcf5.appspot.com",
    //     messagingSenderId: "58180935832",
    //     appId: "1:58180935832:web:6ef107f572f6a9a29570ed"
    // };
    // firebase.initializeApp(firebaseConfig);
    // var database = firebase.database();


    // Actualizar los gráficos con los datos de las propiedades
    function actualizarGraficos() {
        $.ajax({
            url: '/actualizar_propiedades/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.error) {
                    console.error('Error al obtener los datos de las propiedades:', data.error);
                    return;
                }

                // database.ref('graficos').set({
                //     last_value1: data.last_value1,
                //     last_value2: data.last_value2,
                //     last_value3: data.last_value3,
                //     last_value4: data.last_value4,
                //     last_values2: data.last_values2
                // });

                // Actualizar datos del gráfico 1
                chart1.data.labels.push(new Date().toLocaleTimeString());
                chart1.data.datasets[0].data.push(data.last_value1);
                if (chart1.data.labels.length > 5) {
                    chart1.data.labels.shift();
                    chart1.data.datasets[0].data.shift();
                }
                chart1.update();

                // Actualizar datos del gráfico 2
                chart2.data.labels.push(new Date().toLocaleTimeString());
                chart2.data.datasets[0].data.push(data.last_value2);
                if (chart2.data.labels.length > 5) {
                    chart2.data.labels.shift();
                    chart2.data.datasets[0].data.shift();
                }
                chart2.update();

                // Actualizar datos del gráfico 3
                chart3.data.labels.push(new Date().toLocaleTimeString());
                chart3.data.datasets[0].data.push(data.last_value3);
                if (chart3.data.labels.length > 5) {
                    chart3.data.labels.shift();
                    chart3.data.datasets[0].data.shift();
                }

                chart4.data.labels.push(new Date().toLocaleTimeString());
                chart4.data.datasets[0].data.push(data.last_value4);
                if (chart4.data.labels.length > 5) {
                    chart4.data.labels.shift();
                    chart4.data.datasets[0].data.shift();
                }

                // Actualizar el label del dataset con el valor en tiempo real de la temperatura
                var temperaturaActual = data.last_value3;
                chart3.data.datasets[0].label = 'Temperatura: ' + temperaturaActual + '°C';
                chart3.update();

                var dispositivosala = data.last_value1;
                chart1.data.datasets[0].label = 'Dispositivo Sala: ' + dispositivosala;
                chart1.update();

                var Humedadact = data.last_value2;
                chart2.data.datasets[0].label = 'Humedad: ' + Humedadact + '%';
                chart2.update();

                var dispcocina = data.last_value4;
                chart4.data.datasets[0].label = 'Dispositivo Cocina: ' + dispcocina;
                chart4.update();

                actualizarVentanaAbierta(data.last_values2);
            },
            error: function (xhr, status, error) {
                console.error('Error en la solicitud AJAX:', error);
            }
        });
    }
    setInterval(actualizarGraficos, 5000);
    var interruptor = document.getElementById("interruptor");
    var ventanaTexto = document.getElementById("ventana-texto");

    // Cambiar el estado del interruptor según el valor recibido
    function actualizarEstadoInterruptor(valor) {
        interruptor.checked = valor;
        ventanaTexto.textContent = valor ? "Ventana Abierta" : "Ventana Cerrada";
    }

    // Esta función debe ser llamada cada vez que la variable booleana cambie
    function actualizarVentanaAbierta(ventanaAbierta) {
        // Actualizar el estado del interruptor
        actualizarEstadoInterruptor(ventanaAbierta);
    }
});
