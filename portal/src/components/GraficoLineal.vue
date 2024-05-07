<template>
  <div class="row mt-3 d-flex justify-content-center">
    <div class="col-8 col-md-6">
      <div class="card border border-dark">
        <div class="card-header bg-dark"></div>
        <div class="card-body">
          <Line id="my-chart-id" :options="chartOptions" :data="chartData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import * as api from '../methods/api'
import { ref } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const chartData = ref({
  labels: [],
  datasets: [
    {
      data: [],
      backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)'],
      hoverOffset: 10
    }
  ]
})

async function fetchJson(url) {
  const resp = await fetch(url)
  return await resp.json()
}

fetchJson(`${api.apiURL}/stats/Barra`).then(data => {
  const dic_mes_cant = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
  };
  const sortedData = Object.entries(data)
    .sort((a, b) => Object.keys(dic_mes_cant).indexOf(a[0]) - Object.keys(dic_mes_cant).indexOf(b[0]));

  const cdata = sortedData.map(([key, value]) => value);

  chartData.value = {
    labels: Object.values(dic_mes_cant), // Usar los nombres de los meses en español como etiquetas
    datasets: [{
      label: "usuarios por mes",
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
</script>
