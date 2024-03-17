document.addEventListener("DOMContentLoaded", function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var datosElement = document.getElementById('datos');
    var datos = JSON.parse(datosElement.dataset.datos);

    var fechas = Object.keys(datos).map(function(key) {
        return datos[key].fecha_hora;
    });

    // Crear el gráfico inicial con los valores predeterminados
    var myChart = crearGrafico(ctx, fechas, datos, 'last_value1', 'MQ-135');

    // Escuchar cambios en el select y actualizar el gráfico
    document.getElementById('selectDato').addEventListener('change', function() {
        var selectedValue = this.value;
        var label = obtenerEtiqueta(selectedValue);
        // Filtrar los valores correspondientes al dato seleccionado
        var valoresSeleccionados = Object.keys(datos).map(function(key) {
            return datos[key][selectedValue];
        });
        // Actualizar el gráfico con los nuevos valores seleccionados y la etiqueta correcta
        actualizarGrafico(myChart, fechas, valoresSeleccionados, label);
    });
    document.getElementById('generatePdf').addEventListener('click', function() {
        generarPDF();
    });
});

function crearGrafico(ctx, fechas, valores, valorInicial, labelInicial) {
    var valoresSeleccionados = Object.keys(valores).map(function(key) {
        return valores[key][valorInicial];
    });

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: fechas,
            datasets: [{
                label: labelInicial, // Utiliza la etiqueta inicial
                data: valoresSeleccionados,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function actualizarGrafico(chart, fechas, nuevosValores, label) {
    chart.data.labels = fechas;
    chart.data.datasets[0].data = nuevosValores;
    chart.data.datasets[0].label = label; // Actualiza la etiqueta del dataset
    chart.update();
}

function obtenerEtiqueta(selectedValue) {
    switch (selectedValue) {
        case 'last_value1':
            return 'MQ-135';
        case 'last_value2':
        case 'last_value3':
            return 'DHT11';
        case 'last_value4':
            return 'MQ-2';
        default:
            return 'Desconocido';
    }
}

function generarPDF() {
    // Selecciona el canvas del gráfico
    var canvas = document.getElementById('myChart');

    // Crea un nuevo objeto jsPDF
    var pdf = new jsPDF();

    // Obtiene el contexto del canvas
    var ctx = canvas.getContext('2d');

    // Convierte el canvas en una imagen base64
    var imgData = canvas.toDataURL('image/png');

    // Agrega la imagen al PDF
    pdf.addImage(imgData, 'PNG', 10, 10, 180, 100); // Ajusta las coordenadas y el tamaño según sea necesario

    // Guarda el PDF
    pdf.save('grafico.pdf');
}

