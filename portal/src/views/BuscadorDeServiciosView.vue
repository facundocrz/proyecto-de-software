<script setup>
import Pagination from '@/components/Pagination.vue'
import { ref, reactive, onMounted } from 'vue'
import * as api from "../methods/api";
import { flash } from "../methods/alerts";

const searchText = ref('');
const selectedServiceType = ref('');
const serviceTypes = ref([]);
const servicios = reactive({
    data: [],
    page: 1,
    per_page: 2,
    total: 1,
});

async function onSubmit() {
    servicios.page = 1;
    await searchServices();
}

async function searchServices() {
    try {
        const { code, data } = await api.fetchServiceSearch(searchText.value, selectedServiceType.value, servicios.page);
        if (code === 200) {
            servicios.data = data.data;
            servicios.total = data.total;
            servicios.page = data.page;
            servicios.per_page = data.per_page;
        } else {
            flash("Hubo un error al realizar la busqueda. Por favor, vuelva a intentarlo.", "danger");
        }
    } catch (error) {
        flash("Hubo un error al realizar la busqueda. Por favor, vuelva a intentarlo.", "danger");
    }
}

async function loadServiceTypes() {
    try {
        const { code, data } = await api.fetchServiceTypes();
        if (code === 200)
            serviceTypes.value = [...data.data];
        else
            flash("Hubo un error al obtener los tipos de servicios.", "danger");
    } catch (error) {
        flash("Hubo un error al obtener los tipos de servicios.", "danger");
    }
}

function calculateTotalPages(total, perPage) {
    return Math.ceil(total / perPage);
}

const goToPage = (page) => {
    servicios.page = page;
    searchServices();
}

const prevPage = () => {
    if (servicios.page > 1) {
        servicios.page--;
        searchServices();
    }
}

const nextPage = () => {
    const totalPages = calculateTotalPages(servicios.total, servicios.per_page);
    if (servicios.page < totalPages) {
        servicios.page++;
        searchServices();
    }
}

onMounted(loadServiceTypes);
</script>

<!-- ServiceList.vue -->
<template>
    <div class="container">
        <h1>Bienvenido/a al Buscador de Servicios</h1>
        <div class="row">
            <div class="col-3">
                <div class="card">
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <label for="searchText" class="form-label">Título, descripción del servicio, palabras clave o nombre de la
                                Institucion:</label>
                            <!-- Restringe a que no se comience e ingrese mas de un espacio en blanco y solo se ingresen letras y numeros-->
                            <input v-model="searchText" class="form-control" id="searchText" type="text" required pattern=^[a-zA-Zá-úÁ-ÚñÑ0-9]+(\s[a-zA-Z0-9]+)*$>
                            
                            <label for="serviceType" class="form-label">*Tipo de servicio:</label>
                            <select v-model="selectedServiceType" id="serviceType" class="form-select">
                                <option v-for="type in serviceTypes" :key="type.id" :value="type.name">{{ type.name }}
                                </option>
                            </select>
                            <p class="form-text">*Opcional</p>

                            <button type="submit" class="btn btn-primary">Buscar</button>
                        </form>
                    </div>
                </div>
            </div>
            <div v-if="servicios.data.length > 0" class="col">
                <div class="card mb-3" v-for="service in servicios.data" :key="service.id">
                    <div class="card-header">
                        <h4 class="mb-0">{{ service.title }}</h4>
                    </div>
                    <div class="card-body">
                        <p>Descrpcion: {{ service.description }}</p>
                        <p>Institucion a la que pertence: {{ service.institution_name }}</p>
                        <p>Tipo de Servicio: {{ service.type_name }}</p>
                        <RouterLink :to="`/servicios/${service.id}`" class="btn btn-primary">
                            Detalle
                        </RouterLink>
                    </div>
                </div>
                <pagination :currentPage="servicios.page"
                    :totalPage="calculateTotalPages(servicios.total, servicios.per_page)" :goToPage="goToPage"
                    :prevPage="prevPage" :nextPage="nextPage"/>
            </div>
            <!-- Mostrar el mensaje solo si no hay servicios y se ha realizado una búsqueda -->
            <div v-else class="col">
                <p>No se encontraron servicios.</p>
            </div> <!-- !== primero compara el tipo de dato y despues objeto-->
        </div>
    </div>
</template>