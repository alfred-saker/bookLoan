<template>
    <Header/>
    <div class="main_add_book">
      <form @submit.prevent="submitForm" enctype="multipart/form-data">
        <p class="alert alert-danger" style="padding: 1em;margin-top: 1em;" v-if="errors.wrong_fields">{{ errors.wrong_fields }}</p>
        <!-- <p class="alert alert-danger" style="padding: 1em;margin-top: 1em;" v-if="error">{{ error }}</p> -->
        <div class="row col-12" style="line-height: 2;" id="form_add_book">
          <h2 class="fs-1">Add a new book</h2>

          <div class="col-6">
            <label for="">Author of book</label>
            <input type="hidden" name="user_id" v-model="user_id">
            <input type="text" v-model="author_book" class="form-control" placeholder="Author of book" aria-label="Author of book" id="author_book" name="author_book">
            <small v-if="errors.author_book" class="text-danger">{{ errors.author_book }}</small>
          </div>
          <div class="col-6">
            <label for="">Title of book</label>
            <input type="text" v-model="title_book" class="form-control" placeholder="Title of Book" aria-label="title book" id="title_book" name="title_book">
            <small v-if="errors.title_book" class="text-danger">{{ errors.title_book }}</small>
          </div>
          <div class="col-6">
            <label for="">Publication date</label>
            <input type="text" v-model="year_publication" class="form-control" aria-label="year of publication" id="year_publication" name="year_publication">
            <small v-if="errors.year_publication" class="text-danger">{{ errors.year_publication }}</small>
          </div>
          <div class="col-6">
            <label for="">Quantity</label>
            <input type="number" v-model="quantity" class="form-control" aria-label="quantity book" id="quantity" name="quantity">
            <small v-if="errors.quantity" class="text-danger">{{ errors.quantity }}</small>
          </div>
          <div class="col-6">
            <label for="">Gender book</label>
            <select class="form-control" v-model="gender_book" aria-label="Gender book" id="gender_book" name="gender_book">
              <option value="">Please select a gender of book</option>
              <option value="Entrepreunariat">Entrepreunariat</option>
              <option value="Economie">Economie</option>
              <option value="Finance">Finance</option>
              <option value="Chretien">Chretien</option>
            </select>
            <small v-if="errors.gender_book" class="text-danger">{{ errors.gender_book }}</small>
          </div>
          <div class="col-6">
            <label for="">Type book</label>
            <select class="form-control" v-model="type_book" aria-label="type_book" id="type_book" name="type_book">
              <option value="">Please select a type of book</option>
              <option value="Numeric">Numeric book</option>
              <option value="Paper">Paper Book</option>
            </select>
            <small v-if="errors.type_book" class="text-danger">{{ errors.type_book }}</small>
          </div>
          <div class="col-6">
            <label for="">Status of books</label>
            <select class="form-control" v-model="status_book" aria-label="status book" id="status_book" name="status_book">
              <option value="" >Please select a status of book</option>
              <option value="true">Avaible</option>
              <option value="false">Not avaible</option>
            </select>
            <small v-if="errors.status_book" class="text-danger">{{ errors.status_book }}</small>
          </div>
          <div class="col-6">
            <label for="">File of books</label>
            <input type="file" name="file_book"  id="file_book" class="form-control">
            <small v-if="errors.file_book" class="text-danger">{{ errors.file_book }}</small>
          </div>
          <div class="col-12">
            <label for="">Image of books</label>
            <input type="file" name="image_book" id="image_book" class="form-control">
            <small v-if="errors.image_book" class="text-danger">{{ errors.image_book }}</small>
          </div>
          <button type="submit" class="btn btn-primary" style="margin-top: 1em;width: auto;">Add book</button>
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
    Header, // Enregistrement du composant Header localement
  },
  data(){
    return{
      user_id:'',
      author_book: '',
      title_book: '',
      year_publication: '',
      quantity: '',
      gender_book: '',
      type_book: '',
      status_book: '',
      // file_book: '',
      // image_book: '',
      errors:{
        author_book: '',
        title_book: '',
        year_publication: '',
        quantity: '',
        gender_book: '',
        type_book: '',
        status_book: '',
        // file_book: '',
        // image_book: '',
        wrong_fields : ''
      }
    }
  },
  methods:{
    async submitForm(){
      this.clearErrors();
      console.log(localStorage.getItem('id'));
      if(this.isValidForm()){
        console.log(this.isValidForm());
        try {
          const response = await axios.post('books/',{
            user:localStorage.getItem('url'),
            author:this.author_book,
            title:this.title_book,
            year_publication:this.year_publication,
            quantity:this.quantity,
            gender:this.gender_book,
            type_book:this.type_book,
            status_book:this.status_book,
            file_book:this.file_book,
            image_book:this.image_book
          },
          {
            headers: {
              'Content-Type': 'application/json', // Si vous envoyez des données JSON
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        console.log(response.data);
        this.$router.push('/');
          console.log(response.data);

          
        } catch (error) {
          if (error.response && error.response.data) {
            this.errors.wrong_fields = "Something wrong, please fill the empty fields";
          }
          console.error('Error:', error.response ? error.response.data : error);
        }
      }
    },
    isValidForm() {
      let valid = true;

      if (!this.author_book.trim()) {
        this.errors.author_book = "Author is required";
        valid = false;
      }
      if (!this.title_book.trim()) {
        this.errors.title_book = "Title is required";
        valid = false;
      }
      if (!this.year_publication) {
        this.errors.year_publication = "year of publication is required";
        valid = false;
      }
      if (!this.quantity) {
        this.errors.quantity = "Quantity is required";
        valid = false;
      }
      if (!this.gender_book) {
        this.errors.gender_book = "Gender is required";
        valid = false;
      }
      if (!this.type_book) {
        this.errors.type_book = "Type of book is required";
        valid = false;
      }
      if (!this.status_book) {
        this.errors.status_book = "Status is required";
        valid = false;
      }
      // if (!this.file_book) {
      //   this.errors.file_book = "File is required";
      //   valid = false;
      // }
      // if (!this.image_book) {
      //   this.errors.image_book = "Image is required";
      //   valid = false;
      // }
      return valid;
    },
    clearErrors() {
      this.errors.author_book = '';
      this.errors.title_book = '';
      this.errors.quantity = '';
      this.errors.gender_book = '';
      this.errors.year_publication = '';
      this.errors.type_book = '';
      this.errors.status_book = '';
      this.errors.file_book = '';
      // this.errors.image_book = '';
      // this.errors.wrong_fields = ''
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