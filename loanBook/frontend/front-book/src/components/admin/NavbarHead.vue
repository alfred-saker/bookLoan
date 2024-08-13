<template>
    <div class="block_navbar_head ">
        <div class="items_navbar">
            <input type="text" name="" id="" placeholder="Enter the text" class="form-control">
        </div>
        <div class="picture">
            <img src="https://i.pravatar.cc/40" alt="" class="rounded-circle">
            <span style="margin-left: 5px;" class="special">Alfred saker</span>&nbsp;
            <font-awesome-icon icon="caret-down" />
        </div>
    </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBars, faTimes, faHome, faInfoCircle, faEnvelope,faSignOutAlt,faCaretDown } from '@fortawesome/free-solid-svg-icons';
  
library.add(faBars, faTimes, faHome, faInfoCircle, faEnvelope,faSignOutAlt,faCaretDown);
 export default {
    name: 'NavabarHead',
    components: {
      FontAwesomeIcon,
    },
    
  };
</script>

<style scoped>
.block_navbar_head{
    max-width: 1400px;
    display: flex;
    justify-content:space-between;
    margin: auto;
}
.items_navbar input[type="text"]{
    width: 60%;
    /* margin-right: 1em; */
}
.items_navbar{
    /* background-color: rgb(206, 203, 38); */
    width: 50%;
    text-align: center;
}
.picture{
    display: flex;
    align-items: center;
    width: 15%;
    text-align: center;
    /* background-color: aqua; */
}
@media screen and (max-width: 1016px) {
  .block_navbar_head {
    display: flex;
    margin:0 auto auto 1em;
    width: 70%;
    background-color: aqua;
  }

  .block_navbar_head .items_navbar input[type="text"] {
    width: 65vh;

  }
  .picture{
    display: none;
  }
}
</style>