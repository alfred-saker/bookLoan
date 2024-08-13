<template>
  <NavbarHead />
  <br><br><br>
  <div class="wrapp_home">
    <div class="section_start text-center">J'affiche les statistiques ici</div>
    <br><br><br>
    <div class="contain_book_recentely">
      <div class="contain_option">
        <div>
          <h2 class="fw-bold fs-5">Recently added books</h2>
        </div>
        <div class="special">
          <button class="btn btn-primary"><font-awesome-icon icon="plus" /> New book</button>
          <a href="#" class="btn btn-primary ml-3">See All <font-awesome-icon icon="angle-right" /></a>
        </div>
      </div>
      <div class="new_book_add shadow p-3 bg-white rounded">
        <div class="new_book" v-for="n in 4" :key="n">
          <img src="https://i.pravatar.cc/150" alt="book image" class="rounded text-center">
          <div class="items_book">
            <p class="title_book fw-semibold fs-7">A la recherche de ma fille</p>
            <p class="author_book fw-medium fs-7 mt-2">Locko Tata</p>
          </div>
        </div>
      </div>
    </div>
    <div class="container_category_book">
      <div class="contain_option">
        <div>
          <h2 class="fw-bold fs-5">Category</h2>
        </div>
        <div class="special">
          <button class="btn btn-primary"><font-awesome-icon icon="plus" /> New book</button>
          <a href="#" class="btn btn-primary ml-3">See All <font-awesome-icon icon="angle-right" /></a>
        </div>
      </div>
      <div class="section_category">
        <ul>
          <li v-for="category in categories" :key="category"><a href="#" class="badge text-bg-primary">{{ category }}</a></li>
        </ul>
      </div>
      <div class="category_book shadow p-3 bg-white rounded">
        <div class="list_category" v-for="n in 4" :key="n">
          <img src="https://i.pravatar.cc/150" alt="book image" class="rounded text-center">
          <div class="items_category">
            <p class="title_book fw-semibold fs-7">A la recherche de ma fille</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import NavbarHead from '@/components/admin/NavbarHead.vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBars, faTimes, faHome, faInfoCircle, faEnvelope, faSignOutAlt, faCaretDown, faPlus, faAngleRight } from '@fortawesome/free-solid-svg-icons';

library.add(faBars, faTimes, faHome, faInfoCircle, faEnvelope, faSignOutAlt, faCaretDown, faPlus, faAngleRight);

export default {
  name: 'HomeContent',
  components: {
    FontAwesomeIcon,
    NavbarHead
  },
  data() {
    return {
      categories: ['All', 'Sci-Fi', 'Drama', 'Business', 'Education', 'Geography', 'Business', 'Education', 'Geography', 'Business', 'Education', 'Geography', 'Business', 'Education', 'Geography']
    };
  }
};
</script>

<style scoped>
.wrapp_home {
  margin-top: 4em; /* Adjust margin to account for NavbarHead */
  position: fixed;
}

.container_category_book .category_book {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 1em;
  margin: 0 auto;
  max-width: 1000px;
  border-radius: 5px;
}

.container_category_book .list_category {
  z-index: 2;
  border: 1.5px solid white;
  border-radius: 5px;
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
  margin: 0 0 1em;
  padding: 0.5em;
  width: 200px;
  text-align: center;
}

.container_category_book .section_category .items_category {
  width: 100%;
  margin-top: 10px;
}

.container_category_book .section_category::-webkit-scrollbar {
  height: 7px; /* Set the height of the scrollbar */
}

.container_category_book .section_category::-webkit-scrollbar-thumb {
  background: #eee9e9; /* Color of the scrollbar handle */
  border-radius: 4px; /* Roundness of the scrollbar handle */
}

.container_category_book .section_category ul {
  display: flex;
  max-width: 1000px;
  margin: 0 auto;
}

.container_category_book .section_category {
  width: 1000px;
  white-space: nowrap;
  margin: 0 auto 1em auto;
  overflow: hidden;
}

.container_category_book .section_category:hover {
  overflow-x: auto;
}

.container_category_book .section_category ul li a {
  margin: 1em 1em 1em 0;
  text-decoration: none;
}

.container_category_book .contain_option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1000px;
  padding-top: 2em;
  margin: 3px auto;
}

.container_category_book .contain_option .special {
  width: 30%;
  text-align: center;
}

.contain_book_recentely .contain_option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1000px;
  padding: 0.5em;
  margin: 0 auto;
}

.contain_book_recentely .contain_option .special {
  width: 30%;
  text-align: center;
}

.new_book_add {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 1em;
  margin: 0 auto;
  max-width: 1000px;
  border-radius: 5px;
}

.new_book_add .new_book {
  border: 1.5px solid white;
  border-radius: 5px;
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
  margin: 0 0 1em;
  padding: 0.5em;
  width: 200px;
  text-align: center;
}

.new_book .items_book {
  width: 100%;
  margin-top: 10px;
}

@media screen and (max-width: 1020px) {
  .section_category {
    width: 100%;
  }

  .container_category_book .section_category ul {
    display: block;
  }

  .container_category_book .contain_option {
    flex-direction: column;
    align-items: flex-start;
  }

  .container_category_book .contain_option .special {
    width: 100%;
    text-align: left;
    margin-top: 1em;
  }

  .contain_book_recentely .contain_option {
    flex-direction: column;
    align-items: flex-start;
  }

  .contain_book_recentely .contain_option .special {
    width: 100%;
    text-align: left;
    margin-top: 1em;
  }
}
</style>
