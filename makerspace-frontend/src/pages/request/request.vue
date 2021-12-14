<template>
  <div class="container mt-5 mb-5">
    <h1>Request Form</h1>
    <FormulateForm
        @submit="onSubmit"
        v-model="data_values">

      <FormulateInput
          type="file"
          name="files"
          label="Select your files to upload"
          help="Select one or more docs to upload"
      />

      <FormulateInput
          type="email"
          name="email"
          placeholder="Enter email"
          label="Email address:"
          validation="required|email"/>

      <FormulateInput
          type="text"
          name="name"
          placeholder="Enter Name"
          label="Student Name:"/>


      <FormulateInput
          type="text"
          name="material"
          placeholder="Enter Material"
          label="Material:"
     />

      <FormulateInput
          type="text"
          name="class_id"
          placeholder="class_id"
          label="Class_id:"
     />



      <!--
      <div class="inputs">
        <FormulateInput
          type="group"
          :repeatable="false"
          v-model="values"
          #default="{ index }"
        >
          <div class="double">
            <FormulateInput
              type="select"
              name="material"
              label="Select a Material"
              placeholder="Select one"
              validation="required"
              :options="{Material1: 'Material1', Material2: 'Material2', Material3: 'Material3'}"
            />
            <FormulateInput
              type="select"
              name="variant"
              validation="required"
              placeholder="Select one"
              :label="label(index)"
              :options="materialOptions(index)"
            />
          </div>
        </FormulateInput>
      </div>
      -->

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
          name="notes"
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
import axios from "axios";

export default {
  data() {
    return {
      values: [{}],
      requestData: {
        files: "",
      },
      data_values : {},
/*
      options: {
          Material1: {
            blue1: 'blue1',
            green1: 'green1',
            red1: 'red1'
          },
          Material2: {
            blue2: 'blue2',
            green2: 'green2',
            red2: 'red2'
          },
          Material3: {
            blue3: 'blue3',
            green3: 'green3',
            red3: 'red3'
          }
        }
        */

    };
  },
  methods: {
    async onSubmit() {
      window.data_values = this.data_values;
      this.data_values.files = this.data_values.files.files[0].file;
      this.data_values.filename = this.data_values.files.name;
      let fff = new FormData();
      Object.keys(this.data_values).forEach(
          (i) => {fff.append(i, this.data_values[i])});
      //fff.append('files', this.data_values.abc.files[0].file)
      const res = await axios.post("http://localhost:5000/api/request/create", fff, {'Content-Type': 'multipart/form-data'});
      console.log(res.data);
      alert("Submitted");

    },

    onReset() {
      this.values = {}
    },

    fileChanged(evt) {
      console.log(evt);
      this.requestData.files = evt.target.files[0];
      console.log(this.requestData)
    },

    selectFile() {
      console.log()
      console.log("YO!", this.$refs.file.files);
    },

    /*
    material (index) {
      return Array.isArray(this.values) &&
        this.values[index] &&
        this.values[index].material
    },
    label (index) {
      return this.material(index) ? `What type of ${this.material(index)}` : '----'
    },
    materialOptions (index) {
      const type = this.material(index)
      const options = type ? this.options[type] : {}
      const values = this.values[index] || {}
      const variant = values.variant
      if (variant && !options[variant]) {
        this.values[index].variant = undefined
      }
      return options
    }
    }
    */
  }
};
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';
</style>