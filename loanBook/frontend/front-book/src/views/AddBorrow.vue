<template>
    <Header/>
    <div class="main_add_book">
      <form @submit.prevent="submitForm" enctype="multipart/form-data">
        <p class="alert alert-danger" style="padding: 1em;margin-top: 1em;" v-if="errors.wrong_fields">{{ errors.wrong_fields }}</p>
        <div class="row col-12" style="line-height: 2;" id="form_add_book">
          <h2 class="fs-1">Add a new borrow</h2>

          <div class="col-12">
            <label for="">Title of book</label>
            <select v-model="title_book" class="form-control" aria-label="title book" id="title_book" name="title_book">
                <option value=""  selected>Please select a book</option>
                <option v-for="list_book in list_books.results" :key="list_book.id" :value="list_book.url">{{ list_book.title }}</option>
            </select>
            <small v-if="errors.title_book" class="text-danger">{{ errors.title_book }}</small>
          </div>
          <div class="col-12">
            <label for="borrow_date">Borrow date</label>
            <input type="date" v-model="borrow_date" class="form-control" name="borrow_date" :min="todayDate">
            <small v-if="errors.borrow_date" class="text-danger">{{ errors.borrow_date }}</small>
          </div>
          <div class="col-12">
            <label for="borrow_date">Return date</label>
            <input type="date" v-model="return_date" class="form-control" name="return_date" :min="todayDate" :max="maxReturnDate">
            <small v-if="errors.return_date" class="text-danger">{{ errors.return_date }}</small>
          </div>

          <button type="submit" class="btn btn-outline-primary" style="margin-top: 1em;width: auto;">Add borrow</button>
        </div>
      </form>
    </div>
    
</template>
<script>
import Header from '@/components/header.vue';
import axios from 'axios';
import { toHandlers } from 'vue';
import { useRoute } from 'vue-router';

export default{
  components: {
    Header,
  },
  data(){
    return{
      user_id:'',
      token: localStorage.getItem('token') || '',
      list_books:[],
      title_book: '',
      todayDate: this.getTodayDate(),
     borrow_date: this.getTodayDate(),
      return_date:'',
      errors:{
        title_book: '',
        borrow_date:'',
        return_date:'',
        wrong_fields : ''
      },
      logic:{
        borrow_date:'',
        return_date:''
      }
    }
  },
  computed: {
        maxReturnDate() {
            const maxDate = new Date();
            maxDate.setDate(maxDate.getDate() + 30); // Ajoute 30 jours
            return maxDate.toISOString().split('T')[0];
        }
    },
  mounted() {
    const book_id = this.$route.params.book_id
    console.log(book_id)
    console.log(localStorage.getItem('url'))
    if (this.token) {
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`
    }
    axios
        .get(`books/`)
        .then((response) => {
        this.list_books = response.data
        })
        .catch((error) => {
        console.error('Erreur lors de la récupération des données : ', error)
    })
  },
  methods:{
    async submitForm(){
      this.clearErrors();
      console.log(localStorage.getItem('id'));
      if(this.isValidForm()){
        console.log(this.isValidForm());
        try {
          const response = await axios.post('emprunts/',{
            user:localStorage.getItem('url'),
            books:this.title_book,
            borrow_date:this.borrow_date,
            return_date:this.return_date
          },
          {
            headers: {
              'Content-Type': 'application/json', // Si vous envoyez des données JSON
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        console.log(response.data);
        this.$router.push('/home');
          console.log(response.data);

          
        } catch (error) {
          if (error.response && error.response.data) {
            this.errors.wrong_fields = "Something wrong, please fill the empty fields";
          }
          console.error('Error:', error.response ? error.response.data : error);
        }
      }
    },
    getTodayDate() {
            const today = new Date();
            return today.toISOString().split('T')[0];
    },
    isValidForm() {
      let valid = true;

      if (!this.title_book.trim()) {
        this.errors.title_book = "Title is required";
        valid = false;
      }
      if (!this.borrow_date.trim()) {
        this.errors.borrow_date = "Borrow date is required";
        valid = false;
      }
      if (!this.return_date.trim()) {
        this.errors.return_date = "Return date is required";
        valid = false;
      }
      return valid;
    },
    clearErrors() {
        this.errors.title_book = '';
        this.errors.borrow_date = '';
        this.errors.return_date = '';
    },
    extractBookId(url) {
      const segments = url.split('/');
      return segments[segments.length - 2]; // L'avant-dernier segment contient l'ID du livre
    }
  }
}
</script>

<style>
#form_add_book{
  max-width: 800px;
  margin: 0 auto;
}
.main_add_book{
  height: 100vh;
}
</style>