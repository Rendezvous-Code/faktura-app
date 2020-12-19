<template>
  <div id="app">
    <img src="./assets/logo.png">
    <p>'Accounts available:'</p>
    <p>
      {{ info }}
    </p>
  </div>
</template>

<script>
import axios from 'axios'
import Vue from 'vue'

global.Vue = Vue

new Vue({ // eslint-disable-line no-new
  name: 'App',
  data () {
    return {
      info: null
    }
  },
  mounted () {
    let url = process.env.API_URL + '/api/accountant/accountant/'
    let config = {
      headers: {
        'Authorization': `Token 94741a380975dc3af6d5a0a54f946945c9bbfab6`
      }
    }
    axios
      .get(url, config)
      .then(response => (this.info = response))
    console.log(this.info)
    console.log('print this')
  }
})
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
