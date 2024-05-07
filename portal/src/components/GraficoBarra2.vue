<template>
    <div class="row mt-3 d-flex justify-content-center">
        <div class="col-6">
            <div class="card border border-dark">
                <div class="card-header bg-dark"></div>
                <div class="card-body">
                    <!-- Renderiza el componente Bar solo si chartData tiene datos -->
                    <Bar v-if="chartData.datasets[0].data.length > 0" id="my-chart-id" :options="chartOptions"
                        :data="chartData" />
                    <!-- Agrega un mensaje o lógica adicional si no hay datos para mostrar -->
                    <p v-else>No hay datos para mostrar.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import * as api from "../methods/api";
import { ref } from "vue";
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController);

const chartData = ref({
    datasets: [{
        data: [],
        backgroundColor: [],
        hoverOffset: 10
    }]
});

async function fetchJson(url) {
    const resp = await fetch(url);
    return await resp.json();
}

fetchJson(`${api.apiURL}/stats/Barra2`).then(data => {
    let labels = [];
    let cdata = [];
    for (const [key, value] of Object.entries(data)) {
        labels.push(key);
        cdata.push(value);
    }
    chartData.value = {
        labels,
        datasets: [{
            data: cdata,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 10
        }]
    };
});

/** Esto hace que en el gráfico las unidades de medida vayan de a 1 y no en 0,5 */
const chartOptions = ref({
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                stepSize: 1,
            },
        },
    },
});
</script>
