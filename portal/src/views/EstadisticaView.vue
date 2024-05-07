<script setup>
    import GraficoPizza from "../components/GraficoPizza.vue"
    import GraficoLineal from "../components/GraficoLineal.vue"
    import GraficoBarra from "../components/GraficoBarra.vue"
</script>

<template>
  <h2>Grafico de solicitudes Agrupado por estados</h2>
  <GraficoPizza></GraficoPizza>
  <br>
  <hr>
  <h2>Grafico de Usuarios registrados por mes </h2>
  <GraficoLineal></GraficoLineal>
  <!-- <hr> -->
  <br>
  <hr>
  <h2>Grafico de Tipos de Servicios mas solicitados</h2>
  <GraficoBarra></GraficoBarra>
  <!-- <hr> -->
  <br>
</template>

