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
            <p v-if="book.description">
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
              <div v-if="token && is_staff === 'true'">
                <button @click="startEditing" class="btn btn-dark" style="width: auto"
                  >Edit book</button
                >
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
                  </div>
                  <div class="col-6">
                    <label for="">Image of books</label>
                    <input type="file" name="image_book" id="image_book" class="form-control" @change="validateImage"/>
                  </div>
                  <div class="mt-2">
                      <button type="submit" class="btn btn-primary">Save Changes</button> &NonBreakingSpace;
                      <button @click="cancelEditing" class="btn btn-secondary">Cancel</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div class="col-lg-5 col-md-5 col-sm-6">
            <div class="white-box text-center">
              <img v-if="book.picture_books"
                :src="book.picture_books"
                class="img-responsive" style="width: 100%;"
              />
              <img v-else :src="default_image_url" alt="Default image" srcset="">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import Header from '../components/header.vue'
import axios from 'axios'
export default {
  components: {
    Header
  },
  data() {
    return {
      book: [],
      username: localStorage.getItem('username') || '',
      is_staff:localStorage.getItem('is_staff') || '',
      token: localStorage.getItem('token') || '',
      user_id: localStorage.getItem('url') || '',
      isEditing: false,
      author_book: '',
      title_book: '',
      year_publication: '',
      gender_book: '',
      type_book: '',
      status_book: '',
      description : '',
      file_book: null,
      image_book: null,
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
    console.log(book_id)
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
    showFileInput(){
      if (this.type_book === 'Paper') {
        this.display_input_file = false;
      } else {
        this.display_input_file = true;
      }
    },
    validateFilePdf(event) {
      const file_book = event.target.files[0];
      // const maxSize = 5 * 1024 * 1024; // 5MB
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      if (!file_book) {
        this.errors.file_book = "Please select a file.";
        return;
      }

      if (!allowedTypes.includes(file_book.type)) {
        this.errors.file_book = "Only PDF, DOCX, and TXT files are allowed.";
        return;
      }

      this.file_book = file_book
      this.errors.file_book = ''

    },
    validateImage(event) {
      const image = event.target.files[0];
      const maxSize = 5 * 1024 * 1024; // 5MB
      const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/svg'];
      
      if (!image) {
        this.errors.image_book = "Please select an image.";
        return;
      }
      
      if (!allowedTypes.includes(image.type)) {
        this.errors.image_book = "Only JPG, JPEG, SVG, and PNG files are allowed.";
        return;
      }
      
      if (image.size > maxSize) {
        this.errors.image_book = "Image size exceeds the limit (5MB).";
        return;
      }
      this.image_book = image
      this.errors.image_book = ''
      
      console.log(this.file_book);
      console.log(image);
    },
    startEditing() {
        // Afficher le formulaire d'édition et cacher le tableau
        this.author_book = this.book.author;
        this.title_book = this.book.title;
        this.year_publication = this.book.year_publication;
        this.gender_book = this.book.gender;
        this.type_book = this.book.type_book;
        this.status_book = this.book.status_book;
        this.description = this.book.description;
        this.file_book = this.book.pdf_file
        this.image_book = this.book.picture_books
        console.log(this.image_book);
        console.log(this.file_book);
        this.isEditing = true;
    },
    async saveChanges() {

        if (!this.isEditing) {
            this.isEditing = true;
        }
        this.clearErrors();
        if(this.isValidForm()){
            console.log('😒😒😒😒😒');
            let formData = new FormData();
            
            // Ajoutez les données de formulaire à FormData
            formData.append('user', this.user_id);
            formData.append('author', this.author_book);
            formData.append('title', this.title_book);
            formData.append('year_publication', this.year_publication);
            formData.append('gender', this.gender_book);
            formData.append('type_book', this.type_book);
            formData.append('status_book', this.status_book);
            formData.append('description', this.description);
            formData.append('pdf_file', this.file_book);
            formData.append('picture_books', this.image_book);

            if (this.type_book === 'Numeric') {
              formData.append('pdf_file', this.file_book);
            } 
            try {
              const response = await axios.put(`books/${this.$route.params.book_id}/`,formData,
                {
                  headers: {
                  Authorization: `Token ${this.token}`,
                  'Content-Type': 'multipart/form-data'
                  }
                }
              );

              console.log('youpii');
              console.log(response.data);
              this.$router.push('home');

            } catch (error) {
                console.log('nonni');

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
        if (!this.status_book) {
            this.errors.status_book = "Status is required";
            valid = false;
        }
        if (!this.description) {
            this.errors.description = "Description is required";
            valid = false;
            console.log('😒oups4');
        }
        // if (!this.file_book) {
        //     this.errors.file_book = "File is required";
        //     valid = false;
        //     console.log('😒oups5');
        // }
        if (!this.image_book) {
            this.errors.image_book = "Image is required";
            valid = false;
            console.log('😒oups6');
        }
        return valid;
    },
    clearErrors() {
      this.errors.author_book = '';
      this.errors.title_book = '';
      this.errors.gender_book = '';
      this.errors.year_publication = '';
      this.errors.type_book = '';
      this.errors.status_book = '';
      this.errors.description = '';
    //   this.errors.file_book = '';
      this.errors.image_book = '';
      this.errors.wrong_fields = '';
    },
    cancelEditing() {
        this.isEditing = false;
    }
}
}
</script>

<style>
.container {
  margin-top: 1em;
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 0 solid transparent;
  border-radius: 0;
}
.card .card-subtitle {
  font-weight: 300;
  margin-bottom: 10px;
  color: #8898aa;
}
.table-product.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f3f8fa !important;
}
.table-product td {
  border-top: 0px solid #dee2e6 !important;
  color: #728299 !important;
}
p {
  line-height: 2;
}
</style>
