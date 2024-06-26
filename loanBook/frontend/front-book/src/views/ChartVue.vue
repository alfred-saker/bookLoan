<template>
    <div>
      <Header></Header>
      <div class="container-chart">
        <div class="chart-container">
          <canvas id="downloadBorrowChart" aria-label="chart" role="img"></canvas>
        </div>
        <div class="chart-container">
          <canvas id="bookAuthorChart" aria-label="chart" role="img"></canvas>
        </div>
        <div class="chart-container">
          <canvas id="bookTypeChart" aria-label="chart" role="img"></canvas>
        </div>
        <div class="chart-container">
          <canvas id="bookGenreRadarChart" aria-label="chart" role="img"></canvas>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </template>
  <script>
  import axios from 'axios'
  import Header from '@/components/header.vue'
  import Footer from '@/components/Footer.vue'
  import { Chart, registerables } from 'chart.js'
  
  Chart.register(...registerables)
  
  export default {
    components: {
      Header, 
      Footer
    },
    data() {
      return {
        downloadBorrowChart: null,
        bookTypeChart: null,
        bookAuthorChart: null,
        bookGenreRadarChart: null,
        downloadBorrowData: null,
        bookTypeData: null,
        bookAuthorData: null,
        bookGenreRadarData: null
      }
    },
    mounted() {
      this.fetchChartData()
    },
    methods: {
      async fetchChartData() {
        try {
          const response = await axios.get('books/')
          const books = response.data.results
  
          this.prepareDownloadBorrowData(books)
          this.prepareBookTypeData(books)
          this.prepareBookAuthorData(books)
          this.prepareBookGenreRadarData(books)
  
          this.renderCharts()
        } catch (error) {
          console.error('Error fetching data:', error)
        }
      },
      prepareDownloadBorrowData(books) {
        const labels = books.map((book) => book.title)
        const downloads = books.map((book) => book.download_count)
        const borrows = books.map((book) => book.borrow_count)
  
        this.downloadBorrowData = {
          labels,
          datasets: [
            {
              label: 'Downloads',
              backgroundColor: 'rgba(54, 162, 235, 0.6)',
              data: downloads
            },
            {
              label: 'Borrows',
              backgroundColor: 'rgba(255, 99, 132, 0.6)',
              data: borrows
            }
          ]
        }
      },
      prepareBookTypeData(books) {
        const typeCounts = books.reduce((acc, book) => {
          acc[book.type_book] = (acc[book.type_book] || 0) + 1
          return acc
        }, {})
  
        this.bookTypeData = {
          labels: Object.keys(typeCounts),
          datasets: [
            {
              data: Object.values(typeCounts),
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)'
              ]
            }
          ]
        }
      },
      prepareBookAuthorData(books) {
        const authorCounts = books.reduce((acc, book) => {
          acc[book.author] = (acc[book.author] || 0) + 1
          return acc
        }, {})
  
        this.bookAuthorData = {
          labels: Object.keys(authorCounts),
          datasets: [
            {
              label: 'Books',
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              data: Object.values(authorCounts)
            }
          ]
        }
      },
      prepareBookGenreRadarData(books) {
        const genreCounts = books.reduce((acc, book) => {
          acc[book.gender] = (acc[book.gender] || 0) + 1
          return acc
        }, {})
  
        this.bookGenreRadarData = {
          labels: Object.keys(genreCounts),
          datasets: [
            {
              label: 'Books by Genre',
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              data: Object.values(genreCounts)
            }
          ]
        }
      },
      renderCharts() {
        this.renderDownloadBorrowChart()
        this.renderBookTypeChart()
        this.renderBookAuthorChart()
        this.renderBookGenreRadarChart()
      },
      renderDownloadBorrowChart() {
        const ctx = document.getElementById('downloadBorrowChart').getContext('2d')
        if (this.downloadBorrowChart) {
          this.downloadBorrowChart.destroy()
        }
        this.downloadBorrowChart = new Chart(ctx, {
          type: 'bar',
          data: this.downloadBorrowData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Books'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Count'
                }
              }
            }
          }
        })
      },
      renderBookTypeChart() {
        const ctx = document.getElementById('bookTypeChart').getContext('2d')
        if (this.bookTypeChart) {
          this.bookTypeChart.destroy()
        }
        this.bookTypeChart = new Chart(ctx, {
          type: 'pie',
          data: this.bookTypeData,
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        })
      },
      renderBookAuthorChart() {
        const ctx = document.getElementById('bookAuthorChart').getContext('2d')
        if (this.bookAuthorChart) {
          this.bookAuthorChart.destroy()
        }
        this.bookAuthorChart = new Chart(ctx, {
          type: 'bar',
          data: this.bookAuthorData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Count'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Authors'
                }
              }
            }
          }
        })
      },
      renderBookGenreRadarChart() {
        const ctx = document.getElementById('bookGenreRadarChart').getContext('2d')
        if (this.bookGenreRadarChart) {
          this.bookGenreRadarChart.destroy()
        }
        this.bookGenreRadarChart = new Chart(ctx, {
          type: 'radar',
          data: this.bookGenreRadarData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              r: {
                angleLines: {
                  display: false
                },
                suggestedMin: 0,
                suggestedMax: 10
              }
            }
          }
        })
      }
    }
  }
  </script>
  
  <style>
  .container-chart {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    max-width: 1400px;
    margin-top: 1em;
    padding: 1em;
  }
  .chart-container {
    width: 600px;
    margin-top: 2em;
  }
  </style>
  @/components/footer.vue@/components/Footer.vue