<script setup>
import api from '@/methods/api.js'
import auth from '@/methods/auth.js'
import { reactive, onMounted } from 'vue'
import Pagination from '@/components/Pagination.vue'
import { RouterLink } from 'vue-router'

const requests = reactive({
  data: [],
  page: 1,
  per_page: null,
  total: 1,
  order: 'desc',
  sort: 'created_at',
  filter: 'All',
  startDate: null,
  endDate: null
})

const getRequests = async () => {
  try {
    const response = await api.requests(
      auth.getToken(),
      requests.page,
      requests.per_page,
      requests.order,
      requests.sort,
      requests.filter,
      requests.startDate,
      requests.endDate
    )
    requests.data = response.data
    requests.total = response.total
    requests.page = response.page
    requests.per_page = response.per_page

    const totalPages = calculateTotalPages(requests.total, requests.per_page)
    if (requests.page > totalPages) {
      requests.page = totalPages
      getRequests()
    }

  } catch (error) {
    console.error('Error obteniendo las solicitudes:', error)
  }
}

onMounted(getRequests)

const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()} ${d.getHours()}:${d.getMinutes()}`
}

const calculateTotalPages = (total, perPage) => {
  return Math.ceil(total / perPage)
}

const goToPage = (page) => {
  requests.page = page
  getRequests()
}

const prevPage = () => {
  if (requests.page > 1) {
    requests.page--
    getRequests()
  }
}

const nextPage = () => {
  const totalPages = calculateTotalPages(requests.total, requests.per_page)
  if (requests.page < totalPages) {
    requests.page++
    getRequests()
  }
}
</script>

<template>
  <div>
    <h1>Solicitudes</h1>
    <div>
      <div class="container me-4 d-flex flex-column justify-content-md-between">
        <div class="d-flex flex-column flex-md-row align-items-md-center">
          <label>Fecha Desde:</label>
          <input type="date" id="startDate" name="startDate" class="form-control" v-model="requests.startDate" @change="getRequests"/>
          <label>Fecha Hasta:</label>
          <input type="date" id="endDate" name="endDate" class="form-control" v-model="requests.endDate" @change="getRequests"/>
          <label for="filter">Filtrar:</label>
          <select class="form-select w-auto" v-model="requests.filter" @change="getRequests">
            <option value="All" selected>Todas</option>
            <option value="Creada">Creada</option>
            <option value="En proceso">En Proceso</option>
            <option value="Aceptada">Aceptada</option>
            <option value="Rechazada">Rechazada</option>
            <option value="Finalizada">Finalizada</option>
            <option value="Cancelada">Cancelada</option>
          </select>
        </div>
        <div class="d-flex flex-column flex-md-row mt-3">
          <div class="mb-3 me-3 d-flex align-items-center">
            <label for="sort" class="form-label">Ordenar por:</label>
            <select class="form-select w-auto" v-model="requests.sort" @change="getRequests">
              <option value="id">Número</option>
              <option value="title">Título</option>
              <option value="created_at" selected>Fecha de Creación</option>
              <option value="updated_at">Fecha de Actualización</option>
              <option value="current_status">Estado</option>
            </select>
          </div>
          <div class="mb-3 me-3 d-flex align-items-center">
            <label for="order" class="form-label">Orden:</label>
            <select class="form-select w-auto" v-model="requests.order" @change="getRequests">
              <option value="asc">Ascendente</option>
              <option value="desc">Descendente</option>
            </select>
          </div>
        </div>
      </div>
      <div v-if="requests.data.length > 0">
        <div v-for="request in requests.data" :key="request.id" class="card mb-3 requestCard">
        <h4 class="card-header">Solicitud #{{ request.id }}</h4>
        <div class="card-body">
          <h5 class="card-title">{{ request.title }}</h5>
          <p class="card-text"><strong>Descripción:</strong> {{ request.description }}</p>
          <p class="card-text"><strong>Estado actual:</strong> {{ request.current_status }}</p>
          <p class="card-text">
            <strong>Fecha de Creación:</strong> {{ formatDate(request.created_at) }}
          </p>
          <p class="card-text">
            <strong>Última Actualización:</strong> {{ formatDate(request.updated_at) }}
          </p>
          <RouterLink :to="`/solicitudes/${request.id}`">
            <button type="button" class="btn btn-primary">Ver Solicitud</button>
          </RouterLink>
        </div>
      </div>
      <pagination
        :currentPage="requests.page"
        :totalPage="calculateTotalPages(requests.total, requests.per_page)"
        :goToPage="goToPage"
        :prevPage="prevPage"
        :nextPage="nextPage"
      />

      </div>
      <div v-else><h2>No hay solicitudes para mostrar.</h2></div>
    </div>
  </div>
</template>

<style></style>
