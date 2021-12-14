<template>
  <div class="container mt-5 mb-5">
    <h1>Request Form</h1>
    <FormulateForm

        @submit="onSubmit"/>


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

      <div class="inputs">
        <FormulateInput
          type="group"
          :repeatable="true"
          add-label="+ Add Material"
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
          <div>
            <FormulateInput
              v-if="values[index] && values[index].hasOwnProperty('variants') && values[index].variants === 'drip'"
              type="checkbox"
              name="roomForCream"
              label="Leave me room for cream"
            />
          </div>
        </FormulateInput>
        <pre>{{ values }}</pre>
      </div>

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
  </div>
</template>

<script>
//import axios from "axios";

export default {
  data() {
    return {
      values: [{}],
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
      },
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
    };
  },
  methods: {
    onSubmit() {
    },
    onReset() {
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
    },

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
};
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';
</style>