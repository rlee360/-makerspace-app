<template>
  <div class="container mt-5 mb-5">
    <h1>Request Form</h1>
    <FormulateForm class="inputs" @submit="onSubmit" v-model="values" @reset="onReset">
      <FormulateInput
          name="file"
          label="File"
          type="Open File"
          :state="Boolean(file1)"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."/>
      <div class="mt-3">Selected file: {{ file1 ? file1.name : '' }}</div>

      <FormulateInput
          type="email"
          name="email"
          placeholder="Enter email"
          label="Email address:"
          validation="required|email"/>

      <FormulateInput
          name="material"
          label="Material:"
          type="select"
          :options="{ material1: 'material1', material2:'material2'}"/>

      <FormulateInput
          name="shells"
          label="Shells:"
          type="number"
          max="100"
          min="0"/>

      <FormulateInput
          name="infill"
          label="Infill:"
          type="number"
          max="100"
          min="0"/>

      <FormulateInput
          name="top_bottom"
          label="Top bottom:"
          type="number"
          max="100"
          min="0"/>

      <FormulateInput
          name="Notes"
          type="textarea"
          label="Notes:"
          placeholder="Please give a short description of the project"
          rows="3"
          max-rows="10"/>
      <FormulateInput type="submit" value="Submit"/>
      <FormulateInput type="submit" value="Reset"/>
    </FormulateForm>
  </div>
</template>

<script>
//import axios from "axios";

export default {
  data() {
    return {
      requestData: {
        files: {},
        email: "",
        name: "",
        material: "",
        notes: "",
        shells: "",
        infill: "",
        top_bottom: "",
        filename: ""
      }
    }
  },
  methods: {
    submitHandler() {
    },
    async fileChanged(e1) {
      console.log(e1);
      //const res = await axios.get("http://localhost:5000/vuetest", {ttt: "data"});
      //const res = await axios.get("http://localhost:8080");
      //console.log(res);
      //this.test = res.data["Status"];
    },
    selectFile() {
      console.log()
      console.log("YO!", this.$refs.file.files);
    }
  }
}
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';
</style>