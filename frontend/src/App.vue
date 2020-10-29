<template>
  <v-app>

    <v-content>
      <router-view/>
    </v-content>

  </v-app>
</template>

<script>
export default {
  data () {
    return {
      fixed: false,
    }
  },
  name: 'App'
}
</script>

<style scoped>

</style>
