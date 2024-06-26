<template>
  <Header />

  <div class="p-2">
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="p-3">Title</th>
          <th scope="col" class="p-3">Author</th>
          <th scope="col" class="p-3">Gender</th>
          <th scope="col" class="p-3">Type of book</th>
          <th scope="col" class="p-3">Publication date</th>
          <th scope="col" class="p-3">Status book</th>
          <th scope="col" class="p-3">All download & Borrow</th>
          <th scope="col" class="p-3">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr
          class="bg-dark text-white"
          v-for="book in books"
          :key="book.id" style="border-bottom: 2px solid darkslategrey;">
          <td scope="row" class="text-wrap p-3">
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
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white" v-if="book.type_book === 'Paper'">
            {{ book.borrow_count }}
          </td>
          <td
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white" v-else>
            {{ book.download_count }}
          </td>

          <td class="px-6 py-4 flex">
            <div class="btn-group" role="group" aria-label="Button group with nested dropdown">
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-outline-light dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  Select Action
                </button>
                <ul class="dropdown-menu p-3">
                  <router-link :to="`/loanbook/books/detail_book/${extractBookId(book.url)}`" class="btn btn-outline-secondary mb-2">Explore</router-link>
                  <button @click="downloadBook(book.url)" class="btn btn-outline-secondary mb-2" v-if="book.type_book === 'Numeric' && token">Download</button>
                  <button data-bs-toggle="modal" :data-bs-target="`#deleteModal${book.id}`" class="btn btn-outline-danger mb-2" v-if=" (token && is_admin === 'true') && (extractBookId(book.user) === extractBookId(user_id))">Delete book</button>
                </ul>
              </div>
            </div>
            <div class="modal fade" :id="`deleteModal${book.id}`" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5 text-danger" id="staticBackdropLabel">Caution Important action</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body text-dark">
                    <p class="fs-5">Are you sure you want to delete this book?</p><br>
                    <p class="fs-5">Warning: This action is irreversible</p>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">No, cancel</button>
                    <button type="button" @click="deleteBook(book.url)" class="btn btn-outline-danger" data-bs-dismiss="modal">Yes, I'm sure</button>
                  </div>
                </div>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <nav aria-label="Page navigation example" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: !prev }">
          <button class="page-link" @click="prevPage" :disabled="!prev">Previous</button>
        </li>
        <li class="page-item" :class="{ active: currentPage === page }" v-for="page in totalPages" :key="page">
          <button class="page-link" @click="goToPage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: !next }">
          <button class="page-link" @click="nextPage" :disabled="!next">Next</button>
        </li>
      </ul>
    </nav>
  </div>
  <Footer></Footer>
</template>

<script>
import { RouterLink } from 'vue-router';
import Footer from '@/components/Footer.vue'
import Header from '../components/header.vue';
import axios from 'axios';
import { useToast } from "vue-toastification";

export default {
  components: { Header,Footer },
  // Initialisation du toast
  setup() {
    // Get toast interface
    const toast = useToast();

    // Make it available inside methods
    return { toast }
  },
  data() {
    return {
      books: [],
      username: localStorage.getItem('username') || '',
      token: localStorage.getItem('token') || '',
      user_id : localStorage.getItem('url'),
      is_admin:localStorage.getItem('is_staff'),
      currentPage: 1,
      limit: 10, // Nombre de livres par page
      offset: 0, // Position de départ
      next: null,
      prev: null,
      totalPages: 0,
      success_message: '',
      wrong_fields: ''
    };
  },
  mounted() {
    const logoutMessage = localStorage.getItem('logoutMessage');
    const borrowMessage = localStorage.getItem('borrowMessage');
    if (logoutMessage) {
      this.successMessage = logoutMessage;
      this.toast.success(logoutMessage);  // Afficher le toast
      localStorage.removeItem('logoutMessage');  // Supprimer le message après l'affichage
    }
    if (borrowMessage) {
      this.successMessage = borrowMessage;
      this.toast.success(borrowMessage);  // Afficher le toast
      localStorage.removeItem('borrowMessage');  // Supprimer le message après l'affichage
    }
    
    if (this.token) {
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
    }

    this.fetchBooks();
  },
  methods: {
    downloadBook(bookID) {
      console.log(this.extractBookId(bookID));
      axios.get(`books/download/${this.extractBookId(bookID)}`, {
        responseType: 'blob', // Pour traiter la réponse en tant que fichier binaire
        headers: {
          'Authorization': `Token ${this.token}`
        }
      }).then((response) => {
        console.log(response);
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      const contentDisposition = response.headers['content-disposition'];
      let fileName = 'downloaded_book.pdf'; // Default filename

      // Extraire le nom de fichier de l'en-tête content-disposition s'il est présent
      if (contentDisposition) {
        const fileNameMatch = contentDisposition.match(/filename="(.+)"/);
        if (fileNameMatch.length === 2) {
          fileName = fileNameMatch[1];
        }
      }

      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();
      this.toast.success("Downloaded book");
      console.log('Livre téléchargé');
      }).catch((error) => {
        console.log('Erreur lors du téléchargement', error);
      });
    },

    fetchBooks() {
      axios.get(`books/?limit=${this.limit}&offset=${this.offset}`).then((response) => {
        this.books = response.data.results;
        this.next = response.data.next;
        this.prev = response.data.previous;
        this.totalPages = Math.ceil(response.data.count / this.limit);
        this.currentPage = (this.offset / this.limit) + 1;
      }).catch((error) => {
        console.error('Erreur lors de la récupération des données : ', error);
      });
    },
    nextPage() {
      if (this.next) {
        this.offset += this.limit;
        this.fetchBooks();
      }
    },
    prevPage() {
      if (this.prev) {
        this.offset -= this.limit;
        this.fetchBooks();
      }
    },
    goToPage(page) {
      this.offset = (page - 1) * this.limit;
      this.fetchBooks();
    },

    async deleteBook(book_id) {
      try {
        // Extraire l'ID du livre
        const bookId = this.extractBookId(book_id);

        // Supprimer le livre
        await axios.delete(`books/${bookId}/`, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${this.token}`
          }
        });

        // Rafraîchir la liste des livres
        this.fetchBooks();

        // Afficher le toast de succès
        this.toast.success("Book successfully deleted");

      } catch (error) {
        if (error.response && error.response.data) {
          this.wrong_fields = "Oups! Something went wrong, please try again";
        }
        console.error('Error:', error.response ? error.response.data : error);
      }
    },
    extractBookId(url) {
      if(url){
        const segments = url.split('/');
        return segments[segments.length - 2]; // L'avant-dernier segment contient l'ID d'un élément
      }
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;1,200;1,500;1,600&display=swap');

body{
  font-family: "Kanit", sans-serif;
  font-weight: 300;
  font-style: normal;
}
table {
  max-width: 100%;
}
</style>
