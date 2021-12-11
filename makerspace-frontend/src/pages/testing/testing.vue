<template>
  <div class="container mt-5 mb-5">
    <h1>Testing</h1>
    <button @click="testClick">send help</button>
    <p>{{this.test}}</p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  components: {},
  data: () => ({test: ""}),
  methods : {
    async testClick() {
      const res = await axios.post("http://localhost:5000/vuetest", {ttt : "data"});
      this.test = res.data["Status"];
    }
  },
  mounted() {
  }
}
</script>

<style scoped>
h6 {
  font-weight: 700;
}
.col {
  height: 90vh;
  overflow: auto;
}
.draggable-list {
  min-height: 10vh;
}
.draggable-list > div {
  cursor: pointer;
}
</style>