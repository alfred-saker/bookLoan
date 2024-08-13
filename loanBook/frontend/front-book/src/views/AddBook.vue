<template>
  <Header />
  <div class="main_add_book">

    <form @submit.prevent="saveBook" enctype="multipart/form-data">
      <p
        class="alert alert-danger"
        style="padding: 1em; margin-top: 1em"
        v-if="errors.wrong_fields"
      >
        {{ errors.wrong_fields }}
      </p>
      <div class="row col-12" style="line-height: 2" id="form_add_book">
        <h2 class="fs-1">Add a new book</h2>

        <div class="col-6">
          <label for="">Author of book</label>
          <input
            type="text"
            v-model="author_book"
            class="form-control"
            placeholder="Author of book"
            aria-label="Author of book"
            id="author_book"
            name="author_book"
          />
          <small v-if="errors.author_book" class="text-danger">{{ errors.author_book }}</small>
        </div>
        <div class="col-6">
          <label for="">Title of book</label>
          <input
            type="text"
            v-model="title_book"
            class="form-control"
            placeholder="Title of Book"
            aria-label="title book"
            id="title_book"
            name="title_book"
          />
          <small v-if="errors.title_book" class="text-danger">{{ errors.title_book }}</small>
        </div>
        <div class="col-6">
          <label for="">Publication date</label>
          <input
            type="date"
            v-model="year_publication"
            class="form-control"
            aria-label="year of publication"
            id="year_publication"
            name="year_publication"
          />
          <small v-if="errors.year_publication" class="text-danger">{{
            errors.year_publication
          }}</small>
        </div>
        <div class="col-6">
          <label for="">Gender book</label>
          <select
            class="form-control"
            v-model="gender_book"
            aria-label="Gender book"
            id="gender_book"
            name="gender_book"
          >
            <option value="">Please select a gender of book</option>
            <option value="Entrepreunariat">Entrepreunariat</option>
            <option value="Economie">Economie</option>
            <option value="Finance">Finance</option>
            <option value="Chretien">Chretien</option>
          </select>
          <small v-if="errors.gender_book" class="text-danger">{{ errors.gender_book }}</small>
        </div>
        <div class="col-12">
          <label for="">Type book</label>
          <select
            class="form-control"
            v-model="type_book"
            aria-label="type_book"
            id="type_book"
            name="type_book"
            @change="showFileInput"
          >
            <option value="">Please select a type of book</option>
            <option value="Numeric">Numeric book</option>
            <option value="Paper">Paper Book</option>
          </select>
          <small v-if="errors.type_book" class="text-danger">{{ errors.type_book }}</small>
        </div>

        <div class="col-12">
          <label for="">Description of book</label>
          <textarea id="" v-model="description" cols="30" rows="3" class="form-control">
Enter some description</textarea
          >
          <small v-if="errors.description" class="text-danger">{{ errors.description }}</small>
        </div>
        <div class="col-6" v-if="type_book !== 'Paper'">
          <label for="">File of books</label>
          <input
            type="file"
            name="file_book"
            id="file_book"
            class="form-control"
            @change="validateFilePdf"
          />
          <small v-if="errors.file_book" class="text-danger">{{ errors.file_book }}</small>
        </div>
        <div class="col-6">
          <label for="">Image of books</label>
          <input
            type="file"
            name="image_book"
            id="image_book"
            class="form-control"
            @change="validateImage"
          />
          <small v-if="errors.image_book" class="text-danger">{{ errors.image_book }}</small>
        </div>
        <button type="submit" class="btn btn-outline-primary" style="margin-top: 1em; width: 100%">
          Add book
        </button>
      </div>
    </form>
  </div>
  <Footer></Footer>
</template>
<script>
import Header from '@/components/header.vue'
import Footer from '@/components/Footer.vue'
import axios from 'axios'
import { toHandlers } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from "vue-toastification";

