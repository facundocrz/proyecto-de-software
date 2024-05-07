<script setup>
    import { ref } from "vue";
    import { RouterLink, useRoute } from "vue-router";
    import * as api from "../methods/api.js";
    import { flash } from "../methods/alerts.js";

    const route = useRoute();
    const id = route.params.id;

    const service = ref(null);
    const institution = ref(null);

    function onMapMounted() {
        const inst = institution.value;
        const coords = inst.location.split(";").map(n => parseFloat(n));

        let map = L.map('map').setView(coords, 14);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
        
        let marker = L.marker(coords).addTo(map);
        marker.bindPopup(`<b>${inst.name}</b><br>${inst.address}<br>${inst.contact}`)
    }

    function onInstitutionDataFetched(code, data) {
        if (code === 200) {
            institution.value = data;
        } else {
            flash("Hubo un error al obtener los datos de la institución. Por favor, vuelva a intentarlo.", "danger");
        }
    }

    function onServiceDataFetched(code, data) {
        if (code === 200) {
            api.fetchInstitution(data.institution_id).then(({ code, data }) => {
                onInstitutionDataFetched(code, data);
            });
            service.value = data;
        } else {
            flash("Hubo un error al obtener los datos del servicio. Por favor, vuelva a intentarlo.", "danger");
        }
    }

    api.fetchService(id).then(({ code, data }) => {
            onServiceDataFetched(code, data);
    });
</script>

<template>
    <div class="row">
        <div class="col">
            <template v-if="service">
                <div class="card mb-3">
                    <h4 class="card-header">{{ service.title }}</h4>
                    <div class="card-body">
                        <h5 class="card-title">Tipo:</h5>
                        <p class="card-text">{{ service.type_name }}</p>
                        <h5 class="card-title">Descripción:</h5>
                        <p class="card-text">{{ service.description }}</p>
                        <h5 class="card-title">Palabras clave:</h5>
                        <p class="card-text">{{ service.keywords.join(", ") }}</p>
                        <RouterLink :to="`/servicios/${$route.params.id}/request`">
                            <button type="button" class="btn btn-primary">Solicitar</button>
                        </RouterLink>
                    </div>
                </div>
            </template>
            <template v-if="institution">
                <div class="card mb-3">
                    <h4 class="card-header">{{ institution.name }}</h4>
                    <div class="card-body">
                        <h5 class="card-title">Dirección:</h5>
                        <p class="card-text">{{ institution.address }}</p>
                        <h5 class="card-title">Contacto:</h5>
                        <p class="card-text">{{ institution.contact }}</p>
                        <h5 class="card-title">Sitio web:</h5>
                        <p class="card-text">{{ institution.web }}</p>
                        <h5 class="card-title">Horarios de atención:</h5>
                        <p class="card-text">{{ institution.availability_schedule }}</p>
                        <h5 class="card-title">Palabras clave:</h5>
                        <p class="card-text">{{ institution.keywords.join(", ") }}</p>
                    </div>
                </div>
            </template>
        </div>
        <div class="col-4">
            <template v-if="institution">
                <div class="card mb-3">
                    <h4 class="card-header">Ubicación</h4>
                    <div class="card-body">
                        <div id="map" class="rounded" style="height: 24em;" @vue:mounted="onMapMounted">
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>