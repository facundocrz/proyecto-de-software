<script setup>
    import { ref } from "vue";
    import { useRoute } from "vue-router";
    import { ErrorMessage, Field, Form } from "vee-validate";
    import { object, string } from "yup";
    import * as api from "../methods/api.js";
    import auth from "../methods/auth.js";
    import { flash } from "../methods/alerts.js";
    import { router } from "../router";

    if (!auth.isAuthenticated())
    {
        flash("Por favor, inicie sesión para solicitar servicios.")
        router.push("/login")
    }

    const route = useRoute();
    const serviceId = route.params.id;

    const service = ref(null);

    function onServiceDataFetched(code, data) {
        if (code === 200) {
            service.value = data
        } else {
            flash("Hubo un error al obtener los datos del servicio. Por favor, vuelva a intentarlo.", "danger")
        }
    }

    function onServiceRequestCreated(code, data) {
        if (code === 201) {
            router.go(-1)
            flash("¡Se creó la solicitud de servicio exitosamente!", "success")
        } else {
            flash("Hubo un error al crear la solicitud de servicio. Por favor, vuelva a intentarlo.", "danger")
        }
    }

    api.fetchService(serviceId)
        .then(({ code, data }) => {
            onServiceDataFetched(code, data);
        })
        .catch(error => {
            onServiceDataFetched(null);
        });

    const formSchema = object({
        title: string().trim()
            .required("El campo no debe estar vacío")
            .max(63, "El campo debe tener menos de 64 carácteres")
            .matches("^[A-Za-z ]+$", "El campo solo puede contener letras y espacios."),
        description: string().trim()
            .required("El campo no debe estar vacío")
            .max(255, "El campo debe tener menos de 256 carácteres"),
    });

    function formSubmit(form) {
        api.createServiceRequest(serviceId, form)
            .then(({ code, data }) => {
                onServiceRequestCreated(code, data);
            })
            .catch(error => {
                onServiceRequestCreated(null);
            });
    }
</script>

<template>
    <template v-if="service">
        <!-- Title -->
        <h1>Solicitud de servicio</h1>
        <h3>{{ service.title }} - {{ service.institution_name }}</h3>
        <!-- Form -->
        <Form @submit="formSubmit" :validation-schema="formSchema">
            <div class="mb-3">
                <label class="form-label" for="title">Título (*):</label>
                <Field class="form-control" name="title"/>
                <ErrorMessage class="form-text text-danger" name="title"/>
            </div>
            <div class="mb-3">
                <label class="form-label" for="description">Descripción (*):</label>
                <Field class="form-control" name="description" as="textarea" rows="8"/>
                <ErrorMessage class="form-text text-danger" name="description"/>
            </div>
            <div class="mb-3 d-flex justify-content-end">
                <button class="btn btn-primary" type="submit" ref="sendbtn">Enviar</button>
            </div>
        </Form>
    </template>
</template>