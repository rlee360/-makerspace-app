<template>
  <div class="container mt-5 mb-5">
    <h1>Request Form</h1>
    <FormulateForm class="inputs" @submit="onSubmit" v-model="values">
      <FormulateInput
          type="file"
          name="files"
          label="Select your files to upload"
          help="Select one or more docs to upload"
      />
      <FormulateInput type="submit" value="Submit"/>
      <FormulateInput type="submit" value="Reset"/>
      <pre>{{values}}</pre>
    </FormulateForm>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      requestData: {
        files: "",
        email: "abc@cooper.edu",
        name: "abc 123",
        material: "PLA",
        notes: "abb",
        shells: "2",
        infill: "30",
        top_bottom: "3",
        filename: "file.stl"
      }
    }
  },
  methods: {
    submitHandler() {
    },
    async fileSet(f) {
      console.log(f);
      const res = await axios.post("http://localhost:5000/api/request/create", this.requestData, {'Content-Type': 'multipart/form-data'});
      console.log(res);
    },
    async onSubmit() {
      console.log(this.requestData);
       const res = await axios.post("http://localhost:5000/api/request/create", this.requestData, {'Content-Type': 'multipart/form-data'});
       console.log(res);
    }
  }
}
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';
</style>