export default {
  components: {
    Header,
    Footer
  },
  // Initialisation du toast
  setup() {
    // Get toast interface
    const toast = useToast();

    // Make it available inside methods
    return { toast }
  },
  data() {
    return {
      author_book: '',
      title_book: '',
      year_publication: '',
      gender_book: '',
      type_book: '',
      successMessage: '',
      description: '',
      file_book: null,
      image_book: null,
      display_input_file: false,
      errors: {
        author_book: '',
        title_book: '',
        year_publication: '',
        description: '',
        gender_book: '',
        type_book: '',
        status_book: '',
        file_book: '',
        image_book: '',
        wrong_fields: ''
      }
    }
  },
  methods: {
    showFileInput() {
      if (this.type_book === 'Paper') {
        this.display_input_file = false
      } else {
        this.display_input_file = true
      }
    },
    // Validation du pdf lors de l'upload
    validateFilePdf(event) {
      const file = event.target.files[0]
      if (file && file.type !== 'application/pdf') {
        this.errors.file_book = 'The file must be a PDF'
        this.file_book = null
      } else {
        this.errors.file_book = ''
        this.file_book = file
      }
      console.log(this.file_book);
    },

    // Validation de l'image lors de l'upload
    validateImage(event) {
      const file = event.target.files[0]
      const validImageTypes = ['image/jpeg', 'image/png']
      if (file && !validImageTypes.includes(file.type)) {
        this.errors.image_book = 'The image must be in JPG or PNG format'
        this.image_book = null
      } else {
        this.errors.image_book = ''
        this.image_book = file
      }
      console.log(this.image_book);
    },
    
    async saveBook() {
      // Effacer les erreurs précédentes
      this.clearErrors();

      // Vérifier la validité du formulaire
      if (!this.isValidForm()) {
        return;
      }

      // Créer un objet FormData pour envoyer les données du formulaire
      const formData = new FormData();
      formData.append('user', localStorage.getItem('url'));
      formData.append('author', this.author_book);
      formData.append('title', this.title_book.toUpperCase());
      formData.append('year_publication', this.year_publication);
      formData.append('gender', this.gender_book);
      formData.append('type_book', this.type_book);
      formData.append('status_book', true);
      formData.append('description', this.description);

      // Ajouter les fichiers si nécessaire
      if (this.type_book === 'Numeric') {
        formData.append('pdf_file', this.file_book);
      }
      if (this.image_book) {

        formData.append('picture_books', this.image_book);
      }
      console.log('FormData Entries:', Array.from(formData.entries()));

      try {
        // Envoyer les données du formulaire à l'API
        await axios.post('books/', formData, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`,
            'Content-Type': 'multipart/form-data',
          },
        });

        // Rediriger vers la page d'accueil après la soumission réussie
        this.$router.push('/loanbook/dashboard_book_admin');
        this.toast.success("Great!! Book added successfully");
      } catch (error) {
        // Gérer les erreurs et afficher un message d'erreur approprié
        if (error.response && error.response.data) {
          this.errors.wrong_fields = 'Something went wrong, please fill the empty fields';
        }
        console.error('Error:', error.response ? error.response.data : error);
      }
    },

    isValidForm() {
      let valid = true

      if (!this.author_book.trim()) {
        this.errors.author_book = 'Author is required'
        valid = false
      }
      if (!this.title_book.trim()) {
        this.errors.title_book = 'Title is required'
        valid = false
      }
      if (!this.year_publication) {
        this.errors.year_publication = 'year of publication is required'
        valid = false
      }
      if (!this.description) {
        this.errors.description = 'Description is required'
        valid = false
      }
      if (!this.gender_book) {
        this.errors.gender_book = 'Gender is required'
        valid = false
      }
      if (!this.type_book) {
        this.errors.type_book = 'Type of book is required'
        valid = false
      }
      if (this.type_book === 'Numeric' && !this.file_book) {
        this.errors.file_book = 'File book is required'
        console.log('sqdfs')
        valid = false
      }
      if (!this.image_book) {
        this.errors.image_book = 'Image book is required'
        console.log('sqdfs2')
        valid = false
      }
      return valid
    },

    clearErrors() {
      this.errors.author_book = ''
      this.errors.title_book = ''
      this.errors.quantity = ''
      this.errors.gender_book = ''
      this.errors.year_publication = ''
      this.errors.type_book = ''
      this.errors.status_book = ''
      this.errors.image_book = ''
      this.errors.file_book = ''
      this.errors.wrong_fields = ''
    }
  }
}
</script>

<style>
#form_add_book {
  max-width: 800px;
  margin: 0 auto;
}
.main_add_book {
  height: 100vh;
  margin-bottom: 14em;
}
</style>
