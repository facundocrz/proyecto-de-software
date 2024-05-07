<script setup>
const props = defineProps(['currentPage', 'totalPage', 'goToPage', 'prevPage', 'nextPage'])
</script>

<template>
  <nav aria-label="Page navigation">
    <ul class="pagination">
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <a class="page-link" @click="prevPage" href="#" aria-label="Previous">
          <span aria-hidden="true">&laquo;</span>
        </a>
      </li>
      <li
        class="page-item"
        v-for="page in totalPage"
        :key="page"
        :class="{ active: currentPage === page }"
      >
        <a class="page-link" @click="goToPage(page)" href="#">{{ page }}</a>
      </li>
      <li class="page-item" :class="{ disabled: currentPage === totalPage }">
        <a class="page-link" @click="nextPage" href="#" aria-label="Next">
          <span aria-hidden="true">&raquo;</span>
        </a>
      </li>
    </ul>
  </nav>
</template>
