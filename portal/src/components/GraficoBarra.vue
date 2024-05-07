<template>
    <div class="row mt-3 d-flex justify-content-center">
        <div class="col-8 col-md-6">
            <div class="card border border-dark">
                <div class="card-header bg-dark"></div>
                <div class="card-body">
                    <Bar id="my-chart-id" :options="chartOptions" :data="chartData"/>
                </div>
            </div>
        </div>
    </div>
</template>


      
<script setup>
import * as api from "../methods/api";
import { ref } from "vue"
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, BarController)

const chartData = ref({
    datasets: [{
        data: [],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
        ],
        hoverOffset: 10

    }]
});

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

async function fetchJson(url) {
    const resp = await fetch(url)
    return await resp.json()
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
            label: "tipos de servicio",
            data: cdata,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 10

        }]
    }
})

</script>
    
