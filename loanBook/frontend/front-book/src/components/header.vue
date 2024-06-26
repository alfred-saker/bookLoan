<template>
<div class="min-h-full w-100">
    <nav class="bg-dark">
      <div class="container-fluid">
        <div class="d-flex align-items-center justify-content-between p-2">
          <div class="col-md-auto d-md-flex">
            <div class="d-flex align-items-baseline space-x-4">
              <router-link
                to="/loanbook/dashboard_book_admin"
                class="text-light btn btn-link px-3 py-2 text-sm font-medium fs-6 text-decoration-none"
                aria-current="page"
                >Home</router-link
              >
              <router-link
                to="/loanbook/user"
                class="text-light btn btn-link px-3 py-2 text-sm font-medium fs-6 text-decoration-none"
                >All User</router-link
              >
              <router-link
                to="/loanbook/about_us"
                class="text-light btn btn-link px-3 py-2 text-sm font-medium fs-6 text-decoration-none"
                >About Us</router-link
              >
            </div>
          </div>
          <div class="col-md-auto d-md-flex align-items-center" v-if="token">
            
            <div v-if="username">
              <h2 class="text-light">Welcome, {{ username }}&nbsp;&nbsp;</h2>
            </div>
            <div>
              <button @click="logout" class="btn btn-outline-light">Logout</button>
            </div>
            <div>
              &nbsp;
              <router-link to="/loanbook/user/profile" class="btn btn-outline-light"
                >My profile</router-link
              >
            </div>
          </div>
          <div class="col-md-auto d-md-flex align-items-center" v-else>
            <div>
              &nbsp;
              <router-link to="/loanbook/login" class="btn btn-outline-light"
                >Login</router-link
              >
            </div>
            <div>
              &nbsp;
              <router-link to="/loanbook/register" class="btn btn-outline-light"
                >Register</router-link
              >
            </div>
          </div>
        </div>
      </div>
    </nav>

    <header class="bg-white shadow p-3 d-flex flex-column flex-md-row justify-content-between align-items-center">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-dark">Dashboard Book 🚀</h1>
        <p></p>
      </div>
      <div
        v-if="username && is_staff === 'true'"
        class="d-flex flex-column flex-md-row "
      >
        <router-link to="/loanbook/books/add_book" class="btn btn-outline-primary"
          >New Book</router-link
        >
        &nbsp;
        <button class="btn btn-outline-dark" data-bs-toggle="modal" data-bs-target="#exampleModal">
          New Borrow
        </button>
        &nbsp;
        <router-link to="/loanbook/statitic_book" class="btn btn-outline-secondary"
          >View Statistic Book</router-link
        >
        &nbsp;
      </div>
      <div v-else-if="username && is_staff === 'false'" class="d-flex align-items-center">
        <button class="btn btn-outline-dark" data-bs-toggle="modal" data-bs-target="#exampleModal">
          New Borrow
        </button>
        &nbsp;
      </div>
    </header>

    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Add a new borrow</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveBorrow" enctype="multipart/form-data">
              <p
                class="alert alert-danger"
                style="padding: 1em; margin-top: 1em"
                v-if="errors.wrong_fields"
              >
                {{ errors.wrong_fields }}
              </p>
              <div class="row g-3" id="form_add_book">
                <div class="col-12">
                  <label for="title_book">Title of book</label>
                  <select
                    v-model="title_book"
                    @change="validateSelectedBook"
                    class="form-control"
                    aria-label="title book"
                    id="title_book"
                    name="title_book"
                  >
                    <option value="" selected>Please select a book</option>
                    <option
                      v-for="list_book in filtered_books"
                      :key="list_book.url"
                      :value="list_book.url"
                    >
                      {{ list_book.title }}
                    </option>

                  </select>
                  <small v-if="errors.title_book" class="text-danger">{{
                    errors.title_book
                  }}</small>
                </div>
                <div class="col-12">
                  <label for="borrow_date">Borrow date</label>
                  <input
                    type="date"
                    v-model="borrow_date"
                    class="form-control"
                    name="borrow_date"
                    :min="todayDate"
                    readonly
                  />
                  <small v-if="errors.borrow_date" class="text-danger">{{
                    errors.borrow_date
                  }}</small>
                </div>
                <div class="d-flex">
                  <button
                    type="submit"
                    class="btn btn-outline-primary"
                    style="margin-top: 1em; width: auto"
                  >
                    Add borrow
                  </button>
                  &nbsp;
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    data-bs-dismiss="modal"
                    style="margin-top: 1em; width: auto"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
  import axios from 'axios'
  import { useToast } from 'vue-toastification'
  export default {
    setup() {
      // Get toast interface
      const toast = useToast()

      // Make it available inside methods
      return { toast }
    },
    data() {
      return {
        username: '',
        is_staff: '',
        // logo:'images/logo_bookloan.svg',
        token:localStorage.getItem('token'),
        user_profile: 'images/user_profile.png',
        user_id: localStorage.getItem('url'),
        list_books: [],
        title_book: '',
        todayDate: this.getTodayDate(),
        borrow_date: '',
        errors: {
          title_book: '',
          borrow_date: '',
          wrong_fields: ''
        }
      }
    },
    created() {
      this.username = localStorage.getItem('username')
      this.is_staff = localStorage.getItem('is_staff')
      this.fetchBooks()
    },
    methods: {
      fetchBooks() {
        if (localStorage.getItem('token')) {
          axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`
        }
        axios
          .get('books/')
          .then((response) => {
            this.list_books = response.data.results
          })
          .catch((error) => {
            console.error('Erreur lors de la récupération des données : ', error)
          })
        this.borrow_date = this.getTodayDate()
      },
      logout() {
        axios
          .post('logout/')
          .then(() => {
            localStorage.clear()
            delete axios.defaults.headers.common['Authorization']
            localStorage.setItem('logoutMessage', 'Your are logout now') // Stocker le message
            window.location.href = '/loanbook/dashboard_book_admin'
          })
          .catch((error) => {
            console.error('Erreur lors de la déconnexion : ', error)
          })
      },
      getTodayDate() {
        const today = new Date()
        return today.toISOString().slice(0, 10)
      },
      validateSelectedBook() {
        const selectedBook = this.list_books.find((book) => book.url === this.title_book && book.status_book === true)
        if (selectedBook && selectedBook.type_book === 'Numeric') {
          this.errors.title_book = 'You cannot borrow books of type Numeric.'
        } else if (!selectedBook) {
          this.errors.title_book = 'Please select a valid book.';
        } else {
          this.errors.title_book = '';
        }
      },
      saveBorrow() {
        this.clearErrors()
        if (this.isValidForm()) {
          const data_borrow = {
            user: localStorage.getItem('url'),
            books: this.title_book,
            borrow_date: this.borrow_date
            
          }
          console.log('Data Borrow:', data_borrow)
          axios
            .post('emprunts/', data_borrow, {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`
              }
            })
            .then(() => {
              let bookId = this.extractBookId(this.title_book)
              console.log(bookId)
              return axios.get(`books/${bookId}/`, {
                headers: {
                  Authorization: `Token ${localStorage.getItem('token')}`
                }
              })
            })
            .then((response) => {
              const book = response.data
              const book_id = this.extractBookId(book.url)

              const updatedBorrowCount = book.borrow_count + 1
              return axios.patch(
                `books/${book_id}/`,
                {
                  status_book: false,
                  borrow_count: updatedBorrowCount
                },
                {
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('token')}`
                  }
                }
              )
            })
            .then(() => {
              localStorage.setItem('borrowMessage', 'Borrowed with success. Enjoy your reading') // Stocker le message
              window.location.href = '/loanbook/dashboard_book_admin'
            })
            .catch((error) => {
              if (error.response && error.response.data) {
                this.errors.wrong_fields = 'Something went wrong, please fill the empty fields'
              }
              console.error('Error:', error.response ? error.response.data : error)
            })
        }
      },
      isValidForm() {
        let valid = true
        if (!this.title_book.trim()) {
          this.errors.title_book = 'Title is required'
          valid = false
        }
        if (!this.borrow_date.trim()) {
          this.errors.borrow_date = 'Borrow date is required'
          valid = false
        }
        return valid
      },
      clearErrors() {
        this.errors.title_book = ''
        this.errors.borrow_date = ''
      },
      extractBookId(url) {
        const segments = url.split('/')
        return segments[segments.length - 2]
      }
    },
    computed: {
      filtered_books() {
        return this.list_books.filter(
          (book) => book.status_book === true && book.type_book === 'Paper'
        )
      }
    }
  }
</script>

<style>
.burger_btn{
  display: none;
}

@media screen and(max-width:760px) {
  .burger_btn{
   display: block;
  }
  .container-fluid{
    display: block;
  }

}
</style>
