<template>
  <div class="container mt-5 mb-5">
    <h1>Request Form</h1>
    <FormulateForm class="inputs" @submit="onSubmit" @reset="onReset" v-model="data_values">
      <FormulateInput
          type="file"
          name="files"
          label="Select your files to upload"
          help="Select one or more docs to upload"
      />
      <FormulateInput
          type="select"
          name="material_type"
          label="Select a Material"
          placeholder="Select one"
          validation="required"
          :options="material_data.types"
          @change="matChanged"
      />
      <FormulateInput
          type="select"
          name="material"
          label="Select a Material"
          placeholder="Select one"
          validation="required"
          error-behavior="submit"
          v-if="material_data.changed == true"
          :options="material_data.specifics"
      />
      <FormulateInput type="submit" label="Submit"/>
      <FormulateInput type="submit" label="Reset"/>
    </FormulateForm>
    <input type="file" @change="fileChanged($event)"/>
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
        filename: "file.stl",
        class_id: "ME420"
      },
      data_values: {},
      material_data: {
        types: [],
        changed: false,
        specifics: []
      }
    }
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/api/material/");
    this.material_data.types = res.data;
  },
  methods: {
    async matChanged() {
      this.material_data.changed = true;
      window.data_values = this.data_values;
      const res = await axios.get("http://localhost:5000/api/material/?type=" + this.data_values.material_type);
      this.material_data.specifics = res.data;
    },
    fileChanged(evt) {
      console.log(evt);
      this.requestData.files = evt.target.files[0];
      console.log(this.requestData)
    },
    // async fileSet(f) {
    //   console.log(f);
    //   const res = await axios.post("http://localhost:5000/api/request/create", this.requestData, {'Content-Type': 'multipart/form-data'});
    //   console.log(res);
    // },
    // async onSubmit() {
    //   console.log(this.requestData);
    //    const res = await axios.post("http://localhost:5000/api/request/create", this.requestData, {'Content-Type': 'multipart/form-data'});
    //    console.log(res);
    // }
    async onSubmit() {
      window.data_values = this.data_values;
      this.requestData.files = this.data_values.files.files[0].file;
      let fff = new FormData();
      Object.keys(this.requestData).forEach((i) => {
        fff.append(i, this.requestData[i])
      });
      //fff.append('files', this.data_values.abc.files[0].file)
      const res = await axios.post("http://localhost:5000/api/request/create", fff, {'Content-Type': 'multipart/form-data'});
      console.log(res);
    },
    onReset() {
      this.values = {}
    },
  }
}
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';
</style>