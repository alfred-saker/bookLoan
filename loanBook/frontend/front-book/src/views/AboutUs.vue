<template>
    <Header></Header>
    <h2 class="fs-2 text-center" style="padding: 1em;">Who we are?</h2>
    <div class="about_us">
        <div class="img_about">
            <img :src="about_us_image" alt="About us image">
        </div>
        <div class="description_about">
            <h2 class="fs-2">Bienvenue dans le monde de BookLoan !</h2>
            <p>Chez <strong>BookLoan</strong> , nous croyons en le pouvoir transformateur de la lecture. Notre plateforme a été créée avec une vision simple mais puissante : connecter les passionnés de lecture avec les livres qu'ils adorent, de manière pratique, accessible et communautaire.</p>
            

            <h3 class="fs-3">Notre Mission</h3>
            <p>Notre mission est de rendre la lecture plus accessible à tous, en offrant une plateforme conviviale où les utilisateurs peuvent emprunter, échanger et découvrir une vaste sélection de livres. Que vous soyez un amoureux des classiques intemporels, un passionné de romans contemporains ou un explorateur avide de nouvelles connaissances, BookLoan est là pour vous accompagner dans votre voyage littéraire.</p>
            

            <h3 class="fs-3">Comment ça marche</h3>
            <p>BookLoan offre une expérience de prêt de livres simple et intuitive. Les utilisateurs peuvent parcourir notre catalogue en ligne, explorer des milliers de titres dans une variété de genres, et emprunter les livres qui captivent leur imagination. De plus, notre fonction de profil utilisateur personnalisé permet aux membres de suivre leurs emprunts, de partager leurs recommandations et de se connecter avec d'autres lecteurs partageant les mêmes idées.</p>
            

            <h3 class="fs-3">Notre Engagement envers la Communauté</h3>
            <p>Chez BookLoan, nous croyons en la force de la communauté. Nous encourageons le partage des connaissances, des idées et des histoires à travers notre plateforme. En facilitant les échanges entre les lecteurs, nous créons un environnement dynamique où la passion pour la lecture peut prospérer.</p>
            

            <h3 class="fs-3">Notre Équipe</h3>
            <p>L'équipe de BookLoan est composée de passionnés de lecture et de technologues dévoués, unis par une vision commune de rendre la lecture plus accessible et plus enrichissante pour tous. Nous sommes constamment à l'écoute de nos utilisateurs et nous nous efforçons d'améliorer continuellement notre plateforme pour répondre à leurs besoins et à leurs attentes.</p>
            
            <p> Rejoignez-nous dans notre mission de partager le plaisir de la lecture avec le monde entier. Chez BookLoan, chaque page tournée est une nouvelle aventure à explorer.</p>
            
            <p>Bienvenue dans notre communauté de lecteurs passionnés !</p>
        </div>
    </div>
    <Footer></Footer>
</template>

<script>
import { RouterLink } from 'vue-router';
  import Header from '../components/header.vue';
  import Footer from '@/components/Footer.vue'
  import axios from 'axios'
    export default{
        components:{
            Header,
            Footer
        },
        data(){
            return {
                about_us_image:'https://images.unsplash.com/photo-1598015132635-131afe3ba07f?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
            }
        }
    }
</script>

<style>
.about_us{
    display: flex;
    justify-content: center;
}
.about_us p{
   text-align: justify;
}
.about_us .description_about{
    width: 60%;
    margin-left: 1em;
}

.about_us .img_about{
    width:35%;  
}
.about_us .img_about img{
    width:"100%";  
}
</style>