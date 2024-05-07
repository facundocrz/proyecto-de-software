<script setup>
import { ref } from 'vue'
import auth from '../methods/auth.js'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as Yup from 'yup'

const schema = Yup.object().shape({
  user: Yup.string()
    .required('El email o nombre de usuario es requerido')
    .test('no-blank-spaces', 'No se permiten solo espacios en blanco', (value) => {
      return value.trim().length > 0
    }),
  password: Yup.string()
    .required('La contraseña es requerida')
    .test('no-blank-spaces', 'No se permiten solo espacios en blanco', (value) => {
      return value.trim().length > 0
    })
})

const error = ref('')

const onSubmit = async (values) => {
  const { user, password } = values;
  const removedSpaces = {
    user: user.trim(),
    password: password.trim()
  };
  try {
    let result = await auth.login(removedSpaces.user, removedSpaces.password);
    if (result.error) {
      console.error('Error en el inicio de sesión:', result.error);
      error.value = result.error;
    }
  } catch (err) {
    console.error('Error inesperado:', err);
    error.value = 'Error inesperado al iniciar sesión.';
  }
};

const goToRegister = () => {
  window.location.href = 'https://admin-grupo12.proyecto2023.linti.unlp.edu.ar/user/register'
}
</script>

<template>
  <div class="container mt-5">
    <div class="card p-4">
      <h2 class="mb-4 text-center">Inicio de sesión</h2>
      
      <Form @submit="onSubmit" :validation-schema="schema">
        <div class="mb-3 text-danger">
          {{ error }}
        </div>
        <div class="mb-3">
          <label for="user" class="form-label">Email o nombre de usuario</label>
          <Field name="user" class="form-control" />
          <ErrorMessage name="user" class="text-danger" />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <Field type="password" name="password" class="form-control" />
          <ErrorMessage name="password" class="text-danger" />
        </div>

        <div class="mb-3">
          <button type="submit" class="btn btn-primary">Iniciar sesión</button>
          <button type="button" @click="goToRegister" class="btn btn-link">Registrarse</button>
        </div>
      </Form>
    </div>
  </div>
</template>

<style>
form {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
