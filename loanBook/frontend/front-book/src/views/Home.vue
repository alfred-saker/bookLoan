<template>
    
  <Header/>
  <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
  <div class="relative overflow-x-auto shadow-md">
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3">Title</th>
          <th scope="col" class="px-6 py-3">Author</th>
          <th scope="col" class="px-6 py-3">Gender</th>
          <th scope="col" class="px-6 py-3">Type of book</th>
          <th scope="col" class="px-6 py-3">Publication date</th>
          <th scope="col" class="px-6 py-3">Status book</th>
          <th scope="col" class="px-6 py-3">All download</th>
          <th scope="col" class="px-6 py-3">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr
          class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700"
          v-for="book in books"
          :key="book.id">
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ book.title }}
          </td>
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ book.author }}
          </td>
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ book.gender }}
          </td>
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ book.type_book }}
          </td>
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ book.year_publication }}
          </td>
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ book.status_book ? 'Available' : 'Not available' }}
          </td>
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ book.number_dowload }}
          </td>
          <td class="px-6 py-4 flex">
            <div>
              <router-link :to="`/detail_book/${extractBookId(book.url)}`" class="btn btn-outline-primary" >Explore</router-link>
            </div>
            <div>
              <router-link :to="`/detail_book/${extractBookId(book.url)}`" class="btn btn-outline-danger" >Delete</router-link>
            </div>
            &nbsp;
            <div v-if="username">
              <router-link :to="`/add_borrow/`" class="btn btn-outline-secondary" v-if="book.type_book === 'Paper'" >Borrow</router-link>
              <router-link :to="`/detail_book/${extractBookId(book.url)}`" class="btn btn-outline-secondary" v-else >Download</router-link>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</template>
  
<script>
  import { RouterLink } from 'vue-router';
  import Header from '../components/header.vue';
  import axios from 'axios'

  export default {
  components: { Header },
  data() {
    return {
      books: [],
      username: localStorage.getItem('username') || '',
      token: localStorage.getItem('token') || '',
      successMessage: this.$route.params.successMessage,
    };
  },
  mounted() {
    if (this.token) {
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
    }
    this.fetchBooks();
  },
  methods: {
    fetchBooks() {
      axios.get(`books/`).then((response) => {
        this.books = response.data.results;
      }).catch((error) => {
        console.error('Erreur lors de la récupération des données : ', error);
      });
    },
    
    extractBookId(url) {
      const segments = url.split('/');
      return segments[segments.length - 2]; // L'avant-dernier segment contient l'ID du livre
    }
  }
};
</script>

<style>
</style>
