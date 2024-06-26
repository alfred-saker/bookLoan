<template>
  <Header></Header>
  <div class="container">
    <div class="card">
      <div class="card-body">
        <div class="row">
          <div class="col-lg-7 col-md-7 col-sm-6">
            <h2 class="fs-1">{{ book.title }}</h2>
            <br />
            <h3 class="card-subtitle fs-2 fw-bold">{{ book.author }}</h3>
            <h6 class="card-subtitle">Add by <span style="font-weight: 600;">{{ book.user }}</span></h6>
            <h3 class="box-title mt-5 fs-2">Book description</h3>
            <br />
            <p v-if="book.description" class="lh-base text-start">
             <q>{{ book.description }}</q>
            </p>
            <p v-else>
             Sorry, description doesn't exist for this book 😣
            </p> <br>
            <p v-if="book.pdf_file" style="font-size: 20px;">Do you want to download this book? Click  <strong><a href="">here</a></strong></p>
            <div class="col-lg-12 col-md-12 col-sm-12" v-if="!isEditing">
              <h3 class="box-title mt-5" style="font-size: 30px;">General Infos</h3>
              <br />
              <div class="table-responsive">
                <table class="table table-striped table-product">
                  <tbody>
                    <tr>
                      <td width="full">Title</td>
                      <td>{{ book.title }}</td>
                    </tr>
                    <tr>
                      <td>Author</td>
                      <td>{{ book.author }}</td>
                    </tr>
                    <tr>
                      <td>publication date</td>
                      <td>{{ book.year_publication }}</td>
                    </tr>
                    <tr>
                      <td>Type of book</td>
                      <td>{{ book.type_book }}</td>
                    </tr>
                    <tr>
                      <td>Gender of book</td>
                      <td>{{ book.gender }}</td>
                    </tr>
                    <tr>
                      <td>Number of download</td>
                      <td>{{ book.number_dowload }}</td>
                    </tr>
                    <tr>
                      <td>Status book</td>
                      <td>{{ book.status_book ? 'Available' : 'Not available' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-if="token && is_staff === 'true' && book.user === username">
                <button @click="startEditing" class="btn btn-outline-dark" style="width: auto"
                  >Edit book</button
                > &nbsp;
                <button @click="deleteBook" class="btn btn-outline-danger" style="width: auto">Delete book</button>
              </div>
            </div>
            <div class="col-lg-12 col-md-12 col-sm-12" v-else>
              <form @submit.prevent="saveChanges" enctype="multipart/form-data">
                <div class="row col-12" style="line-height: 2" id="form_add_book">
                  <h2 class="fs-1">Edit book</h2>
                    <p class="alert alert-danger" v-if="errors.wrong_fields">{{ errors.wrong_fields }}</p>
                  <div class="col-6">
                    <label for="">Author of book</label>
                    <input type="hidden" name="user_id" v-model="user_id" />
                    <input
                      type="text"
                      v-model="author_book"
                      class="form-control"
                      placeholder="Author of book"
                      aria-label="Author of book"
                      id="author_book"
                      name="author_book"
                    />
                    <small v-if="errors.author_book" class="text-danger">{{
                      errors.author_book
                    }}</small>
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
                    <small v-if="errors.title_book" class="text-danger">{{
                      errors.title_book
                    }}</small>
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
                    <small v-if="errors.gender_book" class="text-danger">{{
                      errors.gender_book
                    }}</small>
                  </div>
                  <div class="col-6">
                    <label for="">Type book</label>
                    <select
                      class="form-control"
                      v-model="type_book"
                      aria-label="type_book"
                      id="type_book"
                      name="type_book"
                    >
                      <option value="">Please select a type of book</option>
                      <option value="Numeric">Numeric book</option>
                      <option value="Paper">Paper Book</option>
                    </select>
                    <small v-if="errors.type_book" class="text-danger">{{
                      errors.type_book
                    }}</small>
                  </div>
                  <div class="col-6">
                    <label for="">Status of books</label>
                    <select
                      class="form-control"
                      v-model="status_book"
                      aria-label="status book"
                      id="status_book"
                      name="status_book"
                    >
                      <option value="">Please select a status of book</option>
                      <option value="true">Avaible</option>
                      <option value="false">Not avaible</option>
                    </select>
                    <small v-if="errors.status_book" class="text-danger">{{
                      errors.status_book
                    }}</small>
                  </div>
                  <div class="col-12">
                    <label for="">Description</label>
                    <textarea name="description" id="description" class="form-control" v-model="description" rows="3">Enter some description for this book</textarea>
                    <small v-if="errors.description" class="text-danger">{{
                        errors.description
                    }}</small>
                  </div>
                  <div class="col-6" v-if="type_book !== 'Paper'">
                    <label for="">File of books</label>
                    <input type="file" name="file_book" id="file_book" class="form-control" @change="validateFilePdf"/>
                    {{ book.pdf_file }}
                  </div>
                  <div class="col-6">
                    <label for="">Image of books</label>
                    <input type="file" name="image_book" id="image_book" class="form-control" @change="validateImage"/>
                    {{ book.picture_books }}
                  </div>
                  <div class="mt-2">
                      <button type="submit" class="btn btn-outline-primary">Save Changes</button> &NonBreakingSpace;
                      <button @click="cancelEditing" class="btn btn-outline-secondary">Cancel</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div class="col-lg-5 col-md-5 col-sm-6">
            <div class="white-box text-center">
              <img
                :src="book.picture_books"
                class="img-responsive" style="width: 100%;border-radius: 10px;"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Footer></Footer>
</template>

<script>
import { RouterLink } from 'vue-router'
import Header from '../components/header.vue'
import Footer from '@/components/Footer.vue'
import axios from 'axios'
export default {
  components: {
    Header,
    Footer
  },
  data() {
    return {
      book: [],
      username: localStorage.getItem('username') || '',
      is_staff:localStorage.getItem('is_staff') || '',
      token: localStorage.getItem('token') || '',
      user_id: localStorage.getItem('url') || '',
      user:'',
      isEditing: false,
      author_book: '',
      title_book: '',
      year_publication: '',
      gender_book: '',
      type_book: '',
      status_book: '',
      description : '',
      file_book: 'null',
      image_book: 'null',
      errors:{
        author_book: '',
        title_book: '',
        year_publication: '',
        gender_book: '',
        type_book: '',
        status_book: '',
        description:'',
        file_book: '',
        image_book: '',
        wrong_fields : ''
      }
    }
  },
  mounted() {
    const book_id = this.$route.params.book_id
    const requestOptions = {
      headers: {},
    };
    if (this.token) {
      requestOptions.headers.Authorization = `Token ${this.token}`;
    }
    // Get all book to fill editing
    axios
      .get(`books/${book_id}/`,requestOptions)
      .then((response) => {
        this.book = response.data;
        axios.get(this.book.user,requestOptions)
          .then((userResponse) => {
            this.book.user = userResponse.data.username;
            console.log(this.book.user);
          })
          .catch((error) => {
            console.error('Erreur lors de la récupération des données de l\'utilisateur : ', error);
          });
      })
      .catch((error) => {
        console.error('Erreur lors de la récupération des données : ', error);
      });
  },
  methods: {

    // Displaying and undisplaying file book fiels if book is paper or Numeric  type
    showFileInput(){
      if (this.type_book === 'Paper') {
        this.display_input_file = false;
      } else {
        this.display_input_file = true;
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

    // Afficher le formulaire d'édition et cacher le tableau
    startEditing() {
      this.author_book = this.book.author;
      this.title_book = this.book.title;
      this.year_publication = this.book.year_publication;
      this.gender_book = this.book.gender;
      this.type_book = this.book.type_book;
      this.status_book = this.book.status_book;
      this.description = this.book.description;
      this.file_book = this.book.pdf_file
      this.image_book = this.book.picture_books
      this.isEditing = true;
    },
    // Delete selected book
    async deleteBook(){
      console.log("deleteBook");
      try {
        const response = await axios.delete(`books/${this.$route.params.book_id}/`,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': `Token ${this.token}`
            }
          }
        );
        this.$router.push('/loanbook/dashboard_book_admin');

      } catch (error) {
        console.log('erreur de suppression');

        if (error.response && error.response.data) {
          this.errors.wrong_fields = "Oups! Something wrong, please try again";
        }
        console.error('Error:', error.response ? error.response.data : error);
      }
    },
    // Save change for editing book
    async saveChanges() {

      if (!this.isEditing) {
        this.isEditing = true;
      }
      this.clearErrors();
      if(this.isValidForm()){

        console.log('😒😒😒😒😒');
        let formData = new FormData();

        formData.append('user', this.user_id);
        formData.append('author', this.author_book);
        formData.append('title', this.title_book);
        formData.append('year_publication', this.year_publication);
        formData.append('gender', this.gender_book);
        formData.append('type_book', this.type_book);
        formData.append('status_book', this.status_book);
        formData.append('description', this.description);

        if (this.file_book!== this.book.pdf_file) {
          formData.append('pdf_file', this.file_book)
        }
        if (this.image_book !== this.book.picture_books ) {
          formData.append('picture_books', this.image_book)
        }

        try {
          const response = await axios.patch(`books/${this.$route.params.book_id}/`,formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Token ${this.token}`
              }
            }
          );
          console.log('Success');
          this.$router.push('/loanbook/dashboard_book_admin');

        } catch (error) {
          console.log('Echec');
          if (error.response && error.response.data) {
            this.errors.wrong_fields = "Something wrong, please try again";
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
        console.log('😒oups1');
      }
      if (!this.title_book.trim()) {
        this.errors.title_book = "Title is required";
        valid = false;
        console.log('😒oups2');
      }
      if (!this.year_publication) {
        this.errors.year_publication = "year of publication is required";
        valid = false;
        console.log('😒oups3');
      }
      if (!this.gender_book) {
        this.errors.gender_book = "Gender is required";
        valid = false;
      }
      if (!this.type_book) {
        this.errors.type_book = "Type of book is required";
        valid = false;
      }
      if (!this.status_book && !this.book.status_book) {
        this.errors.status_book = "Status is required";
        valid = false;
      }
      if (!this.description) {
        this.errors.description = "Description is required";
        valid = false;
        console.log('😒oups4');
      }
      // if (this.type_book === 'Numeric' && !this.file_book) {
      //   this.errors.file_book = "File is required";
      //   valid = false;
      //   console.log('😒oups5');
      // }
      // if (!this.image_book && !this.book.picture_books) {
      //   this.errors.image_book = "Image is required";
      //   valid = false;
      //   console.log('😒oups6');
      // }
      return valid;
    },
    // Clean error after resolve them
    clearErrors() {
      this.errors.author_book = '';
      this.errors.title_book = '';
      this.errors.gender_book = '';
      this.errors.year_publication = '';
      this.errors.type_book = '';
      this.errors.status_book = '';
      this.errors.description = '';
      this.errors.file_book = '';
      this.errors.image_book = '';
      this.errors.wrong_fields = '';
    },
    // Cancel editing
    cancelEditing() {
      this.isEditing = false;
    }
}
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  margin-bottom: 20px;
}

.card-body {
  padding: 20px;
}

.table-product td {
  vertical-align: middle;
}

.white-box img {
  width: 100%;
  height: auto;
  border-radius: 10px;
}
</style>

