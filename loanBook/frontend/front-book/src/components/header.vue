<template>
  <div class="container-header-admin">
    <nav>
      <div class="block_logo">
        <img :src="logo" alt="Logo BooklLoan" width="50px" class="rounded-1" /> &nbsp;
        <!-- <h1 class="fs-3">BookLoan</h1> -->
      </div>
      <div class="input-group">
        <span class="input-group-text" id="basic-addon1">
          <i class="bi bi-search"></i>
        </span>
        <input
          type="text"
          class="form-control"
          placeholder="Search"
          aria-label="Search"
          aria-describedby="basic-addon1"
        />
      </div>
      <div class="user_profil">
        <p>Alfred Saker</p>
        <img :src="user_profile" alt="" srcset="" class="rounded-circle" width="50px" />
      </div>
    </nav>
  </div>
</template>
<script>
import axios from 'axios'
import { document } from 'postcss'
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
      logo: '/images/logo.jpg',
      token: localStorage.getItem('token'),
      user_profile: '/images/user.png',
      burger_icon: 'images/burger-icon.svg',
      user_id: localStorage.getItem('url'),
      list_books: [],
      title_book: '',
      todayDate: this.getTodayDate(),
      borrow_date: '',
      showNav: true,
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
    changeScreen() {
      this.showNav = !this.showNav
    },
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
      const selectedBook = this.list_books.find(
        (book) => book.url === this.title_book && book.status_book === true
      )
      if (selectedBook && selectedBook.type_book === 'Numeric') {
        this.errors.title_book = 'You cannot borrow books of type Numeric.'
      } else if (!selectedBook) {
        this.errors.title_book = 'Please select a valid book.'
      } else {
        this.errors.title_book = ''
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
              Authorization: `Token ${localStorage.getItem('token')}`
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
                  Authorization: `Token ${localStorage.getItem('token')}`
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
.container-header-admin {
  padding: 2em;
}
.container-header-admin nav {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: aqua;
  padding: 1em;
}
.container-header-admin nav .input-group {
  width: 30%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.container-header-admin nav .user_profil {
  width: 50%;
  display: flex;
  align-items: center;
}
.container-header-admin nav .block_logo {
  display: flex;
  align-items: center;
}
@media screen and (max-width: 768px) {
}
</style>
