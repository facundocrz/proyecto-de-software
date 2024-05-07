<script setup>
import { useRoute } from 'vue-router'
import { reactive, onMounted } from 'vue'
import api from '@/methods/api.js'
import auth from '@/methods/auth.js'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as Yup from 'yup'

const schema = Yup.object().shape({
  text: Yup.string()
    .required('El comentario es requerido')
    .test('no-blank-spaces', 'No se permiten solo espacios en blanco', (value) => {
      return value.trim().length > 0
    })
    .min(10, 'El comentario debe tener al menos 10 caracteres')
    .test('contains-letter', 'El comentario debe contener al menos una letra', (value) => {
      return /[a-zA-Z]/.test(value)
    })
})

const route = useRoute()
const id = route.params.id

const request = reactive({
  comments: [],
  created_at: '',
  current_status: '',
  description: '',
  status_changes: [],
  title: '',
  updated_at: '',
  service: {
    title: ''
  },
  institution: ''
})

const getRequest = async () => {
  try {
    const response = await api.request(auth.getToken(), id)
    request.comments = response.comments
    request.created_at = response.created_at
    request.current_status = response.current_status
    request.description = response.description
    request.status_changes = response.status_changes
    request.title = response.title
    request.updated_at = response.updated_at
    request.service.title = response.service.title
    request.institution = response.institution
  } catch (error) {
    console.error('Error obteniendo la solicitud:', error)
  }
}

const onSubmit = async (values, { resetForm }) => {
  const { text } = values
  const removedSpaces = text.trim()
  try {
    let result = await api.commentRequest(auth.getToken(), id, removedSpaces)
    if (result.error) {
      console.error('Error agregando el comentario:', result.error)
    } else {
      getRequest()
      resetForm()
    }
  } catch (error) {
    console.error('Error agregando el comentario:', error)
  }
}

const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()} ${d.getHours()}:${d.getMinutes()}`
}

onMounted(getRequest)
</script>

<template>
  <div v-if="request" class="container mt-4">
    <h1 class="mb-4">Solicitud #{{ id }}</h1>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">{{ request.title }}</h5>
        <p class="card-text">{{ request.description }}</p>
        <p class="card.text">
          Perteneciente al servicio: {{ request.service.title }} de la institución: {{ request.institution }}
        </p>
        <p class="card-text">
          Estado Actual: <strong>{{ request.current_status }}</strong>
        </p>
      </div>
      <div class="card-footer text-muted">Creada el: {{ formatDate(request.created_at) }}</div>
    </div>
    <div v-if="request.status_changes.length !== 0" class="card mb-4">
      <div class="card-header">Historial de Cambios de Estado</div>
      <ul class="list-group list-group-flush">
        <li
          class="list-group-item d-flex"
          v-for="change in request.status_changes"
          :key="change.id"
        >
          <strong>{{ change.status.name }}</strong> - {{ formatDate(change.created_at) }}
          <blank class="ms-3">
            usuario: {{ change.user.username }}
          </blank>
          <blank v-if="change.observation" class="ms-3">
            Observación: {{ change.observation }}</blank
          >
        </li>
      </ul>
    </div>
    <div class="card mb-4">
      <div class="card-header">Comentarios</div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="comment in request.comments" :key="comment.id">
          {{ comment.username }}: {{ comment.content }} - {{ formatDate(comment.created_at) }}
        </li>
      </ul>
      <div class="card-body">
        <Form @submit="onSubmit" :validation-schema="schema">
          <div class="mb-3">
            <label for="text" class="form-label">Agregar comentario</label>
            <Field name="text" class="form-control" />
            <ErrorMessage name="text" class="text-danger" />
          </div>
          <button type="submit" class="btn btn-primary">Agregar</button>
        </Form>
      </div>
    </div>
  </div>
</template>